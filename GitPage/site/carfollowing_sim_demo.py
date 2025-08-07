import numpy as np
import matplotlib.pyplot as plt
import json
import os

# Load configuration file
config_file = "openpav_config.json"

if not os.path.exists(config_file):
    raise FileNotFoundError(f"Configuration file '{config_file}' not found. Please download it first.")

with open(config_file, "r") as file:
    config = json.load(file)

# Extract parameters from JSON
try:
    param_str = config["parameter"]
    param_dict = dict(item.split("=") for item in param_str.split(", "))
    kv = float(param_dict["kv"])
    kg = float(param_dict["kg"])
    Td = float(param_dict["td"])
    z = float(param_dict["z"])
except KeyError as e:
    raise ValueError(f"Missing parameter {e} in config file.")

# Simulation settings
dt = 0.1  # Time step (s)
T = 20    # Total simulation time (s)
steps = int(T / dt)

# Initialize lead vehicle motion
time = np.linspace(0, T, steps)
p_lead = 10 + 2 * time  # Lead vehicle position (constant speed 2 m/s)
v_lead = np.full(steps, 2.0)  # Lead vehicle velocity

# Initialize following vehicle motion
p_follow = np.zeros(steps)  # Following vehicle position
v_follow = np.zeros(steps)  # Following vehicle velocity
a_follow = np.zeros(steps)  # Following vehicle acceleration

# Simulation loop
for t in range(1, steps):
    a_follow[t] = kv * (v_lead[t] - v_follow[t]) + kg * (p_lead[t] - p_follow[t] - v_follow[t] * Td) + z
    v_follow[t] = v_follow[t-1] + a_follow[t] * dt
    p_follow[t] = p_follow[t-1] + v_follow[t] * dt

# Plot results
plt.figure(figsize=(10, 5))
plt.plot(time, p_lead, label="Lead Vehicle", linestyle="--")
plt.plot(time, p_follow, label="Following Vehicle")
plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.title(f"Car-Following Simulation - {config['vehicle']} ({config['model']} Model)")
plt.legend()
plt.grid(True)
plt.show()
