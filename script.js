document.addEventListener("DOMContentLoaded", function() {
    const currentDataTableBody = document.querySelector("#current-data-table tbody");
    const historicalDataTableBody = document.querySelector("#historical-data-table tbody");
    const timeTravelDateInput = document.getElementById("time-travel-date");
    const loadHistoricalDataBtn = document.getElementById("load-historical-data");
    const timeTravelError = document.getElementById("time-travel-error");
    const ingestDataBtn = document.getElementById("ingest-data");
    const evolveSchemaBtn = document.getElementById("evolve-schema");
    const ingestionStatus = document.getElementById("ingestion-status");

    // Function to fetch and display current data
    async function fetchCurrentData() {
        try {
            const response = await fetch("/api/current_data");
            const data = await response.json();
            renderTable(currentDataTableBody, data);
        } catch (error) {
            console.error("Error fetching current data:", error);
            currentDataTableBody.innerHTML = `<tr><td colspan="3">Error loading current data.</td></tr>`;
        }
    }

    // Function to fetch and display historical data
    async function fetchHistoricalData(date) {
        timeTravelError.textContent = "";
        try {
            const response = await fetch(`/api/historical_data?date=${date}`);
            const data = await response.json();
            if (data.error) {
                timeTravelError.textContent = data.error;
                historicalDataTableBody.innerHTML = `<tr><td colspan="3"></td></tr>`;
            } else {
                renderTable(historicalDataTableBody, data);
            }
        } catch (error) {
            console.error("Error fetching historical data:", error);
            historicalDataTableBody.innerHTML = `<tr><td colspan="3">Error loading historical data.</td></tr>`;
        }
    }

    // Function to render data in a table
    function renderTable(tableBody, data) {
        tableBody.innerHTML = "";
        if (data.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="${Object.keys(data[0] || {}).length}">No data available.</td></tr>`;
            return;
        }
        // Create header if not present (for dynamic columns like 'Volume')
        const headerRow = document.createElement("tr");
        for (const key in data[0]) {
            const th = document.createElement("th");
            th.textContent = key.charAt(0).toUpperCase() + key.slice(1); // Capitalize first letter
            headerRow.appendChild(th);
        }
        if (tableBody.previousElementSibling.tagName === "THEAD") {
            tableBody.previousElementSibling.innerHTML = ""; // Clear existing header
            tableBody.previousElementSibling.appendChild(headerRow);
        }

        data.forEach(row => {
            const tr = document.createElement("tr");
            for (const key in row) {
                const td = document.createElement("td");
                td.textContent = row[key];
                tr.appendChild(td);
            }
            tableBody.appendChild(tr);
        });
    }

    // Event listeners
    loadHistoricalDataBtn.addEventListener("click", function() {
        const selectedDate = timeTravelDateInput.value;
        if (selectedDate) {
            fetchHistoricalData(selectedDate);
        } else {
            timeTravelError.textContent = "Please select a date.";
        }
    });

    ingestDataBtn.addEventListener("click", async function() {
        ingestionStatus.textContent = "Ingesting new data...";
        try {
            const response = await fetch("/api/ingest_data", { method: "POST" });
            const result = await response.json();
            ingestionStatus.textContent = result.message;
            fetchCurrentData(); // Refresh current data after ingestion
        } catch (error) {
            console.error("Error ingesting data:", error);
            ingestionStatus.textContent = "Error during data ingestion.";
        }
    });

    evolveSchemaBtn.addEventListener("click", async function() {
        ingestionStatus.textContent = "Evolving schema...";
        try {
            const response = await fetch("/api/evolve_schema", { method: "POST" });
            const result = await response.json();
            ingestionStatus.textContent = result.message;
            fetchCurrentData(); // Refresh current data after schema evolution
        } catch (error) {
            console.error("Error evolving schema:", error);
            ingestionStatus.textContent = "Error during schema evolution.";
        }
    });

    // Initial data load
    fetchCurrentData();
});

