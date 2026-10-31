import redis
import time
import json

from app.schemas import UserCreate, UserResponse, UserUpdate

client = redis.Redis(
    host="localhost",
    port=63790,
    decode_responses=True
)
#
# data = {
#     'id': 1,
#     'username': 'Alex',
#     'age': 20
# }
# json_data = json.dumps(data)
# client.set("user:1001", json_data, ex=30)
# data = client.get("user:1001")
# data = json.loads(data)
# print(data)
# print(type(data))
# user_response = UserResponse(id=data["id"], username=data["username"], age=data["age"])
# print(user_response)
# print(type(user_response))

client.set("username", "tom")
client.delete("key")


def delete_user_cache(user_id):
    key = f"user:{user_id}"
    client = get_client()
    delete_status = delete_user_sql(user_id=user_id)
    client.delete(key)
    return delete_status
