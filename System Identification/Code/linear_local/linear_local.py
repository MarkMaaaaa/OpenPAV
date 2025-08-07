import pandas as pd
import numpy as np
import json
from datetime import datetime
from sklearn.linear_model import LinearRegression

# Load the trajectory data
file_path = "C:\\Users\\20410\\OneDrive\\文档\\GitHub\\OpenPAV\\Calibration\\Code\\Trajectory_example.xlsx"  # Ensure this file exists in the working directory
xls = pd.ExcelFile(file_path)

# Load the first sheet (assuming the correct data is here)
df = pd.read_excel(xls, sheet_name=xls.sheet_names[0])

# Prepare data for regression
X = np.column_stack([
    df["Speed_LV"],  # Lead vehicle velocity (v_l)
    df["Speed_FAV"],  # Following vehicle velocity (v_f)
    df["Pos_LV"] - df["Pos_FAV"],  # Position difference (p_l - p_f)
])
y = df["Acc_FAV"]  # Acceleration of the following vehicle (a_f)

# Fit the regression model
reg = LinearRegression().fit(X, y)

# Extract regression coefficients
kv = reg.coef_[0]  # Coefficient for v_l
kg = reg.coef_[2]  # Coefficient for (p_l - p_f)

# Solve for T_d using the relationship: coef_vf = -k_v - k_g * T_d
Td = -(reg.coef_[1] + kv) / kg  # Td = -(coef_vf + kv) / kg

# Intercept as z
z = reg.intercept_

# Generate standardized JSON output
parameter_data = {
    "vehicle": "Audi A4",  # Example vehicle
    "model": "Linear",
    "filetype": "Original",
    "parameter": f"kv={kv:.3f}, kg={kg:.3f}, td={Td:.3f}, z={z:.3f}",
    "timestamp": datetime.utcnow().isoformat()
}

# Save as JSON file
json_output_path = "C:\\Users\\20410\\OneDrive\\文档\\GitHub\\OpenPAV\\Calibration\\Model repositories\\vehicle_parameters.json"
with open(json_output_path, "w") as json_file:
    json.dump(parameter_data, json_file, indent=2)

# Print results
print(f"Car-Following Model Parameters:")
print(json.dumps(parameter_data, indent=2))

print(f"\nParameter file saved as {json_output_path}")
