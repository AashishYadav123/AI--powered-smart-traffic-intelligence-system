import tkinter as tk
import random

previous = {"North": 0, "South": 0, "East": 0, "West": 0}
emergency = None

# Weather conditions
weather_conditions = ["Normal", "Fog", "Rain", "Night"]
current_weather = "Normal"

# ---------------- Traffic Logic ----------------

def calculate_time(count, stressed=0, high_risk=0):
    """Base green time + stress + accident risk"""
    if count < 20:
        base = 5
    elif count < 40:
        base = 8
    else:
        base = 12
    # Add extra time for stressed drivers and high-risk vehicles
    return base + stressed*0.5 + high_risk*1

def get_congestion_level(total):
    if total < 100:
        return "Low Traffic 🟢"
    elif total < 180:
        return "Medium Traffic 🟡"
    else:
        return "High Traffic 🔴"

def adjust_for_weather(green_time, lane):
    """Modify green time / risk / display based on weather"""
    global current_weather
    if current_weather == "Fog":
        # Fog → longer green time
        green_time += 3
    elif current_weather == "Rain":
        # Rain → stricter risk evaluation
        risk_scores[lane] += 0.2
    elif current_weather == "Night":
        # Night → dim lighting
        directions[lane].config(bg="gray20")
    else:
        # Normal
        directions[lane].config(bg="black")
    return green_time

def show_yellow(direction):
    directions[direction].delete("all")
    directions[direction].create_oval(20, 20, 80, 80, fill="yellow")
    status.config(text=f"Yellow: {direction}")
    root.after(2000, update_signals)

def countdown(direction, time_left, total, level, stress, risk):
    if time_left > 0:
        status.config(
            text=f"Green: {direction} | {level} | Total: {total} | Time Left: {time_left}s | Stress:{stress} | Risk:{risk} | Weather:{current_weather}"
        )
        root.after(1000, countdown, direction, time_left-1, total, level, stress, risk)
    else:
        show_yellow(direction)

def activate_emergency():
    global emergency
    emergency = random.choice(["North", "South", "East", "West"])
    update_signals()

def update_signals():
    global previous, emergency, current_weather

    # Simulate weather
    current_weather = random.choice(weather_conditions)
    weather_label.config(text=f"Weather: {current_weather}")

    traffic = {}
    stress_levels = {}
    global risk_scores
    risk_scores = {}
    for d in previous:
        # Random traffic count
        current = random.randint(5, 60)
        traffic[d] = int(current + previous[d]*0.3)
        # Simulate driver stress (0-100)
        stress_levels[d] = random.randint(0, 100)
        # Simulate accident risk (0-1)
        risk_scores[d] = round(random.random(),2)

    total = sum(traffic.values())
    level = get_congestion_level(total)

    if emergency:
        max_dir = emergency
        green_time = 10
        emergency = None
    else:
        # Combine traffic + stress + risk for decision
        scores = {}
        for d in traffic:
            scores[d] = traffic[d]*0.5 + stress_levels[d]*0.3 + risk_scores[d]*0.2
        max_dir = max(scores, key=scores.get)
        green_time = calculate_time(traffic[max_dir], stress_levels[max_dir]//20, int(risk_scores[max_dir]*5))

    # Apply weather adaptive adjustments
    green_time = adjust_for_weather(green_time, max_dir)

    previous = traffic.copy()

    for d in directions:
        directions[d].delete("all")
        if d == max_dir:
            directions[d].create_oval(20, 20, 80, 80, fill="green")
        else:
            if risk_scores[d] > 0.7:
                directions[d].create_oval(20, 20, 80, 80, fill="red")
                directions[d].create_text(50, 50, text="⚠️", font=("Arial", 20), fill="yellow")
            else:
                directions[d].create_oval(20, 20, 80, 80, fill="red")

    countdown(max_dir, int(green_time), total, level, stress_levels[max_dir], risk_scores[max_dir])

# ---------------- GUI ----------------

root = tk.Tk()
root.title("AI-Powered Smart Traffic Intelligence System")
root.geometry("750x550")

title = tk.Label(root, text="AI-Powered Smart Traffic Intelligence System",
                 font=("Arial", 16, "bold"))
title.pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=20)

directions = {}

for name in ["North", "South", "East", "West"]:
    box = tk.Frame(frame)
    box.pack(side="left", padx=15)

    tk.Label(box, text=name, font=("Arial", 11)).pack()
    canvas = tk.Canvas(box, width=100, height=100, bg="black")
    canvas.pack()
    directions[name] = canvas

status = tk.Label(root, text="Smart City Dashboard Ready",
                  font=("Arial", 13))
status.pack(pady=10)

weather_label = tk.Label(root, text=f"Weather: {current_weather}", font=("Arial", 12, "bold"))
weather_label.pack(pady=5)

tk.Button(root, text="Start System",
          font=("Arial", 11),
          command=update_signals).pack(pady=5)

tk.Button(root, text="Emergency Mode 🚑",
          font=("Arial", 11),
          bg="red", fg="white",
          command=activate_emergency).pack(pady=5)

root.mainloop()
