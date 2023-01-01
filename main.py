import subprocess
from flask import Flask, render_template

app = Flask(__name__)

def get_wifi_info():
    # Run the 'netsh wlan show profiles' command to get a list of WiFi profiles
    profiles = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], stdout=subprocess.PIPE).stdout.decode('utf-8')

    # Extract the names of the WiFi profiles
    profiles = profiles.split('\n')
    profiles = [p.strip() for p in profiles if 'Profile' in p]
    profiles = [p.split(': ')[1] for p in profiles]

    # Run the 'netsh wlan show profile name=PROFILE_NAME key=clear' command for each profile to get the password
    wifi_info = []
    for profile in profiles:
        result = subprocess.run(['netsh', 'wlan', 'show', 'profile', f'name={profile}', 'key=clear'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        lines = result.split('\n')

        # Extract the WiFi name and password from the command output
        name = None
        password = None
        for line in lines:
            if 'SSID name' in line:
                name = line.split(': ')[1]
            elif 'Key Content' in line:
                password = line.split(': ')[1]

        # Add the WiFi name and password to the list
        wifi_info.append({'name': name, 'password': password})

    return wifi_info

@app.route('/')
def home():
    wifi_info = get_wifi_info()
    return render_template('home.html', wifi_info=wifi_info)

if __name__ == '__main__':
    app.run()
