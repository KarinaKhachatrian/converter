from src.db.database import Database

db = Database(
    dbname="rls",
    user="postgres",
    password="postgres",
    host="localhost"
)

db.drop_departments()
db.drop_users()
db.drop_users_departments()
db.drop_second_level_contents()
db.drop_third_level_contents()
db.drop_users_second_level_contents()
db.drop_users_third_level_contents()