// highlight

// Function to handle menu item clicks
    
// document.querySelectorAll('.sidebar-menu .menu-item a').forEach(link => {
//     link.addEventListener('click', function(event) {
//         event.preventDefault(); // Prevent navigation
//         const parent = this.closest('.menu-item');

//         document.querySelectorAll('.sidebar-menu .menu-item').forEach(menuItem => {
//             menuItem.classList.remove('active');
//         });

//         parent.classList.add('active');
//     });
// });


// sale js
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('sellModal');
    const sellButtons = document.querySelectorAll('.sell-btn');
    const confirmBtn = document.getElementById('confirmSale');

    // Open modal when clicking any Sell button
    sellButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            document.getElementById('sellProductId').value = productId;
            modal.style.display = 'block';
        });
    });

    
    // Close modal function
    window.closeSellModal = function() {
        modal.style.display = 'none';
    }

    // Event listener for closing modal
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            closeSellModal();
        }
    });

    // Confirm sale handler
    confirmBtn.addEventListener('click', function() {
        const quantity = document.getElementById('quantity').value;
        if (!quantity || quantity < 1) {
            alert('Please enter a valid quantity');
            return;
        }
        alert(`Sale confirmed for ${quantity} items of product ID: ${document.getElementById('sellProductId').value}`);
    });
});

// Generate Bill function
function generateBill() {
    const productId = document.getElementById('sellProductId').value;
    const quantity = document.getElementById('quantity').value;
    const user = document.getElementById('user').value; // Get the value of the user input

    // Populate bill details
    document.getElementById('billProductId').innerText = productId;
    document.getElementById('userID').innerText = user;
    document.getElementById('billSaleId').innerText = 'SALE' + Math.floor(Math.random() * 10000);
    document.getElementById('billSaleDate').innerText = new Date().toISOString().split('T')[0];
    document.getElementById('billProductName').innerText = 'iPhone 15'; // Replace with actual product name
    document.getElementById('billDescription').innerText = 'Latest Apple model'; // Replace with actual description
    document.getElementById('billQuantity').innerText = quantity;
    document.getElementById('billTotalCost').innerText = '₹' + (quantity * 89999); // Replace with actual price calculation

    // Hide products view and show bill
    document.getElementById('viewProductsSection').style.display = 'none'; // Hide the products view
    closeSellModal();
    document.getElementById('saleBillSection').style.display = 'block'; // Show the invoice
}

// Download Bill as PDF
function downloadBillPDF() {
    const element = document.getElementById('saleBillSection');
    const button = document.querySelector('.ok-button');
    button.style.display='none';
    const opt = {
        margin: 1,
        filename: 'sale_bill_' + Date.now() + '.pdf',
        html2canvas: { scale: 2 },
        jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
    };
    html2pdf().set(opt).from(element).save().then(() => {
        // Restore products view after download
        document.getElementById('viewProductsSection').style.display = 'block'; // Show the products view
        document.getElementById('saleBillSection').style.display = 'none'; // Hide the invoice
        button.style.display='block'; // restore after export
    });
}


// // restock js

// Function to open the restock modal
function openRestockForm() {
    document.getElementById('restockModal').style.display = 'block';
    // document.getElementById('restockQuantity').value = 1; // Reset quantity
    document.getElementById('restockError').style.display = 'none'; // Hide error message
}

// Function to close the restock modal
function closeRestockModal() {
    document.getElementById('restockModal').style.display = 'none';
}

// Function to handle confirm restock
function confirmRestock() {
    const quantityInput = document.getElementById('restockQuantity');
    const quantityError = document.getElementById('restockError');

    // Validate input
    if (!quantityInput.value || parseInt(quantityInput.value) < 1) {
        quantityError.style.display = 'block';
        return;
    }

    // Here you would typically send the restock data to your backend
    const quantity = parseInt(quantityInput.value);
    console.log(`Restocking ${quantity} items`); // Corrected variable name

    // Close the modal
    closeRestockModal();

    // Show success message (optional)
    alert(`Successfully restocked ${quantity} items`); // Corrected variable name
}

// Close modal when clicking outside of it
window.onclick = function(event) {
    const restockModal = document.getElementById('restockModal');
    if (event.target == restockModal) {
        closeRestockModal();
    }
}
