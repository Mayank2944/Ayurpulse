from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import csv
import os

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # Enable CORS for all routes


# Initialize CSV file with headers
def init_csv():
    file_path = "data.csv"
    if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
        fields = ["timestamp", "mac", "ir1", "ir2", "ir3", "spo2", "temperature", "dosha"]
        try:
            with open(file_path, mode="w", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fields)
                writer.writeheader()
            print("✓ CSV file initialized with headers")
        except Exception as e:
            print(f"Error initializing CSV: {e}")


init_csv()  # Initialize on startup


def determine_dosha(pulse, temp):
    pulse = float(pulse)
    temp = float(temp)

    if pulse > 80 and temp < 98.4:
        return "Vata"
    if pulse > 80 and 98.6 <= temp <= 99:
        return "Vat-Pitta"
    if 70 <= pulse <= 80 and temp > 99:
        return "Pitta"
    if 70 <= pulse <= 80 and temp < 98:
        return "Pitta-Kapha"
    if pulse < 70 and temp < 98:
        return "Kapha"
    if pulse > 80 and temp < 95:
        return "Kapha-Vat"

    return "Healthy"


def getval(ir1, ir2, ir3, temp):
    try:
        ir1 = float(ir1 or 0)
        ir2 = float(ir2 or 0)
        ir3 = float(ir3 or 0)
        temp = float(temp or 98.6)
    except:
        return "Invalid"

    pulse = (ir1 + ir2 + ir3) / 1500.0 if (ir1 + ir2 + ir3) > 0 else 75
    pulse = max(60.0, min(110.0, pulse))

    return determine_dosha(pulse, temp)


@app.route("/data", methods=["POST"])
def esp32_data():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    incoming = request.get_json()
    print("Received JSON data:", incoming)

    # Fields including prediction
    fields = ["timestamp", "mac", "ir1", "ir2", "ir3", "spo2", "temperature", "dosha"]

    # Create clean row
    data = {}
    for field in fields:
        data[field] = incoming.get(field, None)

    # Compute dosha
    data["dosha"] = getval(
        incoming.get("ir1"),
        incoming.get("ir2"),
        incoming.get("ir3"),
        incoming.get("temperature")
    )

    file_path = "data.csv"
    file_exists = os.path.isfile(file_path)

    try:
        with open(file_path, mode="a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)

            # Write header if file doesn't exist
            if not file_exists:
                writer.writeheader()

            writer.writerow(data)

        return jsonify({
            "message": "Data saved successfully",
            "dosha": data["dosha"]
        }), 200

    except Exception as e:
        print("Error writing to CSV:", str(e))
        return jsonify({"error": "Failed to save data"}), 500


@app.route('/')
def serve_antigravity():
    return send_from_directory('.', 'reovered.html')


@app.route('/data.csv')
def serve_data():
    response = send_from_directory('.', 'data.csv')
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/api/latest', methods=['GET'])
def get_latest_data():
    """Get latest data row as JSON"""
    try:
        if not os.path.isfile("data.csv"):
            return jsonify({"error": "No data available"}), 404
        
        with open("data.csv", 'r') as f:
            lines = f.readlines()
            if len(lines) < 2:
                return jsonify({"error": "No data available"}), 404
            
            reader = csv.DictReader(lines)
            rows = list(reader)
            if not rows:
                return jsonify({"error": "No data available"}), 404
            
            latest = rows[-1]
            return jsonify(latest), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)