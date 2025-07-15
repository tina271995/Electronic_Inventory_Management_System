document.addEventListener('DOMContentLoaded', function() {
    // Sales Line Chart
    new Chart(document.getElementById("lineChart"), {
    type: 'line',
    data: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [{
        label: 'Sales',
        data: [120, 150, 180, 130, 170, 220, 200],
        borderColor: 'blue',
        backgroundColor: 'rgba(0, 0, 255, 0.1)',
        fill: true,
        tension: 0.4
        }]
    },
    options: { plugins: { legend: { display: true } } }
    });

    // Stock Bar Chart
    new Chart(document.getElementById("barChart"), {
    type: 'bar',
    data: {
        labels: ['Laptop', 'Mouse', 'Phone', 'Tablet'],
        datasets: [{
        label: '',
        data: [30, 70, 50, 40],
        backgroundColor: ['#007bff', '#28a745', '#ffc107', '#dc3545']
        }]
    },
    options: {
        aspectRatio: 2, 
        // plugins: { legend: { display: true } },
        scales: { y: { beginAtZero: true } }
    }
    });
    
    // Sales Pie Chart
    new Chart(document.getElementById("pieChart"), {
        type: 'pie',
        data: {
        labels: ['Phone', 'Laptop', 'Watch'],
        datasets: [{
            label: 'Sales Share',
            data: [300, 200, 100],
            backgroundColor: ['#17a2b8', '#6f42c1', '#e83e8c']
        }]
    },
    options: {
        aspectRatio: 2, 
        plugins: { legend: { display: true, position: 'right' } }
    }
});
});

window.onload = function () {
    inventoryCharts();
};

// Inventory Charts on load
function inventoryCharts() {
    new Chart(document.getElementById("monthlyLineChart"), {
        type: 'line',
        data: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            datasets: [{
                label: 'Revenue',
                data: [30000, 40000, 45000, 50000],
                borderColor: 'blue',
                backgroundColor: 'rgba(0, 0, 255, 0.1)',
                tension: 0.3,
                fill: true
            }]
        },
        options: {
            plugins: { legend: { display: true } }
        }
    });

    new Chart(document.getElementById("topProductsBarChart"), {
        type: 'bar',
        data: {
            labels: ['Smart Watch', 'Speaker', 'Power Bank'],
            datasets: [{
                label: 'Units Sold',
                data: [150, 120, 90],
                backgroundColor: ['#007bff', '#28a745', '#ffc107']
            }]
        },
        options: {
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true } }
        }
    });
};

function showAlert(message) {
    document.getElementById("alertMessage").innerText = message;
    document.getElementById("alertModal").style.display = "block";
}

function closeModal() {
    document.getElementById("alertModal").style.display = "none";
}

document.addEventListener('click', function(event) {
    const dropdown = document.getElementById('userDropdown');
    const avatar = document.querySelector('.user-avatar');
    
    if (!avatar.contains(event.target) && !dropdown.contains(event.target)) {
        dropdown.classList.remove('active');
    }
});

function logout() {
    // Show a custom alert message instead of logging out
    showAlert("You have successfully logged out.");
}

function toggleDropdown() {
    var dropdown = document.getElementById("userDropdown");
    dropdown.classList.toggle("active");
}


// Function to set the active menu item
function setActiveMenuItem() {
    const currentPath = window.location.pathname.split('/').pop(); // Get the current page name
    const menuItems = document.querySelectorAll('.menu-item');

    menuItems.forEach(item => {
        const link = item.querySelector('a');
        if (link && link.getAttribute('href') === currentPath) {
            item.classList.add('active'); // Add active class to the current item
        } else {
            item.classList.remove('active'); // Remove active class from other items
        }
    });
}

function exportSalesToCSV1() {
    const rows = document.querySelectorAll("#salesHistoryBody tr");
    
    // Check if there are any rows to export
    if (rows.length === 0) {
        alert("No data available to export.");
        return;
    }

    let csvContent = "Sale ID,Sale Date,Name,Description,Quantity,Total Cost\n"; // CSV header

    rows.forEach(row => {
        const cols = row.querySelectorAll("td");
        const rowData = Array.from(cols).map(td => {
            // Escape double quotes and wrap in quotes if necessary
            const text = td.textContent.trim().replace(/"/g, '""');
            return `"${text}"`; // Wrap in quotes to handle commas in data
        }).join(",");
        csvContent += rowData + "\n"; // Add row to CSV content
    });

    // Create a Blob from the CSV content
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement("a");
    link.setAttribute("href", URL.createObjectURL(blob));
    link.setAttribute("download", "sales_history_report.csv");
    document.body.appendChild(link);
    link.click(); // Trigger the download
    document.body.removeChild(link); // Clean up
}


function exportSalesToCSV() {
    const rows = document.querySelectorAll("#InventorySectionBody tr");
    
    let csvContent = "Product ID,Name,Description,Quantity,Price\n"; // CSV header

    rows.forEach(row => {
        const cols = row.querySelectorAll("td");
        const rowData = Array.from(cols).map(td => {
            // Escape double quotes and wrap in quotes if necessary
            const text = td.textContent.trim().replace(/"/g, '""');
            return `"${text}"`; // Wrap in quotes to handle commas in data
        }).join(",");
        csvContent += rowData + "\n"; // Add row to CSV content
    });

    // Create a Blob from the CSV content
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement("a");
    link.setAttribute("href", URL.createObjectURL(blob));
    link.setAttribute("download", "inventory_report.csv");
    document.body.appendChild(link);
    link.click(); // Trigger the download
    document.body.removeChild(link); // Clean up
}

