from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# ✅ Use the correct OpenWeather API key & endpoint
API_KEY = "aa34533c5046196d481c875f167a7122"  # Replace with your actual API key 
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"  # ✅ Correct API endpoint 

@app.route("/", methods=["GET", "POST"])
def home():
    weather_data = None
    error_message = None

    if request.method == "POST":
        city = request.form.get("city")
        params = {"q": city, "appid": API_KEY, "units": "metric"}  # Use metric system for °C

        response = requests.get(BASE_URL, params=params)
        print("Response Status Code:", response.status_code)
        print("Response Content:", response.text)

        if response.status_code == 200:
            try:
                data = response.json()
                weather_data = {
                    "city": data["name"], 
                    "temperature": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"].title(),
                    "icon": f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png",
                }
            except requests.exceptions.JSONDecodeError:
                error_message = "Error decoding JSON. Please try again."
        elif response.status_code == 401:
            error_message = "Invalid API Key. Please check your API key."
        elif response.status_code == 404:
            error_message = "City not found. Please enter a valid city."
        else:
            error_message = f"API Error: {response.status_code}. Please try again later."

    return render_template("index.html", weather=weather_data, error=error_message)

if __name__ == "__main__":
    app.run(debug=True)
