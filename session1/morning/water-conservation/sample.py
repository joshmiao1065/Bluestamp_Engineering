import tkinter as tk

root = tk.Tk()
root.title("Water Conservation Dashboard")

# Example widgets
tk.Label(root, text="Estimated Water Use: 120L/day", font=("Arial", 16)).pack()
tk.Label(root, text="Local Drought: Moderate", fg="red", font=("Arial", 14)).pack()
tk.Label(root, text="Tip: Turn off the tap while brushing!", font=("Arial", 12)).pack()

root.mainloop()

import requests

api_key = "a58478d180b3d306f2b27199aff9e4e9"
city = "Boston"
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

response = requests.get(url).json()
weather = response['weather'][0]['description']
print("Weather:", weather)

import time
tips = [
    "Fix leaky faucets to save 10% on water bills!",
    "Collect rainwater for garden use.",
    "Run full loads in dishwashers and washing machines."
]

while True:
    print(tips[0])
    tips.append(tips.pop(0))
    time.sleep(30)

from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def home():
    water_use = 120
    tip = "Take shorter showers!"
    return render_template("dashboard.html", water=water_use, tip=tip)

app.run(host="0.0.0.0", port=80)
