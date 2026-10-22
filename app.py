"""KLL FindIt AI - starter Flask app.  Run with:  python app.py"""
from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, url_for

import config
import db
import matching

app = Flask(__name__)
app.secret_key = "change-this-before-the-demo"   # needed for flash messages

db.init_db()


def _form_item(kind):
    """Read the shared form fields into a dict."""
    f = request.form
    return dict(
        kind=kind,
        category=f.get("category", "").strip(),
        color=f.get("color", "").strip(),
        brand=f.get("brand", "").strip(),
        description=f.get("description", "").strip(),
        location=f.get("location", "").strip(),
        event_time=f.get("event_time", "").strip(),
    )


@app.route("/")
def index():
    return render_template(
        "index.html",
        lost_items=db.list_items("lost"),
        found_items=db.list_items("found"),
    )


@app.route("/lost", methods=["GET", "POST"])
def report_lost():
    if request.method == "POST":
        data = _form_item("lost")
        if not data["description"] or not data["event_time"]:
            flash("Please fill in the description and the date/time.")
        else:
            lost_id = db.add_item(**data, contact=request.form.get("contact", "").strip())
            return redirect(url_for("matches", lost_id=lost_id))
    return render_template("lost.html", cfg=config, now=datetime.now().strftime("%Y-%m-%dT%H:%M"))


@app.route("/found", methods=["GET", "POST"])
def log_found():
    if request.method == "POST":
        data = _form_item("found")
        if not data["description"] or not data["event_time"]:
            flash("Please fill in the description and the date/time.")
        else:
            db.add_item(
                **data,
                storage_place=request.form.get("storage_place", "").strip(),
                private_detail=request.form.get("private_detail", "").strip(),
            )
            flash("Found item saved.")
            return redirect(url_for("index"))
    return render_template("found.html", cfg=config, now=datetime.now().strftime("%Y-%m-%dT%H:%M"))


@app.route("/matches/<int:lost_id>")
def matches(lost_id):
    lost = db.get_item(lost_id)
    if lost is None or lost["kind"] != "lost":
        flash("Lost report not found.")
        return redirect(url_for("index"))
    ranked = matching.rank_matches(lost, db.list_items("found"))
    return render_template("matches.html", lost=lost, ranked=ranked)


@app.route("/claim", methods=["POST"])
def claim():
    # TODO (team): only logged-in staff should be able to use this route.
    lost_id = int(request.form["lost_id"])
    found_id = int(request.form["found_id"])
    outcome = request.form["outcome"]
    if outcome not in ("Verified", "Not Verified", "Pending"):
        flash("Invalid outcome.")
    else:
        db.record_claim(lost_id, found_id, outcome, request.form.get("notes", "").strip())
        flash(f"Claim saved: {outcome}")
    return redirect(url_for("matches", lost_id=lost_id))


if __name__ == "__main__":
    app.run(debug=True)
