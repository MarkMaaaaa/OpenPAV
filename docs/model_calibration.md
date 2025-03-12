# Model Calibration

Open-PAV provides tools for calibrating various vehicle kinematic models to improve the accuracy of automated vehicle behavior simulations.

## Three-Stage Car-Following Model

The Adaptive Cruise Control (ACC) system in automated vehicles (AVs) consists of two subsystems:

1. **Upper Command Control System** – Generates acceleration commands based on sensor data.
2. **Lower Motion Response System** – Regulates acceleration in response to commands.

To account for real-world system delays, the **Three-Stage Car-Following Model** incorporates:
- **Stage 1: Sensor Perception Delay (\(\eta_{a,1}\))** – The time required for the vehicle to detect and process leading vehicle data.
- **Stage 2: Control Computation Delay (\(\eta_{a,2}\))** – The time taken to compute acceleration commands.
- **Stage 3: Vehicle Response Lag (\(\eta_b\))** – The mechanical delay in executing the acceleration.

### **Mathematical Formulation**
At any given time \( t \), let:
- \( p_i(t) \), \( v_i(t) \), and \( a_i(t) \) be the position, velocity, and acceleration of the **following vehicle**.
- \( p_{i+1}(t) \), \( v_{i+1}(t) \), and \( a_{i+1}(t) \) be the position, velocity, and acceleration of the **preceding vehicle**.
- \( s_i(t) = (p_i(t), v_i(t), a_i(t)) \) represent the **state** of the following vehicle.

The command acceleration at time \( t_0 + \eta_{a,1} + \eta_{a,2} \) is computed as:

$$
u_i(t_0 + \eta_{a,1} + \eta_{a,2}) = g(v_i(t_0), v_{i+1}(t_0), p_i(t_0), p_{i+1}(t_0); \theta_C)
$$

where:
- \( g(\cdot) \) is a **control law function**.
- \( \theta_C \) represents the **control parameters** to be calibrated.

In **Stage 3**, due to the **response lag** \( \eta_b \), the acceleration is modeled as a **first-order system**:

$$
\eta_b \frac{d a_i(t)}{dt} + a_i(t) = u_i(t)
$$

Thus, the **state-space representation** of the system is:

$$
\dot{s}_i(t) = A_i s_i(t) + B_i u_i(t)
$$

where:

$$
A =
\begin{bmatrix}
0 & 1 & 0 \\
0 & 0 & 1 \\
0 & 0 & -\frac{1}{\eta_b}
\end{bmatrix}, \quad
B =
\begin{bmatrix}
0 \\
0 \\
\frac{1}{\eta_b}
\end{bmatrix}
$$

The calibrated control function is:

$$
u_i(t) = g(v_i(t - \eta_a), v_{i+1}(t - \eta_a), p_i(t - \eta_a), p_{i+1}(t - \eta_a); \theta_C)
$$

where \( \eta_a = \eta_{a,1} + \eta_{a,2} \) represents the **total control delay**.

---

## Hybrid Parameter Calibration Method

To calibrate model parameters, Open-PAV implements a **hybrid optimization algorithm** that combines:

1. **Bayesian Optimization (BO)** – Efficient global search for optimal delay parameters (\(\eta_a, \eta_b\)).
2. **Simultaneous Perturbation Stochastic Approximation (SPSA)** – Fast local optimization for control gains (\(\theta_C\)).

### **Mathematical Formulation of Calibration**
The calibration problem is defined as an **optimization problem**:

$$
\min_{\theta} f(\theta, D^{m}, D^{r})
$$

where:
- \( \theta \) is the **parameter set to be calibrated**.
- \( D^m \) is the **model-predicted vehicle states**.
- \( D^r \) is the **real-world vehicle data**.

The objective function \( f(\cdot) \) is based on the **Root Mean Square Error (RMSE)**:

$$
f(\theta, D^{m}, D^{r}) = \sqrt{\frac{1}{N} \sum_{j=1}^{N} \left( a_{i,m}(t_j | \theta) - a_{i,r}(t_j) \right)^2 }
$$

where:
- \( a_{i,m}(t_j | \theta) \) is the **model-predicted acceleration**.
- \( a_{i,r}(t_j) \) is the **real observed acceleration** at time \( t_j \).

### **Calibration Process**
1. **Data Input** – Load collected vehicle trajectory data.
2. **Parameter Adjustment** – Optimize both delay and control parameters using BO + SPSA.
3. **Validation** – Compare calibrated model outputs with real-world observations.
4. **Export** – Save parameters in a compatible format for SUMO, VISSIM, or other simulators.

---

## Supported Models

- **Linear Models** – Suitable for basic simulations.
- **IDM Models** – Ideal for SUMO simulations.
- **Wiedemann-99** – Compatible with VISSIM.
- **Machine Learning-Based Models** – For advanced simulations.
