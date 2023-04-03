"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Members
from api.utils import generate_sitemap, APIException
import json
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Blueprint('api', __name__)

#  GET MEMBERS
@api.route('/members', methods=['GET'])
def getMembers():
    callMembers = Members.query.all() #Llama todos los elementos de la lista
    result = [element.serialize() for element in callMembers] #Crea una lista de elementos json()

    response_body = {
        'msg: ': 'Peticion correcta',
        'result: ': result
    }
    return jsonify(response_body), 200

#  GET MEMBERS ID
@api.route('/members/<int:members_id>', methods=['GET'])
def get_members_id(members_id):
    call_member = Members.query.get(members_id) #Llama el elemento de la lista
    result = call_member.serialize() # Convierte a json()

    response_body = {
        'msg: ': 'Peticion correcta',
        'result: ': result
    }
    return jsonify(response_body), 200

#  ADD MEMBER
@api.route('/signup', methods=['POST'])
def create_member():
    name = request.json.get("name", None) #Agregar los valores al cuerpo de la peticion
    last_name = request.json.get("last_name", None)  #Agregar los valores al cuerpo de la peticion
    age = request.json.get("age", None)  #Agregar los valores al cuerpo de la peticion


    user_already_exist = Members.query.filter_by(name = name).filter_by(last_name=last_name).filter_by(age=age).first() #Comprobar si el valor ya existe en la base de datos
    if user_already_exist:
        return jsonify({'msg': 'El usuario ya existe'}), 401
    
    else:
        new_member = Members(name=name, last_name=last_name, age=age)
        db.session.add(new_member)
        db.session.commit()
    
        response_body = {
            'msg: ' : 'Member agregado', 
            'member': new_member.serialize()
            }
        
        return jsonify(response_body), 200


# DELETE MEMBER
@api.route('/members/<int:member_id>', methods= ['DELETE'])
def deleteMember(member_id):
    delete_Member = Members.query.get(member_id)
    db.session.delete(delete_Member)
    db.session.commit()

    response_body = {
            'msg: ' : 'Member borrado', 
            'member': delete_Member.serialize()
            }
    return jsonify(response_body)


# LOGIN
@api.route('/login', methods=['POST'])
def login():
    name = request.json.get("name", None)
    last_name = request.json.get("last_name", None)
    age = request.json.get("age", None)
    

    member = Members.query.filter_by(name=name).filter_by(last_name=last_name).filter_by(age=age).first()

    if member == None:
        return jsonify({"msg": "Member Not exist!"}), 401
    
    access_token = create_access_token(identity=member.id)

    response_body = {
        "msg": "Token create",
        "token": access_token
    }

    return jsonify(response_body), 201 

# TOKEN
@api.route("/private", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    response_body= {
        "msg": "Permiso concedido",
        "correcto": True,
        "Usuario": get_jwt_identity()
    }
    return jsonify(response_body), 200


