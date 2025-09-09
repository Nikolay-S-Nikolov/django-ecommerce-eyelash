async function updateCartItem(cartItemId, quantity) {
    try {
        const res = await fetch(`/checkout/cart/${cartItemId}/update/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ quantity: quantity }),
        });

        const data = await res.json();

        if (data.success) {
            showTooltip(`#quantity-${cartItemId}`, data.message);
            document.querySelector(`#item-${cartItemId} .quantity-input`).value = data.product_details.quantity;
            document.querySelector(`#item-${cartItemId} .price`).innerText = data.product_details.total_price + " лв";
            document.querySelector(".total-price").innerText = data.product_details.cart_total + " лв";

        } else {
            alert(data.message);
            showTooltip(`#quantity-${cartItemId}`, data.message);
        }

    } catch (err) {
        console.error("Грешка при обновяване на количката:", err);
    }
}

function showTooltip(selector, message) {
    const input = document.querySelector(selector);
    let tooltip = input.parentElement.querySelector(".tooltip");

    if (!tooltip) {
        tooltip = document.createElement("div");
        tooltip.className = "tooltip";
        input.parentElement.appendChild(tooltip);
    }

    tooltip.textContent = message;
    tooltip.style.opacity = "1";

    setTimeout(() => {
        tooltip.style.opacity = "0";
    }, 5000); // скриване след 5 сек
}
