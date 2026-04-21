# PurplePincher Worker

Cloudflare Worker implementing **The Lock** — iterative reasoning enhancement for any agent.

## Quick Deploy

```bash
# 1. Install & login
npm install -g wrangler
wrangler login

# 2. Create resources
wrangler d1 create purplepincher-db
# → copy database_id into wrangler.toml

wrangler vectorize create purplepincher-embeddings --dimensions 1536 --metric cosine
wrangler r2 bucket create purplepincher-artifacts
wrangler kv namespace create CACHE
# → copy id into wrangler.toml

# 3. Init schema
wrangler d1 execute purplepincher-db --file=./schema.sql

# 4. Deploy
wrangler deploy
```

Your API is live at `https://purplepincher.<subdomain>.workers.dev`

## API

### Start a session
```
GET /start?agent=NAME&query=PROBLEM&strategy=STRATEGY&rounds=N
```
Returns `{ sessionId, round: 1, prompt }`

### Get current round prompt
```
GET /round?session=ID
```
Returns `{ round, prompt }`

### Submit response
```
GET /respond?session=ID&response=ANSWER
```
Returns `{ round, feedback, nextPrompt?, complete }`

### Get final result
```
GET /result?session=ID
```
Returns `{ sessionId, query, strategy, rounds: [...], summary }`

### List sessions
```
GET /sessions?agent=NAME
```
Returns `{ sessions: [...] }`

## Strategies

| Strategy | Best For |
|----------|----------|
| socratic | General improvement |
| adversarial | Stress-testing designs |
| decomposition | Complex multi-part problems |
| perspective | Balanced analysis |
| iterative_design | Architecture/design |
| debug | Code reviews, analysis |
| compression | Concise communication |
| playground | Creative exploration |

## Neuron Budget

- Free tier: ~10,000 neurons/day
- 1 round ≈ 1,200 neurons (Llama 3.2 1B)
- 5-round session ≈ 6,000 neurons → 1-2 free sessions/day
- Paid ($5/mo): ~$1.32/day for 100 sessions

## Resources

- **D1** — sessions, rounds, tiles
- **Workers AI** — feedback generation
- **Vectorize** — tile embeddings (future)
- **R2** — artifact storage (future)
- **KV** — session cache
