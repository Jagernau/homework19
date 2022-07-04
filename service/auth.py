import calendar
import datetime
import jwt
from constants import SECRET_KEY, ALGORITM

from service.user import UserService

class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, username, password, is_refresh=False):
        user = self.user_service.get_user_by_username(username)

        if not user:
            return False

        if not is_refresh:
            if not self.user_service.compare_password(user.password, password):
                return False

        data = {"username": user.username, "role": user.role}


        # access token on 30 min
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITM)

        # refresh, 130 days

        day130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(day130.timetuple())
        refresh_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITM)

        return {"access_token": access_token, "refresh_token": refresh_token}


    def approve_refresf_token(self, refresh_token):
        data = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITM])
        username = data['username']
        user = self.user_service.get_user_by_username(username)

        if not user:
            return False
        now = calendar.timegm(datetime.datetime.utcnow().timetuple())
        expired = data['exp']
        if now > expired:
            return False
        return self.generate_tokens(username, user.password, is_refresh=True)


