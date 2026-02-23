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
        password VARCHAR(255) NOT NULL);""")
        self.conn.commit()

    def create_users_departments(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users_departments (
        user_id INT NOT NULL REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE,
        department_id INT NOT NULL REFERENCES departments (department_id) ON DELETE CASCADE ON UPDATE CASCADE);""")
        self.conn.commit()

    def insert_departments(self):
        self.cur.execute("""INSERT INTO departments(department_name) VALUES
        ('Отдел IT'),
        ('Отдел менеджеров'),
        ('Отдел HR'),
        ('Отдел библиомед'),
        ('Отдел администрации');""")
        self.conn.commit()

    def insert_users(self, lastname, firstname, patronymic, email, password):
        self.cur.execute("""INSERT INTO users(lastname, firstname, patronymic, email, password) VALUES
        (%s, %s, %s, %s, %s);""",(lastname, firstname, patronymic, email, password))
        self.conn.commit()

    def insert_users_departments(self, user_id, department_id):
        self.cur.execute("""INSERT INTO users_departments(user_id, department_id) VALUES
        (%s, %s);""", (user_id, department_id))
        self.conn.commit()

    def select_departments(self):
        self.cur.execute("""SELECT department_name FROM departments;""")
        return [row[0] for row in self.cur.fetchall()]

    def select_department_id(self, department_name):
        self.cur.execute("""SELECT department_id FROM departments WHERE department_name = %s;""", (department_name,))
        return self.cur.fetchone()[0]

    def select_user_id(self, email):
        self.cur.execute("""SELECT user_id FROM users WHERE email = %s;""", (email,))
        return self.cur.fetchone()[0]

    def check_credentials(self, email, password):
        self.cur.execute("""
                SELECT * FROM users 
                WHERE email = %s AND password = %s;
            """, (email, password))
        return self.cur.fetchone() is not None
