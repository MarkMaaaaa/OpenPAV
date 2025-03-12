# Quick Start

Get started with Open-PAV by following these steps:

**Installation**: Ensure Open-PAV is installed on your system. Refer to the [Installation Guide](installation.md) for instructions.

##Data Preparation
   - You can **use your own dataset** (LiDAR, images, videos, trajectory data) or  
   - **Use our pre-collected dataset** available in Open-PAV [Model Download](model_download.md) .

**Vehicle Selection**:  
   - Choose a vehicle brand and model (e.g., Tesla, Audi, Benz).

**Model Selection**:  
   - Select a simulation model type:  
     - **Basic Linear Model** (linear parameters).  
     - **IDM Model**.  
     - **Wiedemann-99 Model**.  
     - **AI-based model**.  

**Simulator File Format Selection**:  
   - Choose the output format for your simulator:  
     - **Basic parameters file** (generic format).  
     - **SUMO-compatible file**.  
     - **VISSIM-compatible file**.  
     - **TorchScript package** (for AI-based models).  

##Quick Start Example  
   As an example, we provide a **Basic Linear Model for a Tesla**, running in a simple highway simulation.  
   You can modify parameters and datasets to experiment with different configurations.  

   **Download Example Configuration File:**  
   <button id="downloadButton">Download Configuration</button>

   <script>
   document.getElementById("downloadButton").addEventListener("click", function () {
       const data = {
           "vehicle": "Audi A4",
           "model": "Linear",
           "filetype": "Original",
           "parameter": "kv=1.35, kg=2, td=2, z=-0.5",
           "timestamp": new Date().toISOString()
       };
       const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
       const url = window.URL.createObjectURL(blob);
       const link = document.createElement('a');
       link.href = url;
       link.download = "openpav_config.json";
       document.body.appendChild(link);
       link.click();
       window.URL.revokeObjectURL(url);
   });
   </script>

Then, run the script using Python:
```html
<p>
    <a href="car_following_sim.py" download>
        <button style="padding: 10px 15px; font-size: 16px; background-color: #007bff; color: white; border: none; border-radius: 5px;">
            📥 Download Python Script
        </button>
    </a>
</p>
