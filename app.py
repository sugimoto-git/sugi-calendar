import csv
import os
import io
from flask import Flask, request, redirect, session, url_for
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

app = Flask(__name__)
app.secret_key = os.urandom(24)

# OAuth 2.0 configuration
CLIENT_SECRETS_FILE = "credentials.json"
SCOPES = ["https://www.googleapis.com/auth/calendar"]


@app.route("/")
def index():
    if "credentials" not in session:
        return redirect(url_for("oauth2callback"))

    credentials = Credentials(**session["credentials"])
    service = build("calendar", "v3", credentials=credentials)

    return """
    <h1>Google Calendar Event Uploader</h1>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    """


@app.route("/", methods=["POST"])
def upload_file():
    if "credentials" not in session:
        return redirect(url_for("oauth2callback"))

    credentials = Credentials(**session["credentials"])
    service = build("calendar", "v3", credentials=credentials)

    file = request.files["file"]
    if not file:
        return "No file uploaded.", 400

    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    reader = csv.reader(stream)
    header = next(reader)  # Skip header

    events = []
    for row in reader:
        summary, start_time, end_time, location = row
        event = {
            "summary": summary,
            "location": location,
            "start": {"dateTime": start_time, "timeZone": "Asia/Tokyo"},
            "end": {"dateTime": end_time, "timeZone": "Asia/Tokyo"},
        }
        created_event = (
            service.events().insert(calendarId="primary", body=event).execute()
        )
        events.append(created_event.get("htmlLink"))

    return f"Events created: <br>" + "<br>".join(events)


@app.route("/oauth2callback")
def oauth2callback():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, redirect_uri=url_for("oauth2callback", _external=True)
    )

    if "code" not in request.args:
        authorization_url, state = flow.authorization_url(
            access_type="offline", include_granted_scopes="true"
        )
        session["state"] = state
        return redirect(authorization_url)
    else:
        flow.fetch_token(code=request.args["code"])
        credentials = flow.credentials
        session["credentials"] = {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes,
        }
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)