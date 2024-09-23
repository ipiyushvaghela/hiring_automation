// Fetch candidate data from the Flask API and generate the table
async function fetchCandidateData() {
    try {
        const response = await fetch('/api/candidates');
        const data = await response.json();
        generateTable(data);
    } catch (error) {
        console.error('Error fetching candidate data:', error);
    }
}

// Function to generate the table rows with checkboxes
function generateTable(candidateData) {
    const tableBody = document.getElementById('candidateTableBody');

    candidateData.forEach(profile => {
        const row = document.createElement('tr');

        // Checkbox column
        const selectCell = document.createElement('td');
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.value = profile[1]; // Set the email as the value
        console.log(checkbox.value)
        selectCell.appendChild(checkbox);
        row.appendChild(selectCell);

        // Other columns
        profile.forEach(item => {
            const cell = document.createElement('td');
            cell.textContent = item;
            row.appendChild(cell);
        });

        tableBody.appendChild(row);
    });
}
function sendEmails() {
    const selectedEmails = [];
    const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
    
    checkboxes.forEach(checkbox => {
        selectedEmails.push(checkbox.value);
    });

    if (selectedEmails.length > 0) {
        const formLink = "https://qz4atdkbo71.typeform.com/to/ztMqoegE";  // You can customize this form link

        // Make a POST request to Flask to call the Python function
        fetch('/send-emails', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ emails: selectedEmails, form_link: formLink })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);  // Show a success message
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } else {
        alert('No candidates selected!');
    }
}

// Fetch the candidate data when the page loads
window.onload = fetchCandidateData;
