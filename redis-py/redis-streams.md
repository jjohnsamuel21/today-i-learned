# Redis Streams (redis-py)

This note captures what I learned while exploring **Redis Streams** using `redis-py`. The corresponding hands-on experiments are in `redis-hands-on.py`.

---

## 🧠 Background: Redis patterns I’ve used (Node.js)

Before exploring streams, I used Redis for:

- **Caching API responses**: populate/update cache after POST/PUT so GETs return fresh data.
- **Background jobs with Bull**: Redis as a queue (producer/consumer) for async tasks like sending emails.
  - Jobs are enqueued, then workers poll and process them.
  - Bull adds features such as `delay`, `attempts`, `backoff`, and `priority`.

---

## 🔥 Why Redis Streams?

Redis Streams are an **append-only log** designed for messaging and event streaming. Key benefits:

- ✅ Multiple consumers via **consumer groups**
- ✅ Persistent entries until explicitly deleted
- ✅ At-most-once delivery per group via **Pending Entry List (PEL)**
- ✅ Crash recovery / rebalancing via `XAUTOCLAIM` (idle entries can be moved to another consumer)

### Stream special IDs

| ID | Meaning |
| --- | --- |
| `>` | Entries not yet delivered to this consumer group |
| `0` | Start reading from the beginning of the stream |
| `$` | Only new entries arriving after now |

---

## 🧩 Core Redis Stream commands (redis-py)

### Common Redis commands (used alongside streams)

- `SET`, `MSET`, `GET`, `MGET` — basic key/value operations
- `HSET` — set fields on a hash (useful for job metadata)

### Stream-specific commands

- `XADD` — append an entry to a stream (enqueue a job)
- `XREAD` — read entries from a stream
- `XGROUP CREATE` — create a consumer group for a stream
- `XREADGROUP` — read entries as a member of a consumer group

### Acknowledgements & pending entries

When a consumer reads entries via `XREADGROUP`, those entries move into the group’s **Pending Entry List (PEL)**. The consumer must:

1. Process the entry
2. Call `XACK` to acknowledge completion

If the consumer crashes or never acknowledges, entries remain in PEL.

#### Recovery helpers

- `XAUTOCLAIM` — transfer pending entries idle longer than a threshold to another consumer
- `XPENDING` — inspect pending entries and metadata

### Additional stream utilities

- `XLEN` — count entries in a stream
- `XDEL` — delete specific entries
- `XINFO` — fetch metadata about a stream, consumer groups, and consumers

---

## 🚀 Redis pipelines (redis-py)

Pipelines batch commands to reduce round trips.

### Basic pipeline

```python
pipe = r.pipeline()
pipe.xadd('jobs:email', {'job_id': jid, 'payload': data})
pipe.hset(f'job:{jid}', mapping={'status': 'pending', 'retries': '0'})
pipe.expire(f'job:{jid}', 86400)  # 24h TTL
results = await pipe.execute()
# results: ['1700000000000-0', 1, True]
```

### Context manager pipeline

```python
async with r.pipeline() as pipe:
    pipe.hset(f'job:{jid}', 'status', 'done')
    pipe.hset(f'job:{jid}', 'result', json.dumps(result))
    await pipe.execute()
```

---

## ✅ Key takeaways

- Redis Streams are well-suited for **event-driven / job queue** patterns with persistence, multi-consumer support, and recovery guarantees.
- Consumer groups + PEL + acknowledgements are the foundation for reliable processing.
- `XAUTOCLAIM` enables smooth recovery when a consumer is stuck or fails.

---

> Tip: Keep `redis-hands-on.py` nearby for runnable examples and to iterate quickly on these concepts.
 