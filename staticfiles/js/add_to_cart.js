document.addEventListener("DOMContentLoaded", () => {
  const btns = document.querySelectorAll(".qty-btn");
  const input = document.getElementById("quantity");
  const min = parseInt(input.min, 10);
  const max = parseInt(input.max, 10);

  btns.forEach(btn => {
    btn.addEventListener("click", () => {
      let val = parseInt(input.value, 10) || min;
      if (btn.dataset.action === "increase" && val < max) {
        input.value = val + 1;
      }
      if (btn.dataset.action === "decrease" && val > min) {
        input.value = val - 1;
      }
    });
  });

  // Block Enter key to prevent form submission
  input.addEventListener("keydown", e => {
    if (e.key === "Enter") e.preventDefault();
  });

  // Validate input value on manual entry
  input.addEventListener("input", () => {
    let val = parseInt(input.value, 10) || min;
    if (val < min) input.value = min;
    if (val > max) input.value = max;
  });
});

// Note: Form submission handling is not included as the form 
// action is commented out in the HTML.

// Add additional functionality to dissable buttons at limits if needed.