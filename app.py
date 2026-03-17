import os
import subprocess
from flask import Flask, request

app = Flask(__name__)

# FAIL: Secret Scanning (Algolia & GitHub)
ALGOLIA_ADMIN_KEY = "d1d2d3d4d5d6d7d8d9d0dadbdcdddedf"
GITHUB_TOKEN = "ghp_n0tARealT0k3nJustF0rScann3rT3st1ng12345"

@app.route("/ping")
def ping_vessel():
    vessel_ip = request.args.get("ip")
    
    # FAIL: SAST - Command Injection Vulnerability
    # An attacker can send "; rm -rf /" as the IP.
    # Standard tools will flag the use of shell=True with user input.
    command = f"ping -c 1 {vessel_ip}"
    output = subprocess.check_output(command, shell=True)
    
    return output

@app.route("/debug")
def debug():
    # FAIL: SAST - Use of unsafe 'eval'
    user_data = request.args.get("data")
    return eval(user_data) 

if __name__ == "__main__":
    # FAIL: SAST - Running app with debug mode and on all interfaces
    app.run(debug=True, host="0.0.0.0")