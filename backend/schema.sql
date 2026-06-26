-- YourFuture — authoritative PostgreSQL schema
-- Run once against a fresh database:  psql "$DATABASE_URL" -f schema.sql
-- Idempotent-ish: drops and recreates the app tables.

DROP TABLE IF EXISTS saved_opps     CASCADE;
DROP TABLE IF EXISTS experiences    CASCADE;
DROP TABLE IF EXISTS messages       CASCADE;
DROP TABLE IF EXISTS forum          CASCADE;
DROP TABLE IF EXISTS jobs           CASCADE;
DROP TABLE IF EXISTS unpaid         CASCADE;
DROP TABLE IF EXISTS events         CASCADE;
DROP TABLE IF EXISTS users          CASCADE;

-- ---------------------------------------------------------------------------
-- Users (students and admins). user_type: 'student' | 'admin'
-- ---------------------------------------------------------------------------
CREATE TABLE users (
    user_id        SERIAL PRIMARY KEY,
    username       TEXT NOT NULL UNIQUE,
    user_password  TEXT NOT NULL,
    user_type      TEXT NOT NULL DEFAULT 'student',
    user_org       TEXT,
    user_status    INTEGER NOT NULL DEFAULT 1,   -- 1 = active
    full_name      TEXT,
    profile_pic    TEXT,
    bio            TEXT,
    age            INTEGER,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------------
-- Opportunity listings (admin-curated). Each carries an external apply_url.
-- status columns: 1 = published/visible.
-- ---------------------------------------------------------------------------
CREATE TABLE jobs (
    job_id            SERIAL PRIMARY KEY,
    company           TEXT NOT NULL,
    company_role      TEXT NOT NULL,
    pay               TEXT,
    job_description   TEXT,
    job_location      TEXT,
    company_logo_url  TEXT,
    apply_url         TEXT NOT NULL,
    job_status        INTEGER NOT NULL DEFAULT 1,
    added_by          INTEGER REFERENCES users(user_id) ON DELETE SET NULL,
    date_added        TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE unpaid (
    unpaid_id        SERIAL PRIMARY KEY,
    organization     TEXT NOT NULL,
    unpaid_role      TEXT NOT NULL,
    unpaid_desc      TEXT,
    unpaid_location  TEXT,
    org_logo         TEXT,
    apply_url        TEXT NOT NULL,
    unpaid_status    INTEGER NOT NULL DEFAULT 1,
    added_by         INTEGER REFERENCES users(user_id) ON DELETE SET NULL,
    date_added       TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE events (
    event_id        SERIAL PRIMARY KEY,
    organization    TEXT NOT NULL,
    event_name      TEXT NOT NULL,
    event_desc      TEXT,
    event_location  TEXT,
    org_logo        TEXT,
    apply_url       TEXT NOT NULL,
    event_date      DATE,
    event_status    INTEGER NOT NULL DEFAULT 1,
    added_by        INTEGER REFERENCES users(user_id) ON DELETE SET NULL,
    date_added      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------------
-- Student-saved opportunities. opp_type: 'job' | 'unpaid' | 'event'
-- opp_key references the id within the matching listing table.
-- ---------------------------------------------------------------------------
CREATE TABLE saved_opps (
    id        SERIAL PRIMARY KEY,
    user_id   INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    opp_type  TEXT NOT NULL,
    opp_key   INTEGER NOT NULL,
    UNIQUE (user_id, opp_type, opp_key)
);

-- ---------------------------------------------------------------------------
-- Forum posts. post_status: 1 = visible.
-- ---------------------------------------------------------------------------
CREATE TABLE forum (
    post_id       SERIAL PRIMARY KEY,
    added_by      INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    post_content  TEXT NOT NULL,
    post_media    TEXT,
    post_status   INTEGER NOT NULL DEFAULT 1,
    post_time     TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------------
-- Direct messages between users.
-- ---------------------------------------------------------------------------
CREATE TABLE messages (
    msg_id       SERIAL PRIMARY KEY,
    sender_id    INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    reciever_id  INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    msg_content  TEXT NOT NULL,
    date         TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------------
-- Profile experiences.
-- ---------------------------------------------------------------------------
CREATE TABLE experiences (
    exp_id     SERIAL PRIMARY KEY,
    user_id    INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    exp_head   TEXT,
    exp_org    TEXT,
    exp_desc   TEXT,
    exp_media  TEXT
);

-- Helpful indexes for search / lookups
CREATE INDEX idx_jobs_status   ON jobs (job_status);
CREATE INDEX idx_unpaid_status ON unpaid (unpaid_status);
CREATE INDEX idx_events_status ON events (event_status);
CREATE INDEX idx_forum_status  ON forum (post_status);
CREATE INDEX idx_saved_user    ON saved_opps (user_id);
