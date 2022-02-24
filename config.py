import os

USER = os.getenv('POSTGRES_USER', '')
PASSWORD = os.getenv('POSTGRES_PASSWORD', '')
DB = os.getenv('POSTGRES_DB', '')
DB_DSN = f'postgres://{USER}:{PASSWORD}@database:5432/{DB}'
SALT = 'Mmmd=sdfign834yjbd9bb'
