// static/js/product.js
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

let deleteId = null;
function showConfirmModal(id) {
  deleteId = id;
  document.getElementById("confirmDeleteModal").classList.remove("hidden");
}

function hideConfirmModal() {
  document.getElementById("confirmDeleteModal").classList.add("hidden");
  deleteId = null;
}

function showEditModal(product) {
    // Populate the form fields in your main.html modal
    document.getElementById("name").value = product.name;
    document.getElementById("price").value = product.price;
    document.getElementById("description").value = product.description;
    
    // Call the existing showModal function from main.html, passing the ID
    showModal(product.id); 
}

async function confirmDelete() {
    if (!deleteId) return;
    const response = await fetch(`/delete-product-ajax/${deleteId}/`, {
        method: "POST", // CHANGED FROM "DELETE" TO "POST"
        headers: { "X-CSRFToken": getCSRFToken() },
    });
    if (response.ok) {
        hideConfirmModal();
        // **UPDATED TOAST CALL**
        showToast("Product deleted successfully!", "Success");
        document.dispatchEvent(new Event("productAdded"));
    } else {
        // **UPDATED TOAST CALL**
        showToast("Failed to delete product.", "Error");
    }
}

function addRefreshButton() {
    // Find the "Create News by AJAX" button, which we will place our new button next to.
    const createButton = document.querySelector("button[onclick='showModal()']");

    if (!createButton) return; // Exit if the create button isn't found

    const refreshButton = document.createElement("button");
    refreshButton.innerText = "Refresh Products";
    // Use the same styles as your other buttons for a consistent look
    refreshButton.className = "inline-flex items-center px-4 py-2 bg-blue-600 text-white font-semibold rounded-md hover:bg-blue-700 transition-colors mb-4 ml-4";
    refreshButton.onclick = () => fetchProductsFromServer();

    // Insert the new refresh button immediately after the create button
    createButton.parentNode.insertBefore(refreshButton, createButton.nextSibling);
}

document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("confirmDeleteBtn");
  if (btn) btn.addEventListener("click", confirmDelete);
  addRefreshButton();
});