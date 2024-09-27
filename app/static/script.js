document.getElementById("upload-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    // Get the files
    const file1 = document.getElementById("file1").files[0];
    const file2 = document.getElementById("file2").files[0];

    if (!file1 || !file2) {
        alert("Please upload both files.");
        return;
    }

    // Prepare form data
    const formData = new FormData();
    formData.append("file1", file1);
    formData.append("file2", file2);

    // Send request to the server
    const response = await fetch("/compare/", {
        method: "POST",
        body: formData,
    });

    // Handle the response
    const result = await response.json();
    displayResult(result);
});

// Function to display the result in the result div
function displayResult(result) {
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = '';

    if (result.error) {
        resultDiv.innerHTML = `<div class="alert alert-danger">${result.error}</div>`;
        return;
    }

    // Missing keys in Env 1
    if (result.missing_in_env1.length) {
        resultDiv.innerHTML += `<h4>Keys missing in Environment 1:</h4><ul class="list-group">`;
        result.missing_in_env1.forEach(key => {
            resultDiv.innerHTML += `<li class="list-group-item">${key}</li>`;
        });
        resultDiv.innerHTML += `</ul>`;
    }

    // Missing keys in Env 2
    if (result.missing_in_env2.length) {
        resultDiv.innerHTML += `<h4>Keys missing in Environment 2:</h4><ul class="list-group">`;
        result.missing_in_env2.forEach(key => {
            resultDiv.innerHTML += `<li class="list-group-item">${key}</li>`;
        });
        resultDiv.innerHTML += `</ul>`;
    }

    // Value differences
    if (Object.keys(result.value_differences).length) {
        resultDiv.innerHTML += `<h4>Keys with different values:</h4><ul class="list-group">`;
        for (const [key, values] of Object.entries(result.value_differences)) {
            resultDiv.innerHTML += `<li class="list-group-item">
                <strong>${key}</strong>: 
                <span class="badge bg-danger">Env 1: ${values.env1_value}</span> 
                <span class="badge bg-warning">Env 2: ${values.env2_value}</span>
            </li>`;
        }
        resultDiv.innerHTML += `</ul>`;
    }

    // Common keys (optional)
    if (result.common_keys.length) {
        resultDiv.innerHTML += `<h4>Common Keys:</h4><ul class="list-group">`;
        result.common_keys.forEach(key => {
            resultDiv.innerHTML += `<li class="list-group-item">${key}</li>`;
        });
        resultDiv.innerHTML += `</ul>`;
    }
}
