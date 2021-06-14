import sqlite3


class DBConnection:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(DBConnection)
            return cls.instance
        return cls.instance

    def __init__(self, db_name='Links.db'):
        self.name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_pages_links_table(self):
        self.cursor.execute('''CREATE TABLE pages_links(link TEXT, page_number )''')
        self.conn.commit()

    def create_items_table(self):
        self.cursor.execute('''CREATE TABLE items(link TEXT, name TEXT, price TEXT)''')
        self.conn.commit()

    def delete_pages_links_table(self):
        self.cursor.execute('''DROP TABLE pages_links''')
        self.conn.commit()

    def delete_items_table(self):
        self.cursor.execute('''DROP TABLE items''')
        self.conn.commit()

    def insert_item_links(self, data):
        for record in data:
            self.cursor.execute('''INSERT INTO items (link, name, price) VALUES (?,?,?)''',
                                (record[0], record[1], record[2]))
        self.conn.commit()

    def select_items(self):
        self.cursor.execute('''SELECT * FROM items''')
        return self.cursor.fetchall()

    def __del__(self):
        self.cursor.close()
        self.conn.close()
