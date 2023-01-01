import subprocess
from flask import Flask, render_template

app = Flask(__name__)

def get_wifi_info():
    # Run the 'nmcli --terse --fields name,ssid,bssid,signal device wifi list' command to get a list of WiFi profiles
    profiles = subprocess.run(['nmcli', '--terse', '--fields', 'name,ssid,bssid,signal', 'device', 'wifi', 'list'], stdout=subprocess.PIPE).stdout.decode('utf-8')

    # Extract the WiFi names and passwords from the command output
    wifi_info = []
    for profile in profiles.split('\n'):
        fields = profile.split(':')
        if len(fields) < 3:
            continue
        name = fields[1]
        password = None
        if fields[2] == '--':
            password = fields[3]
        wifi_info.append({'name': name, 'password': password})

    return wifi_info

@app.route('/')
def home():
    wifi_info = get_wifi_info()
    return render_template('home.html', wifi_info=wifi_info)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=2345)
