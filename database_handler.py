import os
import pymongo
from typing import Union
from dotenv import load_dotenv
from pymongo import ASCENDING
from urllib.parse import quote_plus


class DatabaseConnectionError(Exception):
    pass


load_dotenv()
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
MONGODB_IP_AND_PORT = os.getenv("MONGODB_IP_AND_PORT")
MONGODB_STRING = os.getenv("MONGODB_STRING")

# Connect with mongodb string
if MONGODB_STRING:
    db_client = pymongo.MongoClient(MONGODB_STRING)

# Connect if server doesn't have mongodb users with passwords
elif MONGODB_IP_AND_PORT and not MONGODB_USERNAME and not MONGODB_PASSWORD:
    db_client = pymongo.MongoClient(f"mongodb://{MONGODB_IP_AND_PORT}/")

# Connect with username and password
elif MONGODB_IP_AND_PORT and MONGODB_USERNAME and MONGODB_PASSWORD:
    MONGODB_USERNAME = quote_plus(MONGODB_USERNAME)
    MONGODB_PASSWORD = quote_plus(MONGODB_PASSWORD)
    db_client = pymongo.MongoClient(f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_IP_AND_PORT}/")

else:
    raise DatabaseConnectionError("Missing database username, password, ip or atlas string from env")

db = db_client["DiscordBot"]
COLLECTION_NAME = "servers"

# Create collection if not exists
if COLLECTION_NAME not in db.list_collection_names():
    db.create_collection(COLLECTION_NAME)

servers_collection = db[COLLECTION_NAME]
servers_collection.create_index([("guild_id", ASCENDING), ("name", ASCENDING)], unique=True)


def create_default_config(guild_id: int) -> bool:
    """Create default configuration for server in database"""
    if not find_discord_server(guild_id):
        default_config = {
            "guild_id": guild_id,
            "servers": {}
        }

        insert = servers_collection.insert_one(default_config)

        return insert.acknowledged

    else:
        return False


def find_discord_server(guild_id: int) -> Union[dict, None]:
    """Find discord server in database"""
    server_exists = servers_collection.find_one({"guild_id": guild_id})

    return server_exists


def find_game_server(guild_id: int, game_server_name: str) -> Union[dict, None]:
    """Find game server in database"""
    try:
        discord_server = servers_collection.find_one({"guild_id": guild_id}, {"_id": 0})
        game_server = discord_server["servers"][game_server_name]

        return game_server

    except (KeyError, TypeError):
        return None


def all_game_servers(guild_id: int) -> Union[list, None]:
    """List of all game servers in database"""
    try:
        discord_server = servers_collection.find_one({"guild_id": guild_id}, {"_id": 0})
        game_servers = list(discord_server["servers"].keys())

        return game_servers

    except TypeError:
        return None


def add_game_server(guild_id: int, server_name: str, ip: str, port: int, description: str) -> bool:
    """Add game server to the database"""
    new_server = {
        "ip": ip,
        "port": port,
        "description": description
    }

    query = {"guild_id": guild_id}
    update = {"$set": {f"servers.{server_name}": new_server}}
    result = servers_collection.update_one(query, update)

    return result.acknowledged


def del_game_server(guild_id: int, server_name: str) -> bool:
    """Delete game server from database"""
    server_exists = find_game_server(guild_id, server_name)

    if server_exists:
        query = {"guild_id": guild_id}
        update = {"$unset": {f"servers.{server_name}": 1}}
        result = servers_collection.update_one(query, update)

        return result.acknowledged

    else:
        return False
