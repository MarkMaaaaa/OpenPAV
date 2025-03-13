# Vehicle and Model Selection

Use the form below to select your vehicle **brand** and **model**, along with the desired **algorithm model** and **file type**. The generated file will be available for download.

<form id="modelForm">
  <label for="brand">Select Vehicle Brand:</label>
  <select id="brand" required onchange="updateModels()">
    <option value="">--Select--</option>
    <option value="Tesla">Tesla</option>
    <option value="Audi">Audi</option>
    <option value="BMW">BMW</option>
    <option value="Mercedes-Benz">Mercedes-Benz</option>
    <option value="Ford">Ford</option>
    <option value="Waymo">Waymo</option>
    <option value="Toyota">Toyota</option>
    <option value="KIA">KIA</option>
    <option value="Hyundai">Hyundai</option>
    <option value="Mitsubishi">Mitsubishi</option>
    <option value="Peugeot">Peugeot</option>
    <option value="Jaguar">Jaguar</option>
    <option value="Mazda">Mazda</option>
    <option value="Lincoln">Lincoln</option>
    <option value="General">All Models</option>
  </select>

  <br/><br/>

  <label for="vehicle">Select Vehicle Model:</label>
  <select id="vehicle" required>
    <option value="">--Select a Brand First--</option>
  </select>

  <br/><br/>

  <label for="algorithm">Select Algorithm Model:</label>
  <select id="algorithm" required>
    <option value="">--Select--</option>
    <option value="Linear">Basic Linear Model</option>
    <option value="IDM">Intelligent Driver Model (IDM)</option>
    <option value="Wiedemann-99">Wiedemann-99</option>
    <option value="AI-based Model">AI-based Model</option>
  </select>

  <br/><br/>

  <label for="filetype">Select Parameter File Type:</label>
  <select id="filetype" required>
    <option value="">--Select--</option>
    <option value="Original">Original Parameters</option>
    <option value="Vissim">Vissim Parameters</option>
    <option value="SUMO">SUMO Parameters</option>
    <option value="TorchScript">AI-based Parameters</option>
  </select>

  <br/><br/>

  <button type="submit">Download</button>
</form>

<script>
const vehicleModels = {
  "Tesla": ["Model 3", "Model S", "Model X"],
  "Audi": ["A4 Avant", "A6", "A8", "E-tron"],
  "BMW": ["X5", "I3 S"],
  "Mercedes-Benz": ["A-Class", "GLE 450 4Matic"],
  "Ford": ["Fusion", "S-Max"],
  "Waymo": ["Self-Driving Car"],
  "Toyota": ["Rav 4", "Corolla"],
  "KIA": ["Niro"],
  "Hyundai": ["Ioniq Hybrid"],
  "Mitsubishi": ["SpaceStar", "Outlander PHEV"],
  "Peugeot": ["5008 GT Line"],
  "Jaguar": ["I-Pace"],
  "Mazda": ["Mazda 3"],
  "Lincoln": ["MKZ"],
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
      option.value = model;
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

document.getElementById('modelForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const brand = document.getElementById('brand').value;
  const vehicle = document.getElementById('vehicle').value;
  const algorithm = document.getElementById('algorithm').value;
  const filetype = document.getElementById('filetype').value;

  // Prepare data
  const data = {
    brand: brand,
    vehicle: vehicle,
    algorithm: algorithm,
    filetype: filetype,
    timestamp: new Date().toISOString()
  };

  // Generate JSON file
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `${brand}-${vehicle}-${algorithm}-${filetype}-parameters.json`;
  document.body.appendChild(link);
  link.click();
  window.URL.revokeObjectURL(url);
});
</script>
