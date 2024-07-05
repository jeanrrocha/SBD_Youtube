### Banco de dados YouTube-like

## Como restaurar o banco de dados a partir do arquivo:

# OBS: é recomendado usar o arquivo I (método pelo pgAdmin4), visto que esse acompanha o presente texto
# OBS: pode-se utilizar o usuário "postgres" onde for mencionado *seu usuário*


1 - Certifique-se que possui os arquivos de backup:
(ou baixe de https://github.com/jeanrrocha/SBD_Youtube/releases/tag/v1.0.0)
	I - yt_backup.sql
	II - yt_backup (sem extensão)
	III - yt_backup.gz (versão compressa de II)

2 - Crie um banco de dados vazio com o nome youtube
- Pelo "pgAdmin4" é pelo diálogo em:
	Servers -> PostgreSQL 16 -> Databases --(botão direito)-> Create -> Database...
	-> Em "Database" coloque "youtube"
	-> Clique em "Save"
- Pelo terminal:
	createdb --username=*seu usuário* youtube
			
3 - Restaure o arquivo com um dos comandos:
	A - Se usando o arquivo I:
		-> Abra o "pgAdmin4"
		-> Entre no banco de dados criado em *2*
		-> Botão direito no banco e entre no diálogo "Restore..."
		-> Em "Filename" abra o explorador de arquivos e selecione o arquivo I
		-> Clique em "Restore"
		
		alternativamente, pelo terminal
		
		# OBS: substitua os campos entre ** por valores válidos
		-> Abra um terminal
		-> Digite "pg_restore --dbname=youtube --username=*seu usuário* *nome do arquivo I*"

	B - Se usando o arquivo II
		-> Abra um terminal
		-> Digite "psql --username=*seu usuário* youtube < *nome do arquivo II*"

	C - Se usando o arquivo III
		-> Abra um terminal
		-> Digite "gunzip -c *nome do arquivo III* | psql --username=*seu usuário* youtube"

## Como gerar os dados a partir do script:

#OBS: Certifique-se de que não possui nenhum banco de dados com o nome Youtube, visto que o script irá deletá-lo e gerar um novo no lugar.

1 - Certifique-se que possui os arquivos relevantes:
(ou baixe de https://github.com/jeanrrocha/SBD_Youtube)
- requirements.txt
- classes.py
- fake.py
- tables.sql
- triggers.sql

2 - Certifique-se que possui uma instalação válida de Python3 na sua variável PATH
	- Isso pode ser verificado no terminal executando "python --version" e verificando a versão

3 - Abra um terminal na mesma pasta dos arquivos mencionados em *1* e execute:
	- "pip install -r requirements.txt"
	- "python fake.py"
		- passe a senha do usuário "postgres" (pressionando enter apenas assume a senha padrão)
		- passe a porta (port) usada pelo serviço do postgres (pressionando enter apenas assume a porta padrão)

A geração de dados foi feita utilizando o pacote Faker disponível para python:
https://faker.readthedocs.io/en/master/