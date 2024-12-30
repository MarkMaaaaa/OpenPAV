# Open-PAV

Open-PAV (Open Producted Automated Vehicle) is an open platform designed to facilitate **data collection, model calibration, and simulation of automated vehicle behaviors**. It integrates diverse datasets and calibrated vehicle models, making it an essential tool for researchers and developers aiming to study product automated vehicle (PAV) dynamics and their impacts. The project encourages contributions from the research community and provides ready-to-use model parameters for seamless integration with simulation tools.

## Key Features

- **Comprehensive Dataset:**
  - Collects and organizes data from PAV, including LiDAR, images, videos, and trajectory data.
  - Provides datasets in a unified vectorized format for efficient access and analysis.

- **Kinematic Model Calibration:**
  - Supports linear models, IDM models (for SUMO), Wiedemann-99 (for Vissim), and machine learning-based models.
  - Includes pre-configured model parameters for direct use in traditional simulation software.

- **Simulation Integration:**
  - Enables rapid and accurate simulation of automated vehicle behavior and analysis of their impacts.

- **Community Collaboration:**
  - Designed to foster contributions and collaboration among researchers globally.

## What's New

### December 2024
- **Dataset Expansion:** Added new open-source trajectory datasets from ULTRA datasets.
- **Model Enhancements:** Improved basic logic for the project.

### November 2024
- **Project Startup:** Comprehensive installation and user guides are now available.


## Major Components

Open-PAV consists of the following components:

- **Data Repository:** A unified storage of diverse datasets (LiDAR, images, videos, trajectories).
- **Model Calibration Tools:** Utilities to calibrate vehicle kinematic models and export them for simulation.
- **Simulation Integration:** Pre-configured packages for SUMO, Vissim, and other platforms.
- **Scenario Manager:** Tools to create and manage simulation scenarios based on real-world data.

Check the [Open-PAV Documentation](https://open-pav-documentation.readthedocs.io/en/latest/) for more details.

## Get Started

### User Guide

- [Overview](https://open-pav-documentation.readthedocs.io/en/latest/overview.html)
- [Installation](https://open-pav-documentation.readthedocs.io/en/latest/installation.html)
- [Quick Start](https://open-pav-documentation.readthedocs.io/en/latest/quickstart.html)
- [Model Calibration](https://open-pav-documentation.readthedocs.io/en/latest/model_calibration.html)
- [Simulation Integration](https://open-pav-documentation.readthedocs.io/en/latest/simulation_integration.html)

### Developer Guide

- [API Reference](https://open-pav-documentation.readthedocs.io/en/latest/api.html)
- [Class Design](https://open-pav-documentation.readthedocs.io/en/latest/developer_tutorial.html)
- [Customizing Algorithms](https://open-pav-documentation.readthedocs.io/en/latest/customization.html)

## Contribution Rules

We welcome contributions to Open-PAV! Here’s how you can help:

- Report bugs and suggest improvements by submitting issues.
- Submit contributions via [pull requests](https://github.com/example/Open-PAV/pulls). Please use the provided [pull request template](.github/PR_TEMPLATE.md).

## Citation

If you use Open-PAV in your research or projects, please cite the following:

```bibtex
@inproceedings{openpav2024,
  title={Open-PAV: An Open Platform for Automated Vehicle Data and Model Integration},
  author={Your Name and Collaborators},
  booktitle={Proceedings of the International Conference on Automated Vehicle Research},
  year={2024},
  organization={Your Institution}
}





