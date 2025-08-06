# Open-PAV

Open-PAV (Open Production Automated Vehicle) is an open platform designed to facilitate **data collection, model calibration, and simulation** of production automated vehicle (PAV) behaviors. It integrates diverse datasets and calibrated vehicle models, making it an essential tool for researchers and developers aiming to study PAV dynamics and their impacts. The project encourages contributions from the research community and provides ready-to-use model parameters for seamless integration with simulation tools.

## Key Features

**Comprehensive Data Repository**

- A comprehensive trajectory dataset has been compiled by six research teams, including the CATS Lab at UW–Madison, the VECTOR Center at Vanderbilt University, the ITS Lab at Florida Atlantic University, the European Commission’s Joint Research Centre, the UCLA Mobility Lab and Transportation Research Center, Waymo, and Argo AI. This dataset encompasses trajectory data from 14 AV brands and 33 AV models, drawn from 13 open-source AV datasets. All data have been converted into a unified vectorized format to enable efficient access and analysis.  [[Paper]](https://www.nature.com/articles/s41597-024-03795-y) [[Data]](https://github.com/CATS-Lab/Filed-Experiment-Data-ULTra-AV)
<img src="images/Dataset.png" alt="Major Components" width="600">

**AV Model Calibration**

- Supports linear models, IDM models (for SUMO), Wiedemann-99 (for Vissim), and machine learning-based models.
- Includes pre-configured model parameters for direct use in traditional simulation software.

**Multiple Simulator Integrations**

- Enables rapid and accurate simulation of automated vehicle behavior and analysis of their impacts.

**Community Collaboration**

- Designed to foster contributions and collaboration among researchers globally.

## What's New

**March 2025**

- Model Enhancements: Improved calibration modeling methodology.
- Simulation Integration: Configured packages for SUMO, VISSIM, and basic parameters for models.

**December 2024**

- Dataset Expansion: Added new open-source trajectory datasets from ULTRA datasets.
- Model Enhancements: Improved basic logic for the project.

**November 2024**

- Project Startup: Comprehensive installation and user guides are now available.

## Major Components

- **Data Repository**: A unified storage of diverse datasets (LiDAR, images, videos, trajectories).
- **Model Calibration Tools**: Utilities to calibrate vehicle kinematic models and export them for simulation.
- **Simulator Integration**: Pre-configured packages for SUMO, VISSIM, and other platforms.
<img src="images/Workflow.png" alt="Major Components" width="600">


For more details, refer to the [Open-PAV Documentation](#).

## Sponsors

![image-20250805211205549](C:\Users\zh200\AppData\Roaming\Typora\typora-user-images\image-20250805211205549.png)