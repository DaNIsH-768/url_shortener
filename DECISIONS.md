## Authentication approach
Approach: JWT-based authentication for a stateless API
Why: I wanted auth that felt simple and practical for a small backend without managing server-side sessions
Why bcrypt: password hashing is intentionally slow, which makes brute-force attacks harder
Tradeoff: I kept it lightweight instead of adding refresh tokens or a more complex auth system

## Data model choices
Model: separate tables for users, URLs, and clicks
Why: it keeps ownership and analytics concerns clean instead of forcing everything into one table
Why foreign keys: they make the relationships explicit and help keep the data model understandable

## Short link generation
Approach: generate a random 7-character base62 short code and check for collisions before insert
Why random over sequential IDs: random codes avoid leaking how many links have been created and make URLs feel less predictable
Why collision check: if the generated code already exists, I generate a new one rather than silently overwriting anything
Why this approach: it keeps the system simple while still being safe and practical for a small service

## Testing strategy
Approach: use SQLite for tests and inject the database session dependency so the app can be tested without touching the real database
Why SQLite: it is fast, lightweight, and makes tests easy to run locally and in CI
Why dependency injection mattered: it let me isolate the API layer and test behavior without wiring up a full production database for each test
Why test authorisation separately: I wanted to make the 403 vs 404 distinction explicit, so the tests clearly show that a user without access is rejected differently from a resource that simply does not exist

## Stack choice
Stack: FastAPI, SQLModel, PostgreSQL, and Redis
Why: this gave me a good balance between speed, clarity, and learning value
Why not over-engineer: I wanted to build something that worked well, was easy to explain, and could be extended later if needed

## API design
Approach: keep the API small and explicit with separate auth and URL routes
Why: it makes the project easier to test, reason about, and talk through in interviews
Why this mattered to me: I wanted the app to feel like a real backend service, not just a collection of endpoints

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