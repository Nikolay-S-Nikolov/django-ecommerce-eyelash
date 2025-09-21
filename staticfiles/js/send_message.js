const form = document.querySelector('.contact-form');
const url = form.dataset.url;
const csrfToken = form.dataset.csrf;
const spinner = document.getElementById('form-spinner');
const submitBtn = form.querySelector('input[type="submit"]');

function send_email(e) {
    e.preventDefault();
    spinner.style.display = 'flex';
    submitBtn.disabled = true;

    const formData = new FormData(form);

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        },
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            spinner.style.display = 'none';
            submitBtn.disabled = false;
            const messageBox = document.createElement('div');
            messageBox.className = data.success ? 'success' : 'error';
            messageBox.textContent = data.success ? data.message : 'Грешка при изпращане.';
            form.prepend(messageBox);

            if (data.success) {
                form.reset();
            }
        })
        .catch(error => {
            spinner.style.display = 'none';
            submitBtn.disabled = false;

            const errorBox = document.createElement('div');
            errorBox.className = 'error';
            errorBox.textContent = 'Грешка при изпращане.';
            form.prepend(errorBox);

            console.error('Грешка:', error);
        });
}

form.addEventListener('submit', send_email);