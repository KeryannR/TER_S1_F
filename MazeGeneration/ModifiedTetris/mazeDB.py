from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi

CONNECTION_STRING = "mongodb+srv://pacmaz_user:9c2URk5VXXpQG5X8@maze.t1in5bv.mongodb.net/?appName=Maze"

def insert_maze(json_data):
    if not isinstance(json_data, dict):
        raise ValueError("Le paramètre doit être un dictionnaire JSON valide.")
    try:
        client = MongoClient(CONNECTION_STRING, server_api=ServerApi('1'))
        db = client["Mazes"]
        collection = db["maze"]

        result = collection.insert_one(json_data)
        print(f"Document inséré avec _id : {result.inserted_id}")
        return str(result.inserted_id)

    except errors.ServerSelectionTimeoutError:
        print("Impossible de se connecter à MongoDB (timeout)")
    except errors.OperationFailure as e:
        print(f"Erreur d'authentification ou d'accès : {e}")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
    finally:
        client.close()
