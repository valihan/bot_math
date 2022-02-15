import sqlite3

class cl_db:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def user_exists(self, iv_user_id ):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (iv_user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, iv_user_id):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (iv_user_id,))
        return result.fetchone()[0]

    def add_user(self, iv_user_id, iv_first_name):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO `users` (`user_id`,`first_name`) VALUES (?,?)", (iv_user_id, iv_first_name))
        return self.conn.commit()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()