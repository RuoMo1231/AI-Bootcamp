import redis

client = redis.Redis(
    host="localhost",
    port=63790,
    decode_responses=True
)

client.set("name", "AI-Bootcamp")

value = client.get("name")

print(value)
