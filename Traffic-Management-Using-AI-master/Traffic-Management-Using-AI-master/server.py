from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Get the absolute path of the current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(BASE_DIR, 'templates')

# Initialize simulation data
simulation_data = {
    'timeElapsed': 0,
    'signals': [
        {'status': 'RED', 'timer': 0},
        {'status': 'RED', 'timer': 0},
        {'status': 'RED', 'timer': 0},
        {'status': 'RED', 'timer': 0}
    ],
    'vehicleCounts': {
        'right': 0,
        'down': 0,
        'left': 0,
        'up': 0
    }
}

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"Error loading template: {str(e)}")
        return f"Error: {str(e)}", 500

@app.route('/get_data')
def get_data():
    try:
        return jsonify(simulation_data)
    except Exception as e:
        print(f"Error getting data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/update_data', methods=['POST'])
def update_data():
    try:
        global simulation_data
        data = request.get_json()
        
        # Validate and update simulation data
        if data and isinstance(data, dict):
            if 'elapsed_time' in data:
                simulation_data['timeElapsed'] = data['elapsed_time']
            
            if 'signals_data' in data and isinstance(data['signals_data'], list):
                simulation_data['signals'] = [
                    {'status': signal['status'], 'timer': signal['timer']}
                    for signal in data['signals_data']
                ]
            
            if 'vehicle_counts' in data and isinstance(data['vehicle_counts'], dict):
                simulation_data['vehicleCounts'] = data['vehicle_counts']
            
            return jsonify({'status': 'success'})
        else:
            return jsonify({'error': 'Invalid data format'}), 400
            
    except Exception as e:
        print(f"Error updating data: {str(e)}")
        return jsonify({'error': str(e)}), 500

def run_server():
    try:
        app.run(host='127.0.0.1', port=5000, debug=False)
    except Exception as e:
        print(f"Server error: {str(e)}")

if __name__ == '__main__':
    print(f"Starting server on http://127.0.0.1:5000")
    print(f"Template directory: {template_dir}")
    run_server()