# YourFuture

A student opportunity board — discover jobs, internships, volunteer roles, and
events, with a community forum and direct messaging. Listings are admin-curated;
each opportunity links out to the employer's own application page.

- **Frontend** (`frontend/`): React 19 + Vite + Tailwind single-page app.
- **Backend** (`backend/`): Flask JSON API backed by PostgreSQL.
- **Deploy**: a single Vercel project — the SPA is served statically and the
  Flask API runs as a Python serverless function under `/api/*` (same origin).

## Features

- Student registration and login (signed-cookie sessions).
- Browse and search jobs, internships/volunteer roles, and events.
- Save opportunities to a personal profile.
- Community forum and direct messaging between users.
- A protected **admin** page to create and remove listings.

## Architecture

```
repo/
├── frontend/            React + Vite SPA  (calls /api, same-origin)
│   └── src/lib/api.js    API base = VITE_API_URL ?? "/api"
├── backend/             Flask API
│   ├── app.py            app factory + blueprint registration
│   ├── blueprints/       auth, jobs, site (forum/messages/profile), admin
│   ├── db.py             psycopg2 via DATABASE_URL
│   ├── schema.sql        authoritative PostgreSQL schema
│   ├── seed.py           creates admin + sample listings
│   └── api/index.py      Vercel serverless entrypoint (exposes Flask `app`)
├── vercel.json          static SPA build + Python function + SPA fallback
├── requirements.txt     Python deps (used by Vercel)
└── .env.example         documented environment variables
```

## Local development

Requires Python 3.11+, Node 18+, and PostgreSQL.

1. **Configure env**: `cp .env.example .env` and fill in `SECRET_KEY`,
   `DATABASE_URL`, and `ADMIN_PASSWORD`.

2. **Database**:
   ```bash
   createdb yourfuture
   export $(grep -v '^#' .env | xargs)        # load .env into the shell
   psql "$DATABASE_URL" -f backend/schema.sql
   python backend/seed.py                      # creates the admin + samples
   ```

3. **Backend** (port 8000):
   ```bash
   cd backend
   python -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   flask run -p 8000        # or: python app.py
   ```

4. **Frontend** (port 5173): in another terminal:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Vite proxies `/api` → `http://localhost:8000`, so the SPA and API share an
   origin in dev. Visit http://localhost:5173, register a student, or log in
   with the seeded admin credentials and go to `/admin`.

## Deploying to Vercel

1. Provision a PostgreSQL database (e.g. **Neon** via the Vercel integration, or
   **Supabase**). Run `backend/schema.sql` against it, then `python backend/seed.py`
   with `DATABASE_URL`/`ADMIN_*` set.
2. Import the repo into Vercel. `vercel.json` already wires the SPA build and the
   Python function — no build settings needed.
3. Set environment variables in the Vercel dashboard:
   - `SECRET_KEY` — strong random value
   - `DATABASE_URL` — your Postgres connection string
   - `FLASK_ENV=production` — enables Secure cookies, disables dev CORS
4. Deploy. The SPA loads at `/`, the API answers at `/api/*` (same origin, so no
   CORS configuration is required).

## Database schema

The authoritative schema lives in [`backend/schema.sql`](backend/schema.sql).
Core tables: `users`, `jobs`, `unpaid`, `events`, `saved_opps`, `forum`,
`messages`, `experiences`.
