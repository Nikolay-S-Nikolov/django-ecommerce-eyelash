function showToast(message, product = null) {
    const toast = document.getElementById("toast");
    const toastMsg = document.getElementById("toast-message");

    toastMsg.innerText = message;

    if (product) {
        document.getElementById("toast-product-name").innerText = product.name;
        document.getElementById("toast-product-price").innerText = "Цена: " + product.price + " лв";
        document.getElementById("toast-product-image").src = product.picture;
        document.getElementById("toast-product-link").href = "/product/" + product.slug + "/";
    }

    toast.style.display = "block";

    // setTimeout(() => {
    //     toast.style.display = "none";
    // }, 15000); // 5 секунди видимост
}

function addToCart(productId) {
    fetch(`/checkout/add_to_cart/${productId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
            "Content-Type": "application/json",
        },
        body: JSON.stringify({}),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast(data.message, data.product_details);
        } else {
            showToast("Грешка при добавяне в количката!");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        showToast("Сървърна грешка!");
    });
}

function hideToast(){
    const toast = document.getElementById("toast");
    toast.style.display = "none";
}
