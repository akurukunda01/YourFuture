from urllib.parse import urlparse

from flask import Blueprint, request, session, jsonify

from helpers import admin_required
from db import get_db

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


def _clean(value):
    if value is None:
        return None
    value = str(value).strip()
    return value or None


def _valid_http_url(value):
    """Only allow http/https URLs (blocks javascript:/data: href injection)."""
    if not value:
        return False
    try:
        parsed = urlparse(value)
    except ValueError:
        return False
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


@admin_bp.route("/listings", methods=["GET"])
@admin_required
def list_all():
    conn, cursor = get_db()
    cursor.execute("SELECT * FROM jobs ORDER BY date_added DESC")
    jobs = cursor.fetchall()
    cursor.execute("SELECT * FROM unpaid ORDER BY date_added DESC")
    unpaid = cursor.fetchall()
    cursor.execute("SELECT * FROM events ORDER BY date_added DESC")
    events = cursor.fetchall()
    return jsonify({"jobs": jobs, "unpaid": unpaid, "events": events})


@admin_bp.route("/jobs", methods=["POST"])
@admin_required
def create_job():
    data = request.get_json(silent=True) or {}
    company = _clean(data.get("company"))
    company_role = _clean(data.get("company_role"))
    apply_url = _clean(data.get("apply_url"))

    if not (company and company_role):
        return jsonify({"error": "company and role are required"}), 400
    if not _valid_http_url(apply_url):
        return jsonify({"error": "a valid http(s) apply_url is required"}), 400

    conn, cursor = get_db()
    cursor.execute(
        """INSERT INTO jobs
           (company, company_role, pay, job_description, job_location,
            company_logo_url, apply_url, added_by)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING job_id""",
        (company, company_role, _clean(data.get("pay")),
         _clean(data.get("job_description")), _clean(data.get("job_location")),
         _clean(data.get("company_logo_url")), apply_url, session["user_id"]),
    )
    job_id = cursor.fetchone()["job_id"]
    conn.commit()
    return jsonify({"success": "job created", "job_id": job_id}), 201


@admin_bp.route("/jobs/<int:id>", methods=["DELETE"])
@admin_required
def delete_job(id):
    conn, cursor = get_db()
    cursor.execute("DELETE FROM jobs WHERE job_id = %s", (id,))
    conn.commit()
    return jsonify({"success": "job deleted"}), 200


@admin_bp.route("/unpaid", methods=["POST"])
@admin_required
def create_unpaid():
    data = request.get_json(silent=True) or {}
    organization = _clean(data.get("organization"))
    unpaid_role = _clean(data.get("unpaid_role"))
    apply_url = _clean(data.get("apply_url"))

    if not (organization and unpaid_role):
        return jsonify({"error": "organization and role are required"}), 400
    if not _valid_http_url(apply_url):
        return jsonify({"error": "a valid http(s) apply_url is required"}), 400

    conn, cursor = get_db()
    cursor.execute(
        """INSERT INTO unpaid
           (organization, unpaid_role, unpaid_desc, unpaid_location, org_logo, apply_url, added_by)
           VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING unpaid_id""",
        (organization, unpaid_role, _clean(data.get("unpaid_desc")),
         _clean(data.get("unpaid_location")), _clean(data.get("org_logo")),
         apply_url, session["user_id"]),
    )
    unpaid_id = cursor.fetchone()["unpaid_id"]
    conn.commit()
    return jsonify({"success": "opportunity created", "unpaid_id": unpaid_id}), 201


@admin_bp.route("/unpaid/<int:id>", methods=["DELETE"])
@admin_required
def delete_unpaid(id):
    conn, cursor = get_db()
    cursor.execute("DELETE FROM unpaid WHERE unpaid_id = %s", (id,))
    conn.commit()
    return jsonify({"success": "opportunity deleted"}), 200


@admin_bp.route("/events", methods=["POST"])
@admin_required
def create_event():
    data = request.get_json(silent=True) or {}
    organization = _clean(data.get("organization"))
    event_name = _clean(data.get("event_name"))
    apply_url = _clean(data.get("apply_url"))

    if not (organization and event_name):
        return jsonify({"error": "organization and event name are required"}), 400
    if not _valid_http_url(apply_url):
        return jsonify({"error": "a valid http(s) apply_url is required"}), 400

    conn, cursor = get_db()
    cursor.execute(
        """INSERT INTO events
           (organization, event_name, event_desc, event_location, org_logo,
            apply_url, event_date, added_by)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING event_id""",
        (organization, event_name, _clean(data.get("event_desc")),
         _clean(data.get("event_location")), _clean(data.get("org_logo")),
         apply_url, _clean(data.get("event_date")), session["user_id"]),
    )
    event_id = cursor.fetchone()["event_id"]
    conn.commit()
    return jsonify({"success": "event created", "event_id": event_id}), 201


@admin_bp.route("/events/<int:id>", methods=["DELETE"])
@admin_required
def delete_event(id):
    conn, cursor = get_db()
    cursor.execute("DELETE FROM events WHERE event_id = %s", (id,))
    conn.commit()
    return jsonify({"success": "event deleted"}), 200
