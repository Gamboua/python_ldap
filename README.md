## HOW TO

Criar environment
```bash
virtualenv .env
```

Iniciar environment
```bash
source .env/bin/activate
```

Instalar dependencias
```bash
pip install -r requirements.txt
```

Script para rodar csv, cadastrar no MongoDB e no LDAP
```bash
python import_csv.py
```

Rodar servidor flask
```bash
python run.py
```

## TODO
- Criar login
- Validar login do usuario
- Criar reset de senha