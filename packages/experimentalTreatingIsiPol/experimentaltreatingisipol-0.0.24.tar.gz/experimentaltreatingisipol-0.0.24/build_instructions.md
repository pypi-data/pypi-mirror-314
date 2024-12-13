# Passos para gerar o build

- Criar uma pasta dentro de src, com o nome do package

## Configurar arquivo .toml

- Apagar (se houver), a pasta dist
- Desenvolder todo o projeto na pasta acima
- Alterar o nome do projeto no arquivo pyproject.toml
- Modificar o número de versão
- Conferir o tipo de licença
- Configurar as urls (opicional)

## Gerar os arquivos da distribuição
Primeiro instalar:
'''
py -m pip install --upgrade build
'''
Depois:

'''
py -m build
'''

## Fazer upload dos arquivos de distribuição

'''
py -m pip install --upgrade twine
'''

'''
py -m twine upload --repository pypi dist/*
'''

Obs.: É necessário gerar o token. Para assar o token, só colar cliando com o botão direito


# Utilizando o package

Instalar a biblioteca:
'''
pip install experimentalTreatingIsiPol
'''

Depois só importar:

'''
import experimentalTreatingIsiPol as expIsi
'''




