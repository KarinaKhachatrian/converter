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
db.create_second_level_contents()
db.create_third_level_contents()
db.create_users_second_level_content()
db.create_users_third_level_content()