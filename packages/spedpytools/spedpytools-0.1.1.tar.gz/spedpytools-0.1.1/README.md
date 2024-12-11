# SPED para python

Biblioteca para visualização de um arquivo sped em estrutura de tabelas do Pandas e possibilidade de salvar em formato para excel.
Utiliza o relacionamento hierarquico típico da estrutura do SPED FISCAL (EFD, ECD e entre outros)

A ideia seria visualizar em formato de tabela todas as informações de um registro e seus registros pais, por exemplo:

	from spedpytools import spedpytools
	
    arq = spedpytools.EFDFile()
    arq.readfile("efd.txt")
    arq.to_excel("output.xlsx")

## Requisitos

- spedpy
- pandas

## Como instalar

    $ pip install spedpytools