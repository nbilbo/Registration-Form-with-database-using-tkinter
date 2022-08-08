import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
DB_NAME = os.path.join(BASE_DIR, 'database.db')
COMPUTING_IMG = os.path.join(ASSETS_DIR, 'computing.png')
DATABASE_IMG = os.path.join(ASSETS_DIR, 'database.png')
