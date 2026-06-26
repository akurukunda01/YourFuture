from flask import Blueprint, request, session, jsonify

from helpers import login_required
from db import get_db

site_bp = Blueprint("site", __name__, url_prefix="/api")


def _public_user(user):
    """A user row safe to return to clients (never expose the password hash)."""
    if user is None:
        return None
    return {
        "user_id": user["user_id"],
        "username": user["username"],
        "user_type": user["user_type"],
        "user_org": user["user_org"],
        "full_name": user.get("full_name"),
        "profile_pic": user.get("profile_pic"),
        "bio": user.get("bio"),
        "age": user.get("age"),
    }


@site_bp.route("/getmessages", methods=["GET"])
@login_required
def get_messages():
    conn, cursor = get_db()
    user_id = session["user_id"]

    cursor.execute(
        """
        SELECT m.*, s.username AS sender_username, r.username AS receiver_username
        FROM messages m
        JOIN users s ON m.sender_id = s.user_id
        JOIN users r ON m.reciever_id = r.user_id
        WHERE m.sender_id = %s OR m.reciever_id = %s
        ORDER BY m.date ASC
        """,
        (user_id, user_id),
    )
    messages = cursor.fetchall()

    inbox = {}
    for m in messages:
        if m["sender_id"] == user_id:
            other_username = m["receiver_username"]
        else:
            other_username = m["sender_username"]
        inbox.setdefault(other_username, []).append({
            "id": m["msg_id"],
            "content": m["msg_content"],
            "date": m["date"],
            "sender_id": m["sender_id"],
            "sender_username": m["sender_username"],
            "reciever_id": m["reciever_id"],
            "reciever_username": m["receiver_username"],
        })
    return jsonify(inbox)


@site_bp.route("/sendmessages", methods=["POST"])
@login_required
def send_messages():
    conn, cursor = get_db()
    sender_id = session["user_id"]
    receiver = request.form.get("reciever")
    msg_content = request.form.get("msg_content")

    if not (receiver and msg_content):
        return jsonify({"error": "recipient and message are required"}), 400

    cursor.execute("SELECT user_id FROM users WHERE username = %s", (receiver,))
    row = cursor.fetchone()
    if row is None:
        return jsonify({"error": "recipient not found"}), 404

    cursor.execute(
        "INSERT INTO messages (sender_id, reciever_id, msg_content) VALUES (%s, %s, %s)",
        (sender_id, row["user_id"], msg_content),
    )
    conn.commit()
    return jsonify({"success": "message sent"}), 200


@site_bp.route("/reciever", methods=["GET"])
@login_required
def receiver_search():
    item = request.args.get("q")
    if not item:
        return jsonify([])
    conn, cursor = get_db()
    cursor.execute(
        "SELECT username FROM users WHERE username ILIKE %s AND user_status = 1 AND user_id <> %s",
        (f"%{item}%", session["user_id"]),
    )
    return jsonify([row["username"] for row in cursor.fetchall()])


@site_bp.route("/getposts", methods=["GET"])
@login_required
def get_posts():
    conn, cursor = get_db()
    cursor.execute(
        """
        SELECT f.post_id, f.post_content, f.post_media, f.post_time,
               u.username AS added_by, u.full_name, u.profile_pic, u.user_org
        FROM forum f
        JOIN users u ON f.added_by = u.user_id
        WHERE f.post_status = 1
        ORDER BY f.post_time DESC
        """
    )
    return jsonify(cursor.fetchall())


@site_bp.route("/addpost", methods=["POST"])
@login_required
def add_post():
    conn, cursor = get_db()
    post_content = request.form.get("post_content")
    # Optional image URL (no file upload — keeps the app serverless-friendly).
    post_media = request.form.get("post_media") or None

    if not post_content:
        return jsonify({"error": "post content is required"}), 400

    cursor.execute(
        "INSERT INTO forum (added_by, post_content, post_media, post_status) VALUES (%s, %s, %s, 1)",
        (session["user_id"], post_content, post_media),
    )
    conn.commit()
    return jsonify({"success": "post has been added"}), 200


@site_bp.route("/postsearch", methods=["GET"])
@login_required
def post_search():
    item = request.args.get("q")
    if not item:
        return jsonify([])
    like = f"%{item}%"
    conn, cursor = get_db()
    cursor.execute(
        """
        SELECT f.post_id, f.post_content, f.post_media, f.post_time,
               u.username AS added_by, u.full_name, u.profile_pic, u.user_org
        FROM forum f
        JOIN users u ON f.added_by = u.user_id
        WHERE f.post_status = 1 AND (u.username ILIKE %s OR f.post_content ILIKE %s)
        ORDER BY f.post_time DESC
        """,
        (like, like),
    )
    return jsonify(cursor.fetchall())


@site_bp.route("/myprofile", methods=["GET"])
@login_required
def my_profile():
    conn, cursor = get_db()
    user_id = session["user_id"]

    cursor.execute("SELECT * FROM users WHERE user_id = %s AND user_status = 1", (user_id,))
    user = cursor.fetchone()
    if user is None:
        return jsonify({"error": "user not found"}), 404

    cursor.execute("SELECT * FROM experiences WHERE user_id = %s", (user_id,))
    experiences = cursor.fetchall()

    cursor.execute("SELECT * FROM saved_opps WHERE user_id = %s", (user_id,))
    saved = cursor.fetchall()
    saved_opps = []
    for save in saved:
        opp_type = save["opp_type"]
        if opp_type == "job":
            cursor.execute(
                "SELECT * FROM jobs WHERE job_id = %s AND job_status = 1", (save["opp_key"],)
            )
        elif opp_type == "unpaid":
            cursor.execute(
                "SELECT * FROM unpaid WHERE unpaid_id = %s AND unpaid_status = 1", (save["opp_key"],)
            )
        elif opp_type == "event":
            cursor.execute(
                "SELECT * FROM events WHERE event_id = %s AND event_status = 1", (save["opp_key"],)
            )
        else:
            continue
        opp = cursor.fetchone()
        if opp is not None:
            saved_opps.append({"opp_type": opp_type, "opp": opp})

    cursor.execute(
        "SELECT post_id, post_content, post_media, post_time FROM forum "
        "WHERE added_by = %s AND post_status = 1 ORDER BY post_time DESC",
        (user_id,),
    )
    posts = [dict(p, added_by=user["username"]) for p in cursor.fetchall()]

    return jsonify({
        "user": _public_user(user),
        "experiences": experiences,
        "posts": posts,
        "saved_opps": saved_opps,
    })


@site_bp.route("/profile/<int:id>", methods=["GET"])
@login_required
def retrieve_profile(id):
    conn, cursor = get_db()
    cursor.execute("SELECT * FROM users WHERE user_id = %s AND user_status = 1", (id,))
    user = cursor.fetchone()
    if user is None:
        return jsonify({"error": "user not found"}), 404
    cursor.execute("SELECT * FROM experiences WHERE user_id = %s", (id,))
    experiences = cursor.fetchall()
    return jsonify({"user": _public_user(user), "experiences": experiences})
