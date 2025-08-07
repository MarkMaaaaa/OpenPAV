# Vehicle and Model Selection

Use the form below to select your vehicle **brand**, **model**, and **algorithm type**. Then, click the **Download** button to get the corresponding parameter file.

<form id="modelForm">
  <label for="brand">Select Vehicle Brand:</label>
  <select id="brand" required onchange="updateModels()">
    <option value="">--Select--</option>
    <option value="Tesla">Tesla</option>
    <option value="Audi">Audi</option>
    <option value="BMW">BMW</option>
    <option value="General">All Models</option>
  </select>

  <br/><br/>

  <label for="vehicle">Select Vehicle Model:</label>
  <select id="vehicle" required onchange="updateDownloadButton()">
    <option value="">--Select a Brand First--</option>
  </select>

  <br/><br/>

  <label for="algorithm">Select Algorithm Model:</label>
  <select id="algorithm" required onchange="updateDownloadButton()">
    <option value="">--Select--</option>
    <option value="Linear">Basic Linear Model</option>
    <option value="IDM">IDM for SUMO</option>
    <option value="Wiedemann-99">Wiedemann-99 for Vissim</option>
  </select>

  <br/><br/>

  <div id="downloadButtonContainer">
    <!-- Download button will be inserted here dynamically -->
  </div>
</form>

<script>
const vehicleModels = {
  "Tesla": ["Model 3", "Model S", "Model X"],
  "Audi": ["A4", "A6", "A8", "E-tron"],
  "BMW": ["X5", "I3"],
  "General": ["All Available Models"]
};

function updateModels() {
  const brand = document.getElementById("brand").value;
  const vehicleSelect = document.getElementById("vehicle");

  // Clear previous options
  vehicleSelect.innerHTML = "";

  if (brand && vehicleModels[brand]) {
    vehicleModels[brand].forEach(model => {
      const option = document.createElement("option");
      option.value = model.toLowerCase().replace(" ", "_"); // Ensure consistency with file naming
      option.textContent = model;
      vehicleSelect.appendChild(option);
    });
  } else {
    const option = document.createElement("option");
    option.value = "";
    option.textContent = "--Select a Brand First--";
    vehicleSelect.appendChild(option);
  }
}

function updateDownloadButton() {
  const vehicle = document.getElementById("vehicle").value;
  const algorithm = document.getElementById("algorithm").value;
  const downloadContainer = document.getElementById("downloadButtonContainer");

  // Clear previous button
  downloadContainer.innerHTML = "";

  if (vehicle && algorithm) {
    // Define file formats based on the selected algorithm
    const fileMap = {
      "Linear": `vp_linear_${vehicle}.json`,
      "IDM": `idm_${vehicle}.json`,
      "Wiedemann-99": `vissim_${vehicle}.json`
    };

    const fileName = fileMap[algorithm];

    // Create a download button
    const button = document.createElement("button");
    button.textContent = `Download ${algorithm} Model`;
    button.style = "display: block; margin-top: 10px; padding: 8px 12px; font-size: 14px;";
    button.onclick = function () {
      const link = document.createElement("a");
      link.href = `sandbox:/mnt/data/${fileName}`;
      link.download = fileName;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    };

    downloadContainer.appendChild(button);
  }
}
</script>
