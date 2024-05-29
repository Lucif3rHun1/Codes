from flask import Flask, jsonify
import threading
import requests

app = Flask(__name__)

# Initialize request counter and lock
request_count = 0
count_lock = threading.Lock()

# Define the target URL for the cookie function
target_url = "https://www.google.com"

# Variable to store the initial cookies
initial_cookies = None
fetching_cookies = False  # Flag to indicate if cookies are being fetched

# A sample function to simulate calling Google and retrieving cookies
def cookie():
    try:
        response = requests.get(target_url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        cookies = response.cookies
        cookie_string = ", ".join([f"{name}={value}" for name, value in cookies.items()])
        return cookie_string
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

# Function to call the `cookie()` function for every 10 requests
def check_and_call_cookie():
    global request_count, initial_cookies, fetching_cookies
    while True:
        if request_count >= 10:
            print("Refreshing cookies...")
            fetching_cookies = True
            updated_cookies = cookie()
            fetching_cookies = False
            if not updated_cookies.startswith("Error:"):
                with count_lock:
                    initial_cookies = updated_cookies
                    request_count = 0
        time.sleep(1)  # Sleep to avoid busy-waiting

# Endpoint to handle incoming requests
@app.route('/')
def get_cookies():
    global request_count
    with count_lock:
        request_count += 1
    if fetching_cookies:
        return jsonify({"Error": "Please try again later, new cookies are being fetched"})
    return jsonify({"RequestCount": request_count, "Cookies": initial_cookies})

if __name__ == '__main__':
    import time

    # Automatically call the cookie() function when the script starts to initialize initial cookies
    print("Initializing cookies...")
    initial_cookies = cookie()

    # Start a separate thread to check and call `cookie()` every 10 requests
    checker_thread = threading.Thread(target=check_and_call_cookie)
    checker_thread.start()

    # Run the Flask app on 0.0.0.0 and port 1234 with multithreading
    app.run(host='0.0.0.0', port=1234, threaded=True)
