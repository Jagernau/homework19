import base64
import hashlib
import hmac

from constants import PWD_HASH_ITERATIONS, PWD_HASH_SALT

from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao


    def get_one(self, uid):
        return self.dao.get_one(uid)


    def get_all(self):
        return self.dao.get_all() #доработать


    def get_user_by_username(self, username):
        return self.dao.get_user_by_username(username)


    def create(self, user_d):
        return self.dao.create(user_d)


    def update(self, user_d):
        self.dao.update(user_d)
        return self.dao


    def delete(self, uid):
        self.dao.delete(uid)


    def make_user_password_hash(self, password):
        return base64.b64decode(hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), PWD_HASH_SALT, PWD_HASH_ITERATIONS))


    def compare_password(self, password_hash, other_password) -> bool:
        return hmac.compare_digest(base64.b64decode(password_hash), hashlib.pbkdf2_hmac('sha256', other_password.encode('utf-8'), PWD_HASH_SALT, PWD_HASH_ITERATIONS))
