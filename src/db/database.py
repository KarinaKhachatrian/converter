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

    def create_second_level_contents(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS second_level_contents(
        second_content_id SERIAL PRIMARY KEY,
        second_header TEXT NOT NULL,
        content TEXT,
        filename TEXT);""")
        self.conn.commit()

    def create_third_level_contents(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS third_level_contents(
        third_content_id SERIAL PRIMARY KEY,
        third_header TEXT NOT NULL,
        content TEXT,
        filename TEXT);""")
        self.conn.commit()

    def create_users_second_level_content(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users_second_level_content(
        user_second_level_id SERIAL PRIMARY KEY,
        user_id INT NOT NULL REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE,
        second_content_id INT NOT NULL REFERENCES second_level_contents (second_content_id) ON DELETE CASCADE ON UPDATE CASCADE
        );""")
        self.conn.commit()

    def create_users_third_level_content(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users_third_level_content(
        user_third_level_id SERIAL PRIMARY KEY,
        user_id INT NOT NULL REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE,
        third_content_id INT NOT NULL REFERENCES third_level_contents (third_content_id) ON DELETE CASCADE ON UPDATE CASCADE
        );""")
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

    def select_second_content_id(self, second_header):
        self.cur.execute("""SELECT second_content_id FROM second_level_contents WHERE second_header = %s;""", (second_header,))
        return self.cur.fetchone()[0]

    def select_third_content_id(self, third_header):
        self.cur.execute("""SELECT third_content_id FROM third_level_contents WHERE third_header = %s;""", (third_header,))
        return self.cur.fetchone()[0]

    def select_filenames(self, user_id):
        self.cur.execute("""SELECT DISTINCT sc.filename 
                        FROM second_level_contents AS sc
                        JOIN users_second_level_content AS usc
                        ON usc.second_content_id = sc.second_content_id
                        WHERE usc.user_id = %s;""", (user_id,))
        return [row[0].strip() for row in self.cur.fetchall()]

    def select_second_level_headers(self, filename):
        self.cur.execute("""SELECT second_header 
                        FROM second_level_contents
                        WHERE filename = %s;""", (filename,))
        return [row[0].strip() for row in self.cur.fetchall()]

    def select_third_level_headers(self, filename):
        self.cur.execute("""SELECT third_header 
                        FROM third_level_contents
                        WHERE filename = %s;""", (filename,))
        return [row[0].strip() for row in self.cur.fetchall()]

    def select_second_level_content(self, second_header, filename):
        self.cur.execute("""SELECT content FROM second_level_contents
                        WHERE second_header = %s 
                        AND filename = %s;""", (second_header, filename,))
        return self.cur.fetchone()[0]

    def select_third_level_content(self, third_header, filename):
        self.cur.execute("""SELECT content FROM third_level_contents
                        WHERE third_header = %s 
                        AND filename = %s;""", (third_header, filename,))
        return self.cur.fetchone()[0]

    def check_credentials(self, email, password) -> bool:
        self.cur.execute("""
                SELECT * FROM users 
                WHERE email = %s AND password = %s;
            """, (email, password))
        return self.cur.fetchone() is not None

    def check_user_exists(self, email) -> bool:
        self.cur.execute("""
        SELECT 1 FROM users WHERE email = %s;""", (email,))
        return self.cur.fetchone() is not None


    def insert_second_level_content(self, second_header, content, filename):
        self.cur.execute("""INSERT INTO second_level_contents(
                            second_header, 
                            content,
                            filename) 
                            VALUES (%s, %s, %s);""", (second_header, content, filename))
        self.conn.commit()

    def insert_third_level_content(self, second_header, content, filename):
        self.cur.execute("""INSERT INTO third_level_contents(
                            third_header, 
                            content,
                            filename) 
                            VALUES (%s, %s, %s);""", (second_header, content, filename))
        self.conn.commit()

    def insert_users_second_level_content(self, user_id, second_content_id):
        self.cur.execute("""INSERT INTO users_second_level_content(
                                user_id,
                                second_content_id) VALUES (%s, %s);""",
                         (user_id, second_content_id))

    def insert_users_third_level_content(self, user_id, third_content_id):
        self.cur.execute("""INSERT INTO users_third_level_content(
                                user_id,
                                third_content_id) VALUES (%s, %s);""",
                         (user_id, third_content_id))

    def drop_departments(self):
        self.cur.execute("""DROP TABLE IF EXISTS departments CASCADE;""")
        self.conn.commit()

    def drop_users(self):
        self.cur.execute("""DROP TABLE IF EXISTS users CASCADE;""")
        self.conn.commit()

    def drop_users_departments(self):
        self.cur.execute("""DROP TABLE IF EXISTS users_departments CASCADE;""")
        self.conn.commit()

    def drop_second_level_contents(self):
        self.cur.execute("""DROP TABLE IF EXISTS second_level_contents CASCADE;""")
        self.conn.commit()

    def drop_third_level_contents(self):
        self.cur.execute("""DROP TABLE IF EXISTS third_level_contents CASCADE;""")
        self.conn.commit()

    def drop_users_second_level_contents(self):
        self.cur.execute("""DROP TABLE IF EXISTS users_second_level_content CASCADE;""")
        self.conn.commit()

    def drop_users_third_level_contents(self):
        self.cur.execute("""DROP TABLE IF EXISTS users_third_level_content CASCADE;""")
        self.conn.commit()

# db = Database(
#             dbname="rls",
#             user="postgres",
#             password="postgres",
#             host="localhost"
#         )
#
# s = db.check_user_exists(
#     'test@test.com'
# )
#
# print(s)