import redis
import json
from redis.asyncio import Redis, ConnectionPool

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
redis_async = Redis.from_url("redis://localhost:6379", decode_responses=True)
# decode_responses=True → returns str instead of bytes everywhere

# Test connection
print(r.ping())  # True

#Connection pool - sync and async
r_connection_pool = redis.ConnectionPool.from_url("redis://localhost:6379", decode_responses=True)
r_async_connection_pool = ConnectionPool.from_url("redis://localhost:6379", decode_responses=True)


#set and get values
set_result = r.set("my_key", "my_value")
get_result = r.get("my_key")
print(f"Set result: {set_result}, Get result: {get_result}")  # Set result: True, Get result: my_value

delete_result = r.delete("my_key")
print(f"Delete result: {delete_result}")  # Delete result: 1
print(f"Get after delete: {r.get('my_key')}, {r.exists('my_key')}")  # Get after delete: None


# TTL and persist
set_ttl = r.set("temp_key", "temp_value", ex=10)  # Set with TTL of 10 seconds
print(f"Set with TTL result: {set_ttl}, TTL: {r.ttl('temp_key')}")  # Set with TTL result: True, TTL: 10
persist_result = r.persist("temp_key")
print(f"Persist result: {persist_result}, TTL after persist: {r.ttl('temp_key')}")  # Persist result: True, TTL after persist: -1


# HASH OPERATIONS - get, set, delete
set_job_hash = r.hset("job:1", mapping={"title": "Software Engineer", "company": "TechCorp", "location": "Remote"})
set_job_hash2 = r.hset("job:2", mapping={"title": "Electrical Engineer", 'company': "BHEL"})
get_job_hash = r.hget("job:1", "title")
print(get_job_hash)
get_all_job_hash = r.hgetall("job:1")
print(f"Getting all data of job:1 - {get_all_job_hash}")
delete_key_hash = r.hdel("job:1", "location")
after_delete_location = r.hgetall("job:1")
print(f"After deleting location - {after_delete_location}")

# STREAM OPERATIONS
# XADD, XREAD - Append entry and read from a stream
stream_key = "mystream"
stream_key_v2 = "mystream_v2"
add_stream_data = r.xadd(stream_key, {"name": "John", "age": 26}, )
add_stream_data = r.xadd(stream_key, {"name": "Jaffrin", "age": 25})
get_data = r.xread({stream_key: "0-0"})
get_data_v2 = r.xread({stream_key_v2: "0-0"})
print(f"Stream data: {get_data}")
print(f"Stream data V2: {get_data_v2}")

#XCREATE_GROUP, XREADGROUP - Create a consumer group and read from it
group_name = "mygroup"
try:
    r.xgroup_create(stream_key, group_name, id='0-0')
except redis.exceptions.ResponseError as e:
    if 'BUSYGROUP' in str(e):
        print(f"Group '{group_name}' already exists.")
        pass
    else:
        print(f"Group creation error: {e}")

print("Length of the stream data", r.xlen(stream_key))
results = r.xreadgroup(group_name, "consumer1", streams={stream_key: "0"}, count=100)
print(f"XREADGROUP results: {results}")


# Parse entries
if results:
    stream_name, entries = results[0]
    print(stream_name, entries, "stream name and entries")
    for entry_id, data in entries:
        user_name = data['name']
        user_age = data['age']
        print(user_name, user_age, "user name and age")

        r.xack(stream_key, group_name, entry_id)  # Acknowledge the message
        r.xdel(stream_key, entry_id)
        print("Length of the stream data", r.xlen(stream_key))


# Delete Stream
r.delete(stream_key)
r.delete(stream_key_v2)