from dao.model.user import User
from flask import abort


class UserDAO:
    def __init__(self, session):
        """иниц. принимает и сохраняет динамич.сессию"""
        self.session = session


    def get_one(self, uid):
        """Получить одного поль. по id: uid"""
        return self.session.query(User).get(uid)

    
    def get_all(self):
        """Получить юзеров"""
        return self.session.query(User).all()



    def get_user_by_username(self, username):
        """Получить поль. по имени"""
        return self.session.query(User).filter(User.username == username).first()


    def create(self, user):
        """Полностью создать поль. принимает json: user кварг"""
        ent = User(**user)
        self.session.add(ent)
        self.session.commit()
        return ent #отдаёт то что принемает


    def delete(self, uid):
        """Удалить поль. по id: uid"""
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()
       

    def update(self, user_d):
        """Обновить поль. """
        user = self.get_one(user_d.get("id"))
        user.username = user_d.get("username")
        user.password = user_d.get("password")
        user.role = user_d.get("role")

        self.session.add(user)
        self.session.commit()
