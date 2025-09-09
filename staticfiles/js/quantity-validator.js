const quantityInputs = document.querySelectorAll(".quantity");

quantityInputs.forEach((quantityInput) => {
    const wrapper = quantityInput.closest(".cart-item-quantity-wrapper");
    const buttons = wrapper.querySelectorAll(".qty-btn");
    const stockMessage = wrapper.parentElement.querySelector(".stock-message");

    buttons.forEach((btn) => {
        btn.addEventListener("click", () => {
            const action = btn.getAttribute("data-action");
            const currentValue = parseInt(quantityInput.value, 10) || 1;
            const min = parseInt(quantityInput.min, 10);
            const max = parseInt(quantityInput.max, 10);

            let newValue = currentValue;

            if (action === "increase") {
                newValue = currentValue + 1;
            } else if (action === "decrease") {
                newValue = currentValue - 1;
            }

            if (newValue < min) {
                newValue = min;
            } else if (newValue > max) {
                newValue = max;
                stockMessage.style.display = "block";
                stockMessage.innerText = `В момента разполагаме само с ${max} бройки и не можете да поръчате повече.`;
            } else {
                stockMessage.style.display = "none";
                stockMessage.innerText = "";
            }

            quantityInput.value = newValue;
        });
    });
});
