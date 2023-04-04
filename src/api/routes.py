"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Members, Favorites
from api.utils import generate_sitemap, APIException
import json
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Blueprint('api', __name__)

@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all() 
    result = [element.serialize() for element in users] 

    response_body = {
        'result: ': result
    }
    return jsonify(response_body), 200


#  GET MEMBERS
@api.route('/members', methods=['GET'])
def getMembers():
    callMembers = Members.query.all() #Llama todos los elementos de la lista
    result = [element.serialize() for element in callMembers] #Crea una lista de elementos json()

    response_body = {
        'result': result
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


# GET DE TODOS LOS USUARIOS CON SUS FAVORITOS RELACIONADOS
#Crear una llamada de todos los favoritos
@api.route('/users/favorites', methods=['GET'])
def get_favorite():
    favorite = Favorites.query.all() 
    result = [element.serialize() for element in favorite] 

    response_body = {
        'msg: ': 'Peticion correcta',
        'result: ': result
    }
    return jsonify(response_body), 200



# AGREGAR FAVORITOS AL USUARIO
@api.route('/users/<int:user_id>/favorites', methods=['POST'])
def add_favorite_members(user_id):
    #Obtener los datos del favorito
    members_id = request.json.get("members_id", None)
    #Buscar el usuario en la base de datos
    user = User.query.get(user_id)# Parametro recibido por el front
    if user is None:
        return jsonify({'msg: ': 'Usuario no encontrado'})
    
    favorite = Favorites(user_id=user_id, members_id=members_id) #El member se rellenara en el front-end
    db.session.add(favorite)
    db.session.commit()

    # Obtener la lista actualizada de favoritos del usuario
    user_favorites = Favorites.query.filter_by(user_id=user_id).all()
    all_members_favorites = [element.serialize() for element in user_favorites]

    response_body = {
        'msg: ': 'Favorito agregado',
        'Favoritos': all_members_favorites
    }
    # Devolver la lista de favoritos actualizada como respuesta
    return jsonify(response_body)

#VER SOLO LOS FAVORITOS DE 1 USUARIO
@api.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    # Buscar el usuario en la base de datos
    user = User.query.get(user_id)
    if user is None:
        # Si el usuario no existe, devolver un error 404
        return jsonify({"error": "User not found"}), 404

    # Obtener la lista de favoritos del usuario
    user_favorites = Favorites.query.filter_by(user_id=user.id).all()
    all_members_favorites = [f.serialize() for f in user_favorites]

    response_body = {
        'Favoritos': all_members_favorites
    }
    # Devolver la lista de favoritos como respuesta
    return jsonify(response_body)


# VER LA INFORMACION DE LOS FAVORITOS DEL USUARIO
#Buscar el miembro especifico a traves del usuario
@api.route('/users/<int:user_id>/favorites/<int:members_id>', methods=['GET'])
def get_favorite_member_details(user_id, members_id):
    # Buscar el usuario en la base de datos por su ID
    user = User.query.get(user_id)
    if user is None:
        # Si el usuario no existe, devolver un error 404
        return jsonify({"error": "User not found"}), 404

    # Buscar el miembro favorito del usuario por su ID
    favorite = Favorites.query.filter_by(user_id=user_id, members_id=members_id).first()
    if favorite is None:
        # Si el miembro no existe en la lista de favoritos del usuario, devolver un error 404
        return jsonify({"error": "Member not found in user's favorites"}), 404

    # Buscar los detalles del miembro en la base de datos por su ID
    members = Members.query.get(members_id)
    if members is None:
        # Si el miembro no existe, devolver un error 404
        return jsonify({"error": "Member not found"}), 404

    # Devolver los detalles del miembro como respuesta
    return jsonify(members.serialize())
