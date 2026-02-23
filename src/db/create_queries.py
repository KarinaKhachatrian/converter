from src.db.database import Database

db = Database(
    dbname="rls",
    user="postgres",
    password="postgres",
    host="localhost"
)

db.create_departments()
db.create_users()
db.create_users_departments()