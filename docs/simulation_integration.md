# Simulation Integration

Integrate Open-PAV with various simulation platforms to analyze automated vehicle behaviors.

## Supported Platforms

- **Python-Based Basic Model**: Simulate simple car-following behavior using a basic linear model.
- **SUMO**: Implement Intelligent Driver Model (IDM) for SUMO-based simulations.
- **VISSIM**: Implement Wiedemann-99 models with external driver models.
- **TorchScript (AI-Based Models)**: Deploy deep learning-based car-following models using PyTorch.

---

## Python-Based Basic Model

A **Basic Linear Model** can be implemented using the following car-following equation:

\[
a = k_v (v_l - v_f) + k_g (p_l - p_f - v_f \cdot T_d) + z
\]

where:
- \( v_l, v_f \) = velocities of the lead and following vehicle.
- \( p_l, p_f \) = positions of the lead and following vehicle.
- \( T_d \) = time delay.
- \( k_v, k_g, z \) = model parameters.

### **Example Simulation**
Below is a plot of a simple highway simulation where a **Tesla follows a lead vehicle**.

![Basic Model Simulation]

To run the simulation:
refer to [Quick Start](quick_start.md)

---

## SUMO Integration

The **Intelligent Driver Model (IDM)** is supported in SUMO for car-following simulations.

### **Steps to Integrate IDM in SUMO**
1. **Install SUMO** if not already installed:
   ```bash
   sudo apt-get install sumo sumo-tools sumo-doc  # Ubuntu
   ```
2. **Prepare SUMO Configuration:**
   - Open the **SUMO configuration file** and add the IDM car-following model.
   ```xml
   <vType id="IDM" accel="XX" decel="XX" sigma="XX" length="5" minGap="2.5" maxSpeed="33.3" guiShape="passenger"/>
   ```
3. **Assign the IDM Model** to Vehicles:
   ```xml
   <vehicle id="veh0" type="IDM" route="route0" depart="0" />
   ```
4. **Run SUMO Simulation**:
   ```bash
   sumo -c simulation.sumocfg
   ```

🔗 [More details on IDM in SUMO](https://sumo.dlr.de/docs/Developer/How_To/Car-Following_Model.html)

---

## VISSIM Integration (Wiedemann-99 Model)

VISSIM supports the **Wiedemann-99 car-following model**, allowing for **custom driver models**.

### **Steps to Integrate Wiedemann-99 in VISSIM**
1. **Open PTV VISSIM**.
2. **Build the road network** and configure the simulation.
3. **Set Personalized Driving Model**:
   - Open **Visual Studio** and compile the driver model:
     ```bash
     Open car_follow_model.vcxproj and build
     ```
   - This generates a **DriverModel.dll** file.
4. **Load the Driver Model in VISSIM**:
   - Open the **Vehicle Types** interface.
   - Add four vehicle types and link the **DLL file**.
   - Set **External Driver Model** and browse to the `DriverModel.dll` file.
5. **Run the Simulation**:
   - Configure evaluation settings in **Evaluation-Configuration**.
   - Start the VISSIM simulation.

🔗 [Official Wiedemann-99 Documentation](https://www.ptvgroup.com)

---

## AI-Based Model Integration (TorchScript)

For deep learning-based models, Open-PAV supports **TorchScript inference models**.

### **Steps to Deploy AI-Based Car-Following Models**
1. **Train a Neural Network-Based Model** using PyTorch.
   ```python
   import torch

   class CarFollowingModel(torch.nn.Module):
       def __init__(self):
           super().__init__()
           self.linear = torch.nn.Linear(4, 1)

       def forward(self, x):
           return self.linear(x)

   model = CarFollowingModel()
   torch.save(model, "car_following_model.pt")
   ```
2. **Convert to TorchScript for Deployment**:
   ```python
   model = torch.jit.script(model)
   model.save("car_following_model_scripted.pt")
   ```
3. **Run AI-Based Simulation**:
   ```python
   model = torch.jit.load("car_following_model_scripted.pt")
   input_data = torch.tensor([[v_l, v_f, p_l, p_f]])  # Example inputs
   predicted_acceleration = model(input_data)
   ```

This approach allows **AI-enhanced car-following models** to be deployed efficiently.

---

