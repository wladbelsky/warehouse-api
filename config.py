import os
db_config = {
            "engine": "postgresql+asyncpg",
            "host": os.environ.get('DB_HOST'),
            "port": os.environ.get('DB_PORT'),
            "user": os.environ.get('DB_USER'),
            "password": os.environ.get('DB_PASSWORD'),
            "database": os.environ.get('DB_NAME'),
        }

jwt_secret = 'secret'