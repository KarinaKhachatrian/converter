from src.db.database import Database

db = Database(
    dbname="rls",
    user="postgres",
    password="postgres",
    host="localhost"
)

departments = db.select_departments()