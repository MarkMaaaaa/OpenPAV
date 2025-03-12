# Open-PAV

Open-PAV (Open Product Automated Vehicle) is an open platform designed to facilitate **data collection, model calibration, and simulation of producted automated vehicle behaviors**. It integrates diverse datasets and calibrated vehicle models, making it an essential tool for researchers and developers aiming to study product automated vehicle (PAV) dynamics and their impacts. The project encourages contributions from the research community and provides ready-to-use model parameters for seamless integration with simulation tools.

## Key Features

- **Comprehensive Dataset:**
  - Collects and organizes data from PAVs, including LiDAR, images, videos, and trajectory data (We have summarized 14 AV brands, 33 AV models in 13 Open-source AV Datasets from 6 AV Data Providers, [Dataset Publication](https://www.nature.com/articles/s41597-024-03795-y)).
<img src="docs/images/Dataset.png" alt="Major Components" width="600">
  - Provides datasets in a unified vectorized format for efficient access and analysis.

- **Kinematic Model Calibration:**
  - Supports linear models, IDM models (for SUMO), Wiedemann-99 (for Vissim), and machine learning-based models.
  - Includes pre-configured model parameters for direct use in traditional simulation software.

- **Simulation Integration:**
  - Enables rapid and accurate simulation of automated vehicle behavior and analysis of their impacts.

- **Community Collaboration:**
  - Designed to foster contributions and collaboration among researchers globally.

## What's New

### March 2025
- **Model Enhancements:** Improved calibration modeling methodology.
- **Simulation Integration:** Configured packages for SUMO, Vissim, and basic parameters for models.

### December 2024
- **Dataset Expansion:** Added new open-source trajectory datasets from ULTRA datasets.
- **Model Enhancements:** Improved basic logic for the project.

### November 2024
- **Project Startup:** Comprehensive installation and user guides are now available.


## Major Components

Open-PAV consists of the following components:

- **Data Repository:** A unified storage of diverse datasets (LiDAR, images, videos, trajectories).
- **Model Calibration:** Utilities to calibrate vehicle kinematic models and export them for simulation.
- **Simulation Integration:** Pre-configured packages for SUMO, Vissim, and other platforms.
<!-- **Scenario Manager:** Tools to create and manage simulation scenarios based on real-world data. -->
![Major Components](docs/images/Workflow.png)

Check the [Open-PAV Documentation](https://markmaaaaa.github.io/OpenPAV/) for more details.

## Get Started

### User Guide

- [Overview](https://markmaaaaa.github.io/OpenPAV/)
- [Installation](https://markmaaaaa.github.io/OpenPAV/installation/)
- [Quick Start](https://markmaaaaa.github.io/OpenPAV/quick_start/)
- [Model Calibration](https://markmaaaaa.github.io/OpenPAV/model_calibration/)
- [Simulation Integration](https://markmaaaaa.github.io/OpenPAV/simulation_integration/)
- [Model Download](https://markmaaaaa.github.io/OpenPAV/model_download/)

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

@article{ma2025automated,
  title={Automated vehicle microscopic energy consumption study (AV-Micro): Data collection and model development},
  author={Ma, Ke and Zhou, Hang and Liang, Zhaohui and Li, Xiaopeng},
  journal={Energy},
  pages={135096},
  year={2025},
  publisher={Elsevier}
}
```

## License

Open-PAV is released under the [MIT License](LICENSE). See the LICENSE file for details.

## Contributors

Open-PAV is developed and maintained by:([CATS Lab](https://catslab.engr.wisc.edu/, Founder: Xiaopeng Li (https://catslab.engr.wisc.edu/staff/xiaopengli/)))

### Project Lead:
- Ke Ma ([Homepage](https://markmaaaaa.github.io/KeMa.github.io/portfolio/))

### Team Members:
- Hang Zhou ([LinkedIn](https://linkedin.com/in/member-profile), [GitHub](https://github.com/member-profile))


### External Acknowledgements:
We would like to thank the collaborator Jinbiao Huo's effort in this project.


