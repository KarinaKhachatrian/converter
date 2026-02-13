import psycopg2

class Database:
    def __init__(self, dbname: str, user: str, password: str, host: str):
        self.conn = psycopg2.connect(dbname=dbname,
                                     user=user,
                                     password=password,
                                     host=host)
        self.cur = self.conn.cursor()

    def create_departments(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS departments(
        department_id SERIAL PRIMARY KEY, 
        department_name TEXT NOT NULL);""")
        self.conn.commit()

    def create_users(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
        user_id SERIAL PRIMARY KEY,
        lastname TEXT NOT NULL,
        firstname TEXT NOT NULL,
        patronymic TEXT,
        email VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(64) NOT NULL);""")
        self.conn.commit()

    def create_users_departments(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users_departments (
        user_id INT NOT NULL REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE,
        department_id INT NOT NULL REFERENCES departments (department_id) ON DELETE CASCADE ON UPDATE CASCADE);""")
        self.conn.commit()

db = Database(
    dbname="rls",
    user="postgres",
    password="postgres",
    host="localhost"
)

db.create_departments()
db.create_users()
db.create_users_departments()