from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Memori sementara untuk menyimpan data sensor dari ESP32
sensor_data = {
    "type": "telemetry",
    "az": 90.0,
    "el": 0.0,
    "lux": 0.0,
    "volt": 0.0
}

# Memori sementara untuk menyimpan perintah klik dari Web
command_data = {
    "mode": "auto",
    "az": 90.0,
    "el": 0.0,
    "new_cmd": False
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/<page_name>')
def render_page(page_name):
    if page_name.endswith('.html'):
        return render_template(page_name)
    return render_template('index.html')

# --- ENDPOINT DATA SENSOR ---
@app.route('/api/telemetry', methods=['GET', 'POST'])
def handle_telemetry():
    global sensor_data
    if request.method == 'POST':
        # Menerima setoran data dari ESP32
        data = request.json
        if data:
            sensor_data.update(data)
        return jsonify({"status": "sukses_diterima"})
    
    # Memberikan data saat Browser meminta (GET)
    return jsonify(sensor_data)

# --- ENDPOINT PERINTAH MOTOR ---
@app.route('/api/command', methods=['GET', 'POST'])
def handle_command():
    global command_data
    if request.method == 'POST':
        # Menerima perintah klik (Manual Mode) dari Browser
        data = request.json
        if data:
            command_data.update(data)
            command_data["new_cmd"] = True # Tandai ada perintah baru
        return jsonify({"status": "perintah_diterima"})
    
    # Memberikan perintah saat ESP32 mengecek (GET)
    resp = command_data.copy()
    command_data["new_cmd"] = False # Reset setelah dibaca ESP32
    return jsonify(resp)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)