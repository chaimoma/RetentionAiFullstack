async function displayHistory() {
    const tableBody = document.getElementById('history-table-body');
    
    tableBody.innerHTML = "<tr><td colspan='3'>Loading history...</td></tr>";
    
    try {
        const response = await fetch("http://localhost:8081/prediction-history", {
            method: "GET",
            headers: { 
                "Authorization": `Bearer ${getToken()}`,
                "Content-Type": "application/json"
            }
        });
        
        if (!response.ok) {
            if (response.status === 401) {
                throw new Error("Session expired. Please login again.");
            }
            throw new Error("Failed to fetch history data.");
        }

        const historyData = await response.json();

        // Clear the loading message
        tableBody.innerHTML = "";

        if (historyData.length === 0) {
            tableBody.innerHTML = "<tr><td colspan='3' style='text-align:center;'>No history found. Start by making a prediction!</td></tr>";
            return;
        }

        historyData.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

        historyData.forEach(item => {
            const date = new Date(item.timestamp).toLocaleString();
            
            // color better UX
            const probPercent = (item.probability * 100).toFixed(2);
            const color = item.probability > 0.5 ? "#e74c3c" : "#2ecc71"; // Red for high risk, Green for low

            const row = `
                <tr>
                    <td><strong>${item.employee_id}</strong></td>
                    <td style="color: ${color}; font-weight: bold;">${probPercent}%</td>
                    <td>${date}</td>
                </tr>
            `;
            tableBody.insertAdjacentHTML('beforeend', row);
        });

    } catch (error) {
        console.error("History Fetch Error:", error);
        tableBody.innerHTML = `<tr><td colspan='3' style='color:red;'>Error: ${error.message}</td></tr>`;
    }
}


if (!isLoggedIn()) {
    window.location.href = "index.html";
} else {
    document.addEventListener('DOMContentLoaded', displayHistory);
}