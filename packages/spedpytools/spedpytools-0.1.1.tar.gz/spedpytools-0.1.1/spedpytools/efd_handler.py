from sped.arquivos import ArquivoDigital
from sped.registros import Registro
from decimal import Decimal
from tqdm import tqdm
import pandas as pd
import importlib
import json
import itertools


class ArquivoDigitalSchema(object):
    
    _data_sources_def: dict
    _clazz_path: str
    _spreadsheet_def: list
    _views_def: list
    
    def __init__(self, filename: str = None):
        if filename is not None:
            self.load_from_file(filename)
    
    def load_from_file(self, filename: str):
        
        with open(filename, 'r') as f:
            self._schema_file = json.load(f)            
            self._data_sources_def = self._schema_file.get("data_sources", {})
            self._clazz_path = self._schema_file.get("clazz_path", None)
            self._spreadsheet_def = self._schema_file.get("spreadsheet", [])
            self._views_def = self._schema_file.get("views", [])
            
    @property
    def data_sources_def(self):
        return self._data_sources_def

    @property
    def clazz_path(self):
        return self._clazz_path
    
    @property
    def spreadsheet_def(self):
        return self._spreadsheet_def
    
    @property
    def views_def(self):
        return self._views_def
    
    def get_view_def(self, view_name: str):
        for view in self._views_def:
            if view.get('name') == view_name:
                return view
        return None
    
    def get_data_source_def(self, source_name: str):
        for data_source in self._data_sources_def:
            if data_source.get('name') == source_name:
                return data_source
        return None

    def get_spreadsheet_def(self, spreadsheet_name: str):
        for spreadsheet in self._spreadsheet_def:
            if spreadsheet.get('name') == spreadsheet_name:
                return spreadsheet
        return None

class ArquivoDigitalHandler(object):
    _arquivo_digital: ArquivoDigital
    _schema: ArquivoDigitalSchema
          
    def __init__(self, arquivo_digital: ArquivoDigital, schema: ArquivoDigitalSchema, verbose: bool = True):
        self._schema = schema
        self._arquivo_digital = arquivo_digital
        self._indexes = {}
        self._data_sources = self.__create_data_sources(verbose=verbose)
        self._views = self.__create_views(verbose=verbose)

    @property
    def data_sources(self):
        return self._data_sources
    
    @property
    def views(self):
        return self._views
    
    @property
    def arquivo_digital(self):        
        return self._arquivo_digital
    
    def __create_data_sources(self, verbose=True):

        sources = {}
        cache = {}
        source_map = self.__create_source_map()

        for registro in tqdm(self.__get_registros(), 
                            desc="processing registros", 
                            colour="RED",
                            disable=not verbose):

            if registro.REG in source_map:                

                cols = [f'{registro.REG}.{col}' for col in list(source_map[registro.REG][0])]
                #cols = [col for col in list(source_map[registro.REG][0])]
                cols_dict = source_map[registro.REG][1]
                parent = source_map[registro.REG][2]
                
                vals = [self.__get_column_value(registro, col, cols_dict) for col in cols]
                cache[registro.REG] = vals
                
                if parent: # Se existir um pai, adicionar os valores do pai
                    vals = vals + cache[parent]
                    cols += [f'{parent}.{parent_col}' for parent_col in source_map[parent][0]]      
                    parent = source_map[parent][2]           
                
                if registro.REG not in sources:
                    sources[registro.REG] = pd.DataFrame(columns=cols)
                    #sources[registro.REG] = sources[registro.REG].astype(self.__get_cols_dtypes(registro.REG, cols_dict)) 

                sources[registro.REG].loc[len(sources[registro.REG])] = vals
        
        return sources

    def __create_source_map(self): 
        map = {}
        for data_src_id in self._schema.data_sources_def:
            data_source = self._schema.data_sources_def.get(data_src_id)
            cols_dict = self.__get_all_cols_dict(data_source)   
            cols = list(cols_dict.keys())
            idx_names = data_source.get('index', '__rowid__').split("|")
                        
            if '__rowid__' in idx_names:
                cols = ['__rowid__'] if cols == [None] else ['__rowid__'] + cols
                
            #parent = data_source.get('parent', None)
            #if parent:
            #    cols += [f'{parent}.{idx}' for idx in map[parent][3]]                

            map[data_src_id] = (cols, cols_dict, data_source.get('parent', None), idx_names)

        return map
    '''
    def __get_cols_dtypes(self, registro: str, cols_dict):
        dtypes = {}
        try:
            for col_name in cols_dict:
                col = cols_dict.get(col_name)
                if isinstance(col, CampoNumerico): # definir que campos numericos sejam sempre float64               
                    dtypes[f'{registro}.{col_name}'] = 'float64'                
                    #dtypes[col_name] = 'float64'  
        except KeyError:
            raise ArquivoDigitalExportException(f"Não foi possível encontrar coluna {col_name} no registro {registro}")              
        
        return dtypes
    '''
    def __get_registros(self):        
        array = []
        for key in self._arquivo_digital._blocos:
            array += self._arquivo_digital._blocos[key]._registros
        return [self._arquivo_digital._registro_abertura] + array + [self._arquivo_digital._registro_encerramento]

    def __get_column_value(self, registro: Registro, col: str, cols_dict: dict):
        column = col.split('.')[-1]
        if column in cols_dict:
            return getattr(registro, cols_dict[column].nome)
        else:
            return self.__get_row_id(registro.REG) if column == '__rowid__' else col

    def __get_row_id(self, idx: str):
        if idx in self._indexes:
            row_id = self._indexes[idx] 
            return next(row_id)
        else:
            self._indexes[idx] = itertools.count(start=1)
            return next(self._indexes[idx])
        
    def __get_all_cols_dict(self, data_source: any):
        columns_dict = {}
        try:
            modulo = importlib.import_module(self._schema.clazz_path)
            clazz = getattr(modulo, data_source['clazz'])
            columns_dict = {campo.nome: campo for campo in getattr(clazz, 'campos') if campo.nome != 'REG'}
        except ImportError:
            print(f"Erro: O módulo '{modulo}' não foi encontrado.")
        except AttributeError:
            print(f"Erro: A classe '{clazz}' não foi encontrada no módulo '{modulo}'.")
        return columns_dict
    
    def __create_views(self, verbose=True):
        
        views = {}
        try:           
                    
            for view in tqdm(
                    self._schema.views_def,
                    desc="creating views", 
                    colour="RED",
                    disable=not verbose
                ):
                
                view_name = view.get('name')
                ldata_source = view.get('data_source', '')
                cols = view.get('columns', ['__all__'])

                left_df = self._data_sources.get(ldata_source)

                for join in view.get('joins', []):
                    rdata_source = join.get('data_source', '')
                    right_df = self._data_sources.get(rdata_source)               
                    joinned_df = pd.merge(
                        left=left_df,
                        right=right_df, 
                        left_on=join.get('left_on', '__rowid__'), 
                        right_on=join.get('right_on', f'{rdata_source}.__rowid__'),
                        how=join.get('how', 'inner')) 
                    
                    left_df = joinned_df                                   

                views[view_name] = (left_df if cols == ['__all__'] else left_df[cols])
                
        except Exception as e:
            raise ArquivoDigitalExportException(f'Error creating view [{view_name}]: {e}')
        
        return views

 
    def to_excel(self, filename: str, verbose: bool = False):
        """
        Exports the constructed DataFrames to an Excel file.

        This method iterates through the schema blocks and their associated records, 
        exporting each DataFrame to a separate sheet in the specified Excel file. 
        It skips any records marked for exclusion.

        Args:
            filename (str): The name of the Excel file to which the data will be exported.
            verbose (bool): If False, suppresses progress output during processing. Defaults to True.

        Raises:
            RuntimeError: If there is an error during the export process, a RuntimeError is raised 
            with a message indicating the failure.

        Examples:
            handler.to_excel("output.xlsx")
        """
        try:
            with pd.ExcelWriter(filename) as writer:
                for tab in self._schema.spreadsheet_def.get("tabs", []):  
                    view_name = tab.get('view')
                    if view_name in self._views.keys():
                        view_df = self._views[view_name] 

                        if view_df is not None:
                            
                            tab_info = {
                                'name': view_name,
                                'data_source': self._schema.get_view_def(view_name).get('data_source'),
                                'dataframe': view_df,
                                'columns': tab.get('columns', ['__all__'])
                            }
                            rendered_tab = self.__render_tab(tab_info, verbose)
                            rendered_tab.to_excel(writer, sheet_name=tab.get('name', view_name), index=False)
                            
        except Exception as ex:
            raise ArquivoDigitalExportException(
                f"Erro não foi possível exportar dados para arquivo: {filename}, view: {view_name}, erro: {ex}"
            ) from ex

    def __render_tab(self, tab_info: dict, verbose: bool = False):
        
        view_name = tab_info.get('name')
        view = tab_info.get('dataframe')
        columns = tab_info.get('columns')
        data_source = tab_info.get('data_source')
        
        if columns == ['__all__']:
            tab = view.copy(deep=True)
        else:
            tab = view[columns].copy(deep=True)       
        
        # Remover prefixos da view base
        tab.columns = [col.replace(f"{data_source}.", "") for col in tab.columns]
        
        # Converter valores decimais para o formato brasileiro
        for col in tqdm(tab.columns, desc=f"preparing [{view_name}]", colour="RED", disable=not verbose):
            if type(tab[col][0]) == Decimal:                
                tab[col] = tab[col].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))        
                
        return tab

    def __str__(self):
        return str(self._views)
    
    def __add__(self, other):
        # TODO: Implementar a adição de arquivos
        return NotImplemented
        
        
class ArquivoDigitalExportException(Exception):
    pass

    


    

    

    
    
    
    
            

