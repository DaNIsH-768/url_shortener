## Redis caching strategy
Pattern: Cache-aside
Cached: short_code → {original_url, url_id} as Redis hash
TTL: 3600 seconds (1 hour)
Why store url_id: needed for click tracking on cache hits — 
without it we'd need a DB query anyway, defeating the cache purpose
Why cache-aside over write-through: simpler, good enough for read-heavy workload