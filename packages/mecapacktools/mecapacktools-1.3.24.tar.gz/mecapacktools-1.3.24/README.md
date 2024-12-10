# Tools for Mecapack

La doc est disponible en Html ou en MD

## installation par pip

`pip install mecapacktools`

Installer les extensions :

`pip install mecapacktools[excel,sql,webservices]`

### Extensions diponibles :

- excel 
- Sql 
- WebServices 
- FTP 

## Notes pour le développement:

### Installation

`poetry install --with dev,docs --all-extras --sync`

### Génération de la doc

`poetry run .\make.bat html`
`poetry run .\make.bat markdown`

### Publier une nouvelle version

Changer la version :
Dans le fichier pyproject.toml modifier :
```
[tool.poetry]
version = "1.0.0"
 ```

Publier sur pypi `poetry publish --build`



