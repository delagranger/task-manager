from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

class DBManager:
    def __init__(self):
        self.conn = self._create_connection()
        self._create_tables()
        self._insert_default_group()
        self.conn.close() # закрывает соединение с БД
    
    def _create_connection(self): # возвращает объект Соединения с postgreSQL
        connection = psycopg2.connect(dbname=os.getenv("DB_NAME"),
                                      user=os.getenv("DB_USER"),
                                      password=os.getenv("DB_PASSWORD"),
                                      host=os.getenv("DB_HOST"),
                                      port=os.getenv("DB_PORT"),
        )
        return connection

    def _create_tables(self):
        with self.conn.cursor() as cur: # создает объект курсора; курсор - инструмент для выполнения SQL-запросов
            # метод, отправляющий и исполняющий SQL-запрос в БД
            cur.execute("""
                        CREATE TABLE IF NOT EXISTS groups (
                            id SERIAL PRIMARY KEY,
                            title VARCHAR(50) NOT NULL UNIQUE
                        );
                        CREATE TABLE IF NOT EXISTS tasks (
                            id SERIAL PRIMARY KEY,
                            title VARCHAR(50) NOT NULL,
                            status VARCHAR(25) NOT NULL DEFAULT 'active',
                            group_id INTEGER REFERENCES groups(id) ON DELETE SET NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
                        );
            """)
            self.conn.commit() # фиксация изменений в БД
    
    def _insert_default_group(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                        INSERT INTO groups (title) 
                        SELECT 'default group'
                        WHERE NOT EXISTS (SELECT 1 FROM groups WHERE title = 'default group');
            """)
            self.conn.commit()