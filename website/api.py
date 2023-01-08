from flask import Blueprint, request, jsonify
from . import db
from .models import User

api = Blueprint('api', __name__)

@api.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(name=data['first_name'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id}), 201

@api.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({'id': user.id, 'first_name': user.first_name, 'email': user.email})

@api.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    user.first_name = data['first_name']
    user.email = data['email']
    db.session.commit()
    return jsonify({'id': user.id, 'first_name': user.first_name, 'email': user.email}), 200
    


@api.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return "User with id {} deleted successfully".format(id)
    else:
        return "User with id {} not found".format(id)