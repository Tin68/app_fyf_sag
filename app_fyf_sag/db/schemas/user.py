### transforma lo obtenido en la base de datos en un USUARIO en formato json ###
def user_schema(user) -> dict:
    return {"id": str(user["_id"]),
            "username" : user["username"],
            "surname" : user["surname"],            
            "rol" : user["rol"],
            "disabled" : user["disabled"],
            "password" : user["password"]}

def users_schema(users) -> list:
    return [user_schema(user) for user in users]