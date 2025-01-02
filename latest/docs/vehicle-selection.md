
# Vehicle and Model Selection

Use the form below to select your vehicle and algorithm model. The generated file will be available for download.

<form id="modelForm">
  <label for="vehicle">Select Vehicle Model:</label>
  <select id="vehicle" required>
    <option value="">--Select--</option>
    <option value="Tesla">Tesla</option>
    <option value="Audi">Audi</option>
    <option value="Benz">Benz</option>
  </select>

  <br/><br/>

  <label for="algorithm">Select Algorithm Model:</label>
  <select id="algorithm" required>
    <option value="">--Select--</option>
    <option value="IDM">Intelligent Driver Model (IDM)</option>
    <option value="Linear">Linear Model</option>
    <option value="ML">Machine Learning Model</option>
  </select>

  <br/><br/>

  <label for="filetype">Select Parameter File Type:</label>
  <select id="filetype" required>
    <option value="">--Select--</option>
    <option value="Original">Original Parameters</option>
    <option value="Vissim">Vissim Parameters</option>
    <option value="SUMO">SUMO Parameters</option>
  </select>

  <br/><br/>

  <button type="submit">Generate and Download</button>
</form>

<script>
document.getElementById('modelForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const vehicle = document.getElementById('vehicle').value;
  const algorithm = document.getElementById('algorithm').value;
  const filetype = document.getElementById('filetype').value;

  // Prepare data
  const data = {
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
  link.download = `${vehicle}-${algorithm}-${filetype}-parameters.json`;
  document.body.appendChild(link);
  link.click();
  window.URL.revokeObjectURL(url);
});
</script>
