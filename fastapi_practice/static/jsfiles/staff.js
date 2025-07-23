// Close dropdown when clicking outside



        const userData = {
            registrationID: 'USER-2023-04852',
            loginTimestamp: new Date().toISOString(),
            loginStatus: 'active'
        };
        // Logout function
        function logout() {
            showAlert("You have successfully logged out.");
            // Update login status
            userData.loginStatus = 'inactive';

            // Log to console
            console.group('User  Logout Details');
            console.log('Registration ID:', userData.registrationID);
            console.log('Login Timestamp:', userData.loginTimestamp);
            console.log('Login Status:', userData.loginStatus);
            console.groupEnd();
        }



        function setActiveMenuItem(activeItemId) {
            const menuItems = document.querySelectorAll('.menu-item');
            menuItems.forEach(item => {
                item.classList.remove('active'); // Remove active class from all items
            });
            document.getElementById(activeItemId).classList.add('active'); // Add active class to the clicked item
        }


        document.getElementById('addProductMenu').addEventListener('click', function () {
            setActiveMenuItem('addProductMenu');
            document.getElementById('addProductForm').style.display = 'block';
            document.getElementById('UpdateProductForm').style.display = 'none';
            document.getElementById('dashboardContent').style.display = 'none'; // Hide dashboard content
            document.getElementById('viewProductsSection').style.display = 'none'; // HIDE view products
            document.getElementById('salesHistorySection').style.display = 'none';
            document.getElementById('sellProductForm').style.display = 'none';
            document.getElementById('saleBillSection').style.display = 'none';
            document.getElementById('product-cards-view').style.display = 'none';
            document.getElementById('inventoryHistorySection').style.display = 'none';
            document.getElementById('updateProductSection').style.display = 'none';
            // document.getElementById('dashboard-section').style.display = 'none';
        });
        document.getElementById('UpdateProductForm').addEventListener('click', function () {
            setActiveMenuItem('UpdateProductForm');
            document.getElementById('addProductForm').style.display = 'none';
            document.getElementById('UpdateProductForm').style.display = 'block';
            document.getElementById('dashboardContent').style.display = 'none'; // Hide dashboard content
            document.getElementById('viewProductsSection').style.display = 'none'; // HIDE view products
            document.getElementById('salesHistorySection').style.display = 'none';
            document.getElementById('sellProductForm').style.display = 'none';
            document.getElementById('saleBillSection').style.display = 'none';
            document.getElementById('product-cards-view').style.display = 'none';
            // document.getElementById('dashboard-section').style.display = 'none';
        });

        document.getElementById('restockProducts').addEventListener('click', function () {
            setActiveMenuItem('restockProducts');
            document.getElementById('addProductForm').style.display = 'none';
            document.getElementById('UpdateProductForm').style.display = 'none';
            document.getElementById('inventoryHistorySection').style.display = 'none';
            document.getElementById('restockProducts').style.display = 'block';
            document.getElementById('dashboardContent').style.display = 'none'; // Hide dashboard content
            document.getElementById('viewProductsSection').style.display = 'none'; // HIDE view products
            document.getElementById('salesHistorySection').style.display = 'none';
            document.getElementById('sellProductForm').style.display = 'none';
            document.getElementById('saleBillSection').style.display = 'none';
            document.getElementById('product-cards-view').style.display = 'none';
            document.getElementById('updateProductSection').style.display = 'none';
            // document.getElementById('dashboard-section').style.display = 'none';
        });

        document.getElementById('viewProductsMenu').addEventListener('click', function () {
            setActiveMenuItem('viewProductsMenu');
            document.getElementById('dashboardContent').style.display = 'none';
            document.getElementById('UpdateProductForm').style.display = 'none';
            document.getElementById('inventoryHistorySection').style.display = 'none';
            document.getElementById('addProductForm').style.display = 'none';
            document.getElementById('viewProductsSection').style.display = 'none';
            document.getElementById('updateProductSection').style.display = 'none';
            document.getElementById('product-cards-view').style.display = 'block';
            document.getElementById('salesHistorySection').style.display = 'none';
            document.getElementById('sellProductForm').style.display = 'none';
            document.getElementById('saleBillSection').style.display = 'none';
        });

        document.getElementById('saleProducts').addEventListener('click', function () {
            setActiveMenuItem('saleProducts');
            document.getElementById('dashboardContent').style.display = 'none';
            document.getElementById('addProductForm').style.display = 'none';
            document.getElementById('UpdateProductForm').style.display = 'none';
            document.getElementById('inventoryHistorySection').style.display = 'none';
            document.getElementById('viewProductsSection').style.display = 'block';
            document.getElementById('product-cards-view').style.display = 'none';
            document.getElementById('salesHistorySection').style.display = 'none';
            document.getElementById('sellProductForm').style.display = 'none';
            document.getElementById('saleBillSection').style.display = 'none';
            document.getElementById('updateProductSection').style.display = 'none';
        });

        function openSellForm(productId, name, description, price) {
            document.getElementById('sellProductId').value = productId;
            document.getElementById('UpdateProductForm').style.display = 'none';

            document.getElementById('sellProductName').value = name;
            document.getElementById('sellDescription').value = description;
            document.getElementById('sellPrice').value = price;
            document.getElementById('sellQuantity').value = '';
            document.getElementById('totalCost').value = '';

            document.getElementById('viewProductsSection').style.display = 'none';
            document.getElementById('sellProductForm').style.display = 'block';
            document.getElementById('saleBillSection').style.display = 'none';
        }

        function calculateTotal() {
            const quantity = parseInt(document.getElementById('sellQuantity').value);
            const price = parseFloat(document.getElementById('sellPrice').value);
            if (!isNaN(quantity) && !isNaN(price)) {
                document.getElementById('totalCost').value = quantity * price;
            }
        }

        function cancelSell() {
            document.getElementById('sellProductForm').style.display = 'none';
            document.getElementById('viewProductsSection').style.display = 'block';
        }

        function generateBill() {

            const BuyersName = document.getElementById('BuyersName').value;
            console.log(BuyersName, "Buyers Information")
            const productId = document.getElementById('sellProductId').value;
            const name = document.getElementById('sellProductName').value;
            const desc = document.getElementById('sellDescription').value;
            const price = document.getElementById('sellPrice').value;
            const quantity = document.getElementById('sellQuantity').value;
            const manufactureDate = document.getElementById('manufactureDate').value;
            const totalCost = document.getElementById('totalCost').value;

            document.getElementById('billBuyersName').innerText = BuyersName;

            document.getElementById('billProductId').innerText = productId;
            document.getElementById('billManufactureDate').innerText = manufactureDate;
            document.getElementById('billSaleId').innerText = 'SALE' + Math.floor(Math.random() * 10000);
            document.getElementById('billSaleDate').innerText = new Date().toISOString().split('T')[0];
            document.getElementById('billProductName').innerText = name;
            document.getElementById('billDescription').innerText = desc;
            document.getElementById('billQuantity').innerText = quantity;
            document.getElementById('billTotalCost').innerText = totalCost;

            document.getElementById('sellProductForm').style.display = 'none';
            document.getElementById('saleBillSection').style.display = 'block';

            const invoiceData = {
                product_id: parseInt(document.getElementById('billProductId').innerText),
                user: document.getElementById('billBuyersName').innerText,
                quantity_sold: parseInt(document.getElementById('billQuantity').innerText),
                product_amt: parseInt(document.getElementById('billTotalCost').innerText)
            };
            console.log(invoiceData, "invoiceData");

            // Send data to FastAPI
            fetch('/save_invoice/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(invoiceData)
            }).then(response => {
                if (!response.ok) {
                    console.error('Failed to save invoice');
                }
            });

        }

        function downloadBillPDF() {
            const element = document.getElementById('saleBillSection');
            const opt = {
                margin: 1,
                filename: 'sale_bill_' + Date.now() + '.pdf',
                html2canvas: { scale: 2 },
                jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
            };

            html2pdf().set(opt).from(element).save();


        }

        function openRestockForm(productId) {
            const productName = "iPhone 16";
            const productDesc = "Latest Apple model";


            document.getElementById('restockProductId').value = productId;
            document.getElementById('restockProductName').value = productName;
            document.getElementById('restockProductDesc').value = productDesc;

            document.getElementById('viewProductsSection').style.display = 'none';
            document.getElementById('restockFormSection').style.display = 'block';
        }


        function generateRestock() {
            const productId = document.getElementById('restockProductId').value;
            const quantity = document.getElementById('restockQuantity').value;
            console.log(quantity, "Hello")

            fetch('/save_restock/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    product_id: parseInt(productId),
                    quantity: parseInt(quantity)
                })

            })
                .then(response => {
                    if (response.ok) {
                        alert('Restock successful!');

                        document.getElementById('restockFormSection').style.display = 'none';
                        document.getElementById('viewProductsSection').style.display = 'block';

                    } else {
                        alert('Failed to restock.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }


        function cancelRestock() {
            document.getElementById('restockFormSection').style.display = 'none';
            document.getElementById('viewProductsSection').style.display = 'block';

        }


        document.getElementById('dashboardMenu').addEventListener('click', function () {
            setActiveMenuItem('dashboardMenu');
            document.getElementById('addProductForm').style.display = 'none'; // Hide add product form
            document.getElementById('product-cards-view').style.display = 'none';
            document.getElementById('dashboardContent').style.display = 'block'; // Show dashboard content
            document.getElementById('viewProductsSection').style.display = 'none';
            document.getElementById('salesHistorySection').style.display = 'none';
            document.getElementById('sellProductForm').style.display = 'none';
            document.getElementById('inventoryHistorySection').style.display = 'none';
            document.getElementById('UpdateProductForm').style.display = 'none';
            document.getElementById('saleBillSection').style.display = 'none';
            document.getElementById('product-cards-view').style.display = 'none';
            document.getElementById('updateProductSection').style.display = 'none';
        });
        document.getElementById('inventoryHistoryMenu').addEventListener('click', function () {
            setActiveMenuItem('inventoryHistoryMenu');
            document.getElementById('addProductForm').style.display = 'none';
            document.getElementById('dashboardContent').style.display = 'none'; // Hide dashboard content
            document.getElementById('viewProductsSection').style.display = 'none'; // HIDE view products
            document.getElementById('salesHistorySection').style.display = 'none';
            document.getElementById('inventoryHistorySection').style.display = 'block';
            document.getElementById('sellProductForm').style.display = 'none';
            document.getElementById('saleBillSection').style.display = 'none';
            document.getElementById('product-cards-view').style.display = 'none';
            document.getElementById('UpdateProductForm').style.display = 'none';
            document.getElementById('updateProductSection').style.display = 'none';
            // document.getElementById('dashboard-section').style.display = 'none';
        });
        document.getElementById('salesHistoryMenu').addEventListener('click', function () {
            setActiveMenuItem('salesHistoryMenu');
            document.getElementById('dashboardContent').style.display = 'none';
            document.getElementById('product-cards-view').style.display = 'none';
            document.getElementById('UpdateProductForm').style.display = 'none';
            document.getElementById('addProductForm').style.display = 'none';
            document.getElementById('inventoryHistorySection').style.display = 'none';
            document.getElementById('viewProductsSection').style.display = 'none';
            document.getElementById('salesHistorySection').style.display = 'block';
            document.getElementById('sellProductForm').style.display = 'none';
            document.getElementById('saleBillSection').style.display = 'none';
            document.getElementById('updateProductSection').style.display = 'none';
        });



        function exportSalesToCSV() {
            const rows = document.querySelectorAll("#salesHistoryBody tr");
            let csvContent = "Sale ID,Sale Date,Name,Description,Quantity,Total Cost\n";

            rows.forEach(row => {
                const cols = row.querySelectorAll("td");
                const rowData = Array.from(cols).map(td => td.textContent.trim()).join(",");
                csvContent += rowData + "\n";
            });

            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement("a");
            link.setAttribute("href", URL.createObjectURL(blob));
            link.setAttribute("download", "sales_history_report.csv");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }


        // function showUpdateForm(productId) {
        //     console.log("Product to update:", productId);



        //     const form = document.getElementById("productForm");
        //     console.log(form, "Form");
        //     form.action = `http://127.0.0.1:8000/products/${productId}`;



        //     // Show the update form
        //     document.getElementById("UpdateProductForm").style.display = "block";

        //     // Optionally hide other sections if needed
        //     const viewSection = document.getElementById("viewProductsSection");
        //     if (viewSection) {
        //         viewSection.style.display = "none";
        //     }
        // }

        // Currently new code 
        // function showUpdateForm(productId) {
        //     const product = productsData[productId]; // Assume you exposed a productsData dictionary in your template
        //     console.log(product, 'producttkgjkttttttttttttttttt')
        //     document.getElementById("ProductName").value = product.product_name;
        //     document.getElementById("productDesc").value = product.description;
        //     document.getElementById("quantity").value = product.quantity;
        //     document.getElementById("price").value = product.price;

        //     const form = document.getElementById("productForm");
        //     form.action = `/products/${productId}`;
        //     document.getElementById("UpdateProductForm").style.display = "block";
        //     const viewSection = document.getElementById("viewProductsSection");
        //     if (viewSection) viewSection.style.display = "none";
        // }

        //     const productsData = {
        //     {% for product in products %}
        //     "{{ product.id }}": {
        //         product_name: "{{ product.product_name  }}",
        //             description: "{{ product.description }}",
        //                 quantity: { { product.quantity } },
        //         price: { { product.price } }
        //     } {% if not loop.last %}, {% endif %}
        //     {% endfor %}
        // };


        // function showProductUpdateForm(productId) {
        //     // const product = productsData[productId];
        //     // console.log(productsData, 'productdatattatatatattatat')
        //     if (!product) {
        //         console.error("No product found for ID:", productId);
        //         return;
        //     }

        //     document.getElementById("updateProductId").value = productId;
        //     document.getElementById("updateProductName").value = product.product_name;
        //     document.getElementById("updateProductDesc").value = product.description;

        //     // Default quantity to 0 or last value
        //     document.getElementById("updateQuantity").value = product.quantity;
        //     document.getElementById("updatePrice").value = product.price;

        //     document.getElementById("updateProductSection").style.display = "block";
        //     document.getElementById('dashboardContent').style.display = 'none';
        // }

        function showProductUpdateForm(productId, productName, productDesc, productQuantity, productPrice) {
            document.getElementById('updateProductId').value = productId;
            document.getElementById('updateProductName').value = productName;
            document.getElementById('updateProductDesc').value = productDesc;
            document.getElementById('updateQuantity').value = productQuantity;
            document.getElementById('updatePrice').value = productPrice;

            document.getElementById('product-cards-view').style.display = 'none';
            document.getElementById('updateProductSection').style.display = 'block';
        }


        function submitProductUpdate() {
            const productId = document.getElementById("updateProductId").value;
            const quantity = document.getElementById("updateQuantity").value;
            const price = document.getElementById("updatePrice").value;
            const name = document.getElementById("updateProductName").value;
            const description = document.getElementById("updateProductDesc").value;



            const formData = new FormData();
            formData.append("quantity", quantity);
            formData.append("price", price);
            formData.append("name", name);
            formData.append("description", description);

            fetch(`/update_products/${productId}`, {
                method: "POST",
                body: formData
            })
                .then(response => {
                    if (response.ok) {
                        alert("Product updated successfully!");
                        location.reload(); // Or re-render dynamically
                    } else {
                        alert("Failed to update product.");
                    }
                })
                .catch(error => console.error("Error:", error));
        }

        function cancelProductUpdate() {
            document.getElementById("updateProductSection").style.display = "block";
            // document.getElementById("dashboardContent").style.displayProductUpdate() 
            //     document.getElementById("updateProductSection").style.display = "none";
            //     document.getElementById("dashboardContent").style.display = "block";
            // }
            // `` = "block";
        }



        function cancelAddProduct() {
            document.getElementById("UpdateProductForm").style.display = "none";
        }

        function saveProduct() {
            const name = document.getElementById('productName').value;
            const desc = document.getElementById('productDesc').value;
            const quantity = document.getElementById('quantity').value;
            const price = document.getElementById('price').value;

            document.getElementById("confirmationMessage").innerText = `Confirm to add ${name}?`;
            document.getElementById("confirmationModal").style.display = "block";

            document.getElementById("confirmYesButton").onclick = function () {

                document.getElementById('addProductForm').style.display = 'none';
                document.getElementById('dashboardContent').style.display = 'block'; // Show dashboard content

                document.getElementById("confirmationModal").style.display = "none";
            };

            document.getElementById("confirmNoButton").onclick = function () {
                document.getElementById("confirmationModal").style.display = "none";
            };
        }



        function cancelAddProduct() {
            document.getElementById('productName').value = '';
            document.getElementById('productDesc').value = '';
            document.getElementById('quantity').value = '';
            document.getElementById('price').value = '';
            document.getElementById('addProductForm').style.display = 'block';
            document.querySelector('.dashboard-content').style.display = 'none';
        }