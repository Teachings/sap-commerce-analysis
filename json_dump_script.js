// Function to trigger download of a file
function downloadFile(content, filename, contentType) {
    const a = document.createElement('a');
    const file = new Blob([content], { type: contentType });
    a.href = URL.createObjectURL(file);
    a.download = filename;
    a.click();
}

// Select the table by its ID
const table = document.getElementById('props');

// Get all rows in the tbody of the table
const rows = table.querySelectorAll('tbody tr');

// Initialize an object to hold key-value pairs
let properties = {};

// Iterate over the rows
rows.forEach(row => {
  // Select the Key and Value columns (assuming Key is in the first <td> and Value in the second <td>)
  const key = row.querySelector('td:nth-child(1)').innerText.trim();
  const value = row.querySelector('td:nth-child(2) input').value.trim();
  
  // Assign the key-value pair to the object
  properties[key] = value;
});

// Convert the properties object to a JSON string
const jsonDump = JSON.stringify(properties, null, 2);

// Prompt for the environment name
const envName = prompt("Enter the environment name (e.g., 'dev', 'prod'):");

// Generate a filename with the environment name
const filename = `config_${envName}.json`;

// Trigger the download of the JSON file
downloadFile(jsonDump, filename, 'application/json');
