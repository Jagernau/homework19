from flask import request, abort
from flask_restx import Resource, Namespace

from .helpers import auth_required, admin_required
from dao.model.user import UserSchema
from implemented import user_service

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        all_users = user_service.get_all()
        res = UserSchema(many=True).dump(all_users)
        return res, 200


#    @admin_required
    def post(self):
        req_json = request.json
        user = user_service.create(req_json)
        return "", 201, {"location": f"/movies/{user.id}"}



@user_ns.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid):
        u = user_service.get_one(uid)
        su_d = UserSchema().dump(u)
        return su_d, 200


    def put(self, uid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = uid
        user_service.update(req_json)
        return "", 204


    @auth_required
    @admin_required
    def delete(self, uid):
        user_service.delete(uid)
        return "", 204
