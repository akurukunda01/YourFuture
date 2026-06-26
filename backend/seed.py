"""Seed the database with an admin account and a few sample listings.

Usage:
    DATABASE_URL=... ADMIN_USERNAME=admin ADMIN_PASSWORD=secret python seed.py

Safe to re-run: the admin is upserted and samples are only inserted when the
corresponding table is empty.
"""
import os
import sys

import psycopg2
from werkzeug.security import generate_password_hash


def get_conn():
    url = os.environ.get("DATABASE_URL")
    if not url:
        sys.exit("DATABASE_URL is not set")
    return psycopg2.connect(url)


def seed_admin(cur):
    username = os.environ.get("ADMIN_USERNAME", "admin")
    password = os.environ.get("ADMIN_PASSWORD")
    if not password:
        sys.exit("ADMIN_PASSWORD is not set — refusing to seed a blank admin")
    pw_hash = generate_password_hash(password, method="pbkdf2:sha256")
    cur.execute(
        """
        INSERT INTO users (username, user_password, user_type, user_org, user_status, full_name)
        VALUES (%s, %s, 'admin', 'YourFuture', 1, 'Site Admin')
        ON CONFLICT (username)
        DO UPDATE SET user_password = EXCLUDED.user_password, user_type = 'admin'
        RETURNING user_id
        """,
        (username, pw_hash),
    )
    admin_id = cur.fetchone()[0]
    print(f"  admin '{username}' ready (user_id={admin_id})")
    return admin_id


def seed_samples(cur, admin_id):
    cur.execute("SELECT count(*) FROM jobs")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            """INSERT INTO jobs
               (company, company_role, pay, job_description, job_location,
                apply_url, added_by)
               VALUES (%s,%s,%s,%s,%s,%s,%s)""",
            [
                ("Northwind Labs", "Software Intern", "$22/hr",
                 "Build internal tools with our engineering team.",
                 "Remote", "https://example.com/apply/northwind", admin_id),
                ("Cedar Health", "Data Analyst Intern", "$20/hr",
                 "Help analyze patient-flow data.",
                 "Columbus, OH", "https://example.com/apply/cedar", admin_id),
            ],
        )
        print("  inserted sample jobs")

    cur.execute("SELECT count(*) FROM unpaid")
    if cur.fetchone()[0] == 0:
        cur.execute(
            """INSERT INTO unpaid
               (organization, unpaid_role, unpaid_desc, unpaid_location, apply_url, added_by)
               VALUES (%s,%s,%s,%s,%s,%s)""",
            ("City Food Bank", "Volunteer Coordinator",
             "Coordinate weekend volunteer shifts.", "Local",
             "https://example.com/apply/foodbank", admin_id),
        )
        print("  inserted sample internship/volunteer opp")

    cur.execute("SELECT count(*) FROM events")
    if cur.fetchone()[0] == 0:
        cur.execute(
            """INSERT INTO events
               (organization, event_name, event_desc, event_location, event_date, apply_url, added_by)
               VALUES (%s,%s,%s,%s,%s,%s,%s)""",
            ("YourFuture", "Spring Career Fair",
             "Meet local employers and explore openings.", "Main Campus",
             "2026-04-15", "https://example.com/events/career-fair", admin_id),
        )
        print("  inserted sample event")


def main():
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            print("Seeding database...")
            admin_id = seed_admin(cur)
            seed_samples(cur, admin_id)
        print("Done.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
