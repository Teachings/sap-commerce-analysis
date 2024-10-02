function compareFiles() {
    const file1 = document.getElementById('file1').files[0];
    const file2 = document.getElementById('file2').files[0];

    if (!file1 || !file2) {
        alert("Please upload both files.");
        return;
    }

    const formData = new FormData();
    formData.append("file1", file1);
    formData.append("file2", file2);

    // Display sections
    displaySection('/compare/missing-keys', formData, 'Missing Keys');
    displaySection('/compare/value-differences', formData, 'Value Differences');
    displaySection('/compare/common-keys', formData, 'Common Keys');
}

async function displaySection(url, formData, sectionTitle) {
    const response = await fetch(url, { method: 'POST', body: formData });
    const result = await response.json();

    const filterText = document.getElementById('filter').value.toLowerCase();
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML += `<h4>${sectionTitle}:</h4>`;
    let html = `<table class="table">`;

    if (sectionTitle === 'Missing Keys') {
        html += `<thead><tr><th>Missing Keys in Env1</th><th>Missing Keys in Env2</th></tr></thead><tbody>`;
        html += `<tr><td>`;
        result.missing_in_env1.forEach(key => {
            if (key.toLowerCase().includes(filterText)) {
                html += `${key}<br>`; // Use <br> to separate keys on new lines
            }
        });
        html += `</td><td>`;
        result.missing_in_env2.forEach(key => {
            if (key.toLowerCase().includes(filterText)) {
                html += `${key}<br>`; // Use <br> to separate keys on new lines
            }
        });
        html += `</td></tr>`;
    } else if (sectionTitle === 'Value Differences') {
        html += `<thead><tr><th>Key</th><th>Value in Env1</th><th>Value in Env2</th></tr></thead><tbody>`;
        Object.entries(result).forEach(([key, values]) => {
            if (key.toLowerCase().includes(filterText)) {
                html += `<tr><td>${key}</td><td>${values.env1_value || 'N/A'}</td><td>${values.env2_value || 'N/A'}</td></tr>`;
            }
        });
    } else if (sectionTitle === 'Common Keys') {
        html += `<thead><tr><th>Key</th><th>Value</th></tr></thead><tbody>`;
        Object.keys(result).forEach(key => {
            if (key.toLowerCase().includes(filterText)) {
                html += `<tr><td>${key}</td><td>${result[key]}</td></tr>`;
            }
        });
    }

    html += `</tbody></table>`;
    resultDiv.innerHTML += html;
}

