from flask import Blueprint, request, session, jsonify

from helpers import login_required
from db import get_db

jobs_bp = Blueprint("jobs", __name__, url_prefix="/api")

ALLOWED_OPP_TYPES = ("job", "unpaid", "event")


def _date(value):
    return value.strftime("%Y-%m-%d") if value else None


def _job_dict(job):
    return {
        "job_id": job["job_id"],
        "company": job["company"],
        "company_role": job["company_role"],
        "pay": job["pay"],
        "job_description": job["job_description"],
        "job_location": job["job_location"],
        "company_logo_url": job["company_logo_url"],
        "apply_url": job["apply_url"],
    }


def _unpaid_dict(opp):
    return {
        "unpaid_id": opp["unpaid_id"],
        "organization": opp["organization"],
        "org_logo": opp["org_logo"],
        "unpaid_desc": opp["unpaid_desc"],
        "unpaid_location": opp["unpaid_location"],
        "unpaid_role": opp["unpaid_role"],
        "apply_url": opp["apply_url"],
        "date_added": _date(opp["date_added"]),
    }


def _event_dict(event):
    return {
        "event_id": event["event_id"],
        "organization": event["organization"],
        "org_logo": event["org_logo"],
        "event_name": event["event_name"],
        "event_desc": event["event_desc"],
        "event_location": event["event_location"],
        "apply_url": event["apply_url"],
        "event_date": _date(event["event_date"]),
        "date_added": _date(event["date_added"]),
    }


@jobs_bp.route("/viewjobs", methods=["GET"])
def view_jobs():
    conn, cursor = get_db()

    # Mark jobs the *current* user has saved (only when logged in).
    saved_keys = set()
    user_id = session.get("user_id")
    if user_id is not None:
        cursor.execute(
            "SELECT opp_key FROM saved_opps WHERE user_id = %s AND opp_type = 'job'",
            (user_id,),
        )
        saved_keys = {row["opp_key"] for row in cursor.fetchall()}

    cursor.execute("SELECT * FROM jobs WHERE job_status = 1 ORDER BY date_added DESC")
    portfolio = []
    for job in cursor.fetchall():
        item = _job_dict(job)
        if job["job_id"] in saved_keys:
            item["saved"] = 1
        portfolio.append(item)
    return jsonify(portfolio)


@jobs_bp.route("/viewunpaid", methods=["GET"])
def get_unpaid():
    conn, cursor = get_db()
    cursor.execute("SELECT * FROM unpaid WHERE unpaid_status = 1 ORDER BY date_added DESC")
    return jsonify([_unpaid_dict(o) for o in cursor.fetchall()])


@jobs_bp.route("/viewevents", methods=["GET"])
def get_events():
    conn, cursor = get_db()
    cursor.execute("SELECT * FROM events WHERE event_status = 1 ORDER BY date_added DESC")
    return jsonify([_event_dict(e) for e in cursor.fetchall()])


@jobs_bp.route("/job/<int:id>", methods=["GET"])
def job_details(id):
    conn, cursor = get_db()
    cursor.execute("SELECT * FROM jobs WHERE job_id = %s AND job_status = 1", (id,))
    job = cursor.fetchone()
    if job is None:
        return jsonify({"error": "Job not found"}), 404
    data = _job_dict(job)
    data["description"] = job["job_description"]
    data["location"] = job["job_location"]
    return jsonify(data)


@jobs_bp.route("/unpaid/<int:id>", methods=["GET"])
def unpaid_details(id):
    conn, cursor = get_db()
    cursor.execute("SELECT * FROM unpaid WHERE unpaid_id = %s AND unpaid_status = 1", (id,))
    opp = cursor.fetchone()
    if opp is None:
        return jsonify({"error": "Opportunity not found"}), 404
    return jsonify(_unpaid_dict(opp))


@jobs_bp.route("/events/<int:id>", methods=["GET"])
def event_details(id):
    conn, cursor = get_db()
    cursor.execute("SELECT * FROM events WHERE event_id = %s AND event_status = 1", (id,))
    event = cursor.fetchone()
    if event is None:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(_event_dict(event))


@jobs_bp.route("/saveopp", methods=["POST"])
@login_required
def save_opp():
    conn, cursor = get_db()
    data = request.get_json(silent=True) or {}
    opp_type = data.get("opp_type")
    opp_key = data.get("opp_key")

    if opp_type not in ALLOWED_OPP_TYPES:
        return jsonify({"error": "invalid opportunity type"}), 400
    try:
        opp_key = int(opp_key)
    except (TypeError, ValueError):
        return jsonify({"error": "invalid opportunity key"}), 400

    cursor.execute(
        """INSERT INTO saved_opps (opp_type, opp_key, user_id)
           VALUES (%s, %s, %s)
           ON CONFLICT (user_id, opp_type, opp_key) DO NOTHING""",
        (opp_type, opp_key, session["user_id"]),
    )
    conn.commit()
    return jsonify({"success": "opportunity has been saved"}), 200


@jobs_bp.route("/search", methods=["GET"])
def search():
    item = request.args.get("q")
    if not item:
        return jsonify([])

    like = f"%{item}%"
    conn, cursor = get_db()
    portfolio = []

    cursor.execute(
        """SELECT * FROM jobs
           WHERE job_status = 1 AND (company ILIKE %s OR company_role ILIKE %s)""",
        (like, like),
    )
    for job in cursor.fetchall():
        data = _job_dict(job)
        data["description"] = job["job_description"]
        data["type"] = "job"
        portfolio.append(data)

    cursor.execute(
        """SELECT * FROM unpaid
           WHERE unpaid_status = 1 AND (organization ILIKE %s OR unpaid_role ILIKE %s)""",
        (like, like),
    )
    for opp in cursor.fetchall():
        data = _unpaid_dict(opp)
        data["type"] = "unpaid"
        portfolio.append(data)

    cursor.execute(
        """SELECT * FROM events
           WHERE event_status = 1 AND (organization ILIKE %s OR event_name ILIKE %s)""",
        (like, like),
    )
    for event in cursor.fetchall():
        data = _event_dict(event)
        data["type"] = "event"
        portfolio.append(data)

    return jsonify(portfolio)
