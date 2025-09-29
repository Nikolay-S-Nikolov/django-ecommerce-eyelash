function evalXCookieConsent(script) {
  const src = script.getAttribute("src");
  if (src) {
    const newScript = document.createElement('script');
    newScript.src = src;
    newScript.async = true;
    document.head.appendChild(newScript);
  } else {
    const newScript = document.createElement('script');
    // textContent instead of eval
    newScript.textContent = script.innerHTML;
    document.head.appendChild(newScript);
  }
  if (script.parentNode) {
    script.parentNode.removeChild(script);
  }
}

function showCookieBar(options) {
  const defaults = {
    content: '',
    cookie_groups: [],
    cookie_decline: null,
    beforeDeclined: null
  };
  const opts = Object.assign({}, defaults, options);

  const wrapper = document.createElement('div');
  wrapper.innerHTML = opts.content;
  const content = wrapper.firstChild;

  const body = document.querySelector('body');
  body.appendChild(content);
  body.classList.add('with-cookie-bar');

  function getCookie(name) {
    const match = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return match ? match.pop() : '';
  }

  const acceptBtn = content.querySelector(".cc-cookie-accept");
  if (acceptBtn) {
    acceptBtn.addEventListener('click', (e) => {
      e.preventDefault();
      fetch(e.target.getAttribute("href"), {
        method: "POST",
        credentials: 'same-origin',
        headers: { 'X-CSRFToken': getCookie('csrftoken') }
      }).then(() => {
        content.style.display = "none";
        body.classList.remove('with-cookie-bar');
        const scripts = document.querySelectorAll("script[type='x/cookie_consent']");
        scripts.forEach((script) => {
          const varname = script.getAttribute('data-varname');
          if (opts.cookie_groups.indexOf(varname) !== -1) {
            evalXCookieConsent(script);
          }
        });
      });
    });
  }

  const declineBtn = content.querySelector(".cc-cookie-decline");
  if (declineBtn) {
    declineBtn.addEventListener('click', (e) => {
      e.preventDefault();
      if (typeof opts.beforeDeclined === "function") opts.beforeDeclined();
      fetch(e.target.getAttribute("href"), {
        method: "POST",
        credentials: 'same-origin',
        headers: { 'X-CSRFToken': getCookie('csrftoken') }
      }).then(() => {
        content.style.display = "none";
        body.classList.remove('with-cookie-bar');
        if (opts.cookie_decline) document.cookie = opts.cookie_decline;
      });
    });
  }
}
