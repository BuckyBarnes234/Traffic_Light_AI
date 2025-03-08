# We'll implement this after fixing the core simulation 

import requests
from requests.exceptions import RequestException
import threading
from flask import Flask
from server import app

class WebInterface:
    def __init__(self):
        self.server_url = 'http://localhost:5000'
        self.server_thread = None
        
    def start_server(self):
        """Start the Flask server in a separate thread"""
        self.server_thread = threading.Thread(
            name="flaskServer",
            target=lambda: app.run(debug=False, port=5000, use_reloader=False)
        )
        self.server_thread.daemon = True
        self.server_thread.start()
    
    def update_simulation_data(self, signals, vehicles, timeElapsed, currentGreen, currentYellow):
        """Send simulation data to web server"""
        try:
            # Prepare signal data
            signals_data = []
            for i in range(len(signals)):
                status = "RED"
                timer = signals[i].red
                if i == currentGreen:
                    if currentYellow == 1:
                        status = "YELLOW"
                        timer = signals[i].yellow
                    else:
                        status = "GREEN"
                        timer = signals[i].green
                
                signals_data.append({
                    "status": status,
                    "timer": timer
                })
            
            # Prepare vehicle count data
            vehicle_counts = {
                'right': vehicles['right']['crossed'],
                'down': vehicles['down']['crossed'],
                'left': vehicles['left']['crossed'],
                'up': vehicles['up']['crossed']
            }
            
            # Prepare data payload
            data = {
                'elapsed_time': timeElapsed,
                'signals_data': signals_data,
                'vehicle_counts': vehicle_counts
            }
            
            # Send data to server
            response = requests.post(f'{self.server_url}/update_data', json=data, timeout=0.1)
            if response.status_code != 200:
                print(f"Error updating web interface: {response.status_code}")
                
        except RequestException:
            pass  # Silently fail if server is not running
        except Exception as e:
            print(f"Error updating web interface: {str(e)}") 