## Redis caching strategy
Pattern: Cache-aside
Cached: short_code → {original_url, url_id} as Redis hash
TTL: 3600 seconds (1 hour)
Why store url_id: needed for click tracking on cache hits — 
without it we'd need a DB query anyway, defeating the cache purpose
Why cache-aside over write-through: simpler, good enough for read-heavy workload

## Rate limiting
Applied to: GET /{code} redirect endpoint only
Limit: 5 requests/minute per IP
Why 5: accounts for multi-device access and retries
why not auth endpoints: brute force on login is handled 
separately by bcrypt's slow hashing
Tool: slowapi (wraps Redis counter pattern)