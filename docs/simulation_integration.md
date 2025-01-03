# Simulation Integration

Integrate Open-PAV with various simulation platforms to simulate automated vehicle behaviors:

## Supported Platforms

- **SUMO**: Use IDM models with pre-configured parameters.
- **Vissim**: Utilize Wiedemann-99 models for accurate simulations.
- **Other Platforms**: Custom integration supported via exported model parameters.

## Integration Steps

1. **Model Calibration**: Ensure your vehicle model is calibrated. Refer to the [Model Calibration Guide](model_calibration.md).
2. **Parameter Export**: Export the calibrated parameters in the required format (e.g., original parameters, Vissim parameter file, SUMO parameter file).
3. **Simulation Setup**: Import the parameters into your simulation platform.
4. **Execution**: Run the simulation to analyze vehicle behaviors.

For comprehensive integration instructions, see the [Developer Guide](developer_guide.md).
