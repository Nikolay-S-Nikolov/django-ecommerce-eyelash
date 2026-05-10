# 💎 Lash Store — Django E-commerce for Handmade Eyelashes

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2.5-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![django-allauth](https://img.shields.io/badge/django--allauth-65.11-success)](https://docs.allauth.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)](./Dockerfile)

A full-stack Django web application for managing and selling handmade eyelash products. The store provides a complete e-commerce experience — product catalog, AJAX-powered shopping cart, multi-step checkout, order history, blog, and contact module — with email-only authentication, Google OAuth, and a fully translated UI in **Bulgarian**, **English**, and **German**.

---

## 📸 Screenshots

> _Add screenshots/GIFs of the storefront, product page, cart, and checkout flow here._

| Home | Product Detail | Cart & Checkout |
| :--: | :------------: | :-------------: |
| _placeholder_ | _placeholder_ | _placeholder_ |

---

## ✨ Features

### Storefront
- 🛍️ **Product catalog** with multiple images per product, slug-based URLs, stock tracking, and `units_sold` counter
- 🔍 Product list and detail views with image gallery
- 📰 **Blog** module with Markdown rendering, auto-generated slugs, and auto-excerpts
- 📞 **Contact** page with singleton `ContactInfo` and dynamic `SocialLink` icons (FontAwesome)
- 🌐 **Multilingual UI** — Bulgarian (default), German, English via `gettext_lazy` and `LocaleMiddleware`

### Shopping & Orders
- 🛒 **AJAX cart** — add/update/remove items without page reload
- 💳 **Checkout flow** — atomic order creation with stock decrement, price snapshotting (`saved_price`), and cart clearing
- 🚚 **Shipping address & payment method** — _Pay on delivery_ or _Bank transfer_
- 📧 **Order confirmation email** sent automatically (HTML template)
- 📜 **Order history** and detail view per authenticated user
- 🔒 **Validation rules** — bank-paid orders cannot move to `Processing` / `Completed` while unpaid

### Authentication & Accounts
- 🔑 **Email-only login** (no username field) via `django-allauth`
- ✉️ **Mandatory email verification** with code-based verification
- 🔁 **Password reset by code**
- 🌐 **Google OAuth** (Social Account) — Facebook scaffolded but disabled
- 👤 Custom `LashUser` model + extended `Profile` (one-to-one), `GetProfileIdMixin` helper for `select_related` access

### Compliance & UX
- 🍪 **Cookie consent banner** via `django-cookie-consent` with custom JS that gates third-party scripts
- 📝 **Markdown content** rendered safely through `django-markdownify` with a tag/attribute whitelist
- 🔔 Toast notifications for AJAX feedback (custom `toast.js`)

---

## 🧰 Tech Stack

| Layer | Technology |
| --- | --- |
| **Backend** | Python, Django 5.2.5 |
| **Database** | PostgreSQL (`psycopg2`) |
| **Auth** | `django-allauth` 65.11 (email + code login, Google OAuth) |
| **Frontend** | Django Templates, vanilla JavaScript, custom CSS |
| **Content** | `django-markdownify`, `Markdown`, `bleach` |
| **Config** | `django-environ` (`.env` driven) |
| **Compliance** | `django-cookie-consent` |
| **Imaging** | `Pillow` |
| **Slugs** | `python-slugify` |
| **i18n** | Django i18n (`bg`, `de`, `en`) |
| **Email** | SMTP (Gmail-compatible) |

---

## 🏗️ Architecture

The project package is `lash_store/`. All Django apps live as **sub-packages** inside it (`lash_store.accounts`, `lash_store.orders`, …) — not at the repository root. This keeps imports namespaced and avoids collisions with third-party packages.

### Apps

| App | Responsibility |
| --- | --- |
| `accounts` | Custom `LashUser` (email-only) + `Profile`, allauth integration, signals |
| `product` | Catalog: `Product` + `ProductImages`, slug auto-generation in `clean()` / `save()` |
| `orders` | `Cart` → `CartItem` (AJAX) → `Order` + `OrderItem` + `ShippingAddress`, checkout, email |
| `blog` | `BlogPost` + `BlogImage`, Markdown content, auto slug & excerpt |
| `contact` | `ContactInfo` (singleton-style) + `SocialLink` (icon-based) |
| `common` | Homepage and About page (template-only views, no models) |

### Key flows

**Order lifecycle**
```
Cart ─► CartItem (AJAX add/update/delete)
              │
              ▼
    CheckoutView creates ─► Order + OrderItem (snapshots saved_price)
                                │
                                ├─► decrement Product.stock
                                ├─► clear CartItem rows
                                └─► OrderConfirmationView ─► email user
```

**Authentication backends**
- `ModelBackend` — admin & permissions
- `allauth.account.auth_backends.AuthenticationBackend` — email login, code verification, Google OAuth

### Templates

All templates live at the **repository root** in `templates/` (not per-app). The structure mirrors the apps:

```
templates/
├── account/        # allauth overrides (login, signup, email, password reset)
├── accounts/       # custom Profile views
├── allauth/        # additional allauth overrides
├── blog/
├── contact/
├── cookie_consent/
├── email/          # transactional HTML emails (e.g. order_confirmation_email.html)
├── orders/         # cart, checkout, confirmation, history, details
├── partials/       # reusable fragments (toast, messages, form errors)
├── product/
├── socialaccount/
├── about/
├── base.html
└── index.html
```

### Static & Media

- **Static (development)**: `staticfiles/` (added to `STATICFILES_DIRS`)
- **Static (collected)**: `static_files/` (`STATIC_ROOT`)
- **Media uploads**: `media_images/` — products under `products/`, blog under `blog_images/`

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL 13+
- A Google Cloud OAuth client (Client ID + Secret) — required because settings load it eagerly
- An SMTP account (Gmail App Password works out of the box)

### 1. Clone and create a virtual environment
```bash
git clone https://github.com/Nikolay-S-Nikolov/django-ecommerce-eyelash.git
cd django-ecommerce-eyelash

python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy the template and edit values:

```bash
cp .env.example .env
```

See [`.env.example`](.env.example) for the full list with comments. Minimum required for local dev: `DB_*` vars, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`.

> ⚠️ **Note**: `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` are read directly inside `settings.py` and the project will not start if they are missing. For local development without OAuth, supply any non-empty placeholder string.

### 4. Database setup
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Compile translations (optional but recommended)
```bash
python manage.py compilemessages
```

### 6. Run the development server
```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** — you should see the storefront.

---

## 🔧 Development Workflow

### Common commands

```bash
# Run server
python manage.py runserver

# Migrations
python manage.py makemigrations
python manage.py migrate

# Static files (production)
python manage.py collectstatic

# Translations
python manage.py makemessages -l bg     # extract for Bulgarian
python manage.py makemessages -l de     # extract for German
python manage.py makemessages -l en     # extract for English
python manage.py compilemessages        # compile .po → .mo
```

### Testing

Tests live in the **top-level `tests/`** directory, organized by app and layer:

```
tests/
├── blog/       (models, views)
├── contact/    (forms, models, templates, views)
├── orders/     (forms, models, templates, views)
└── products/   (models, templates, views)
```

```bash
# Run the full test suite
python manage.py test

# Run a specific module
python manage.py test tests.orders.views.test_checkout_view

# Run by app subfolder
python manage.py test tests.blog
```

### Translations workflow

Translatable strings use `gettext_lazy` (`_("...")`). Locale `.po` / `.mo` files live in `locale/`. Default language is **Bulgarian** (`bg`). Switch via `/i18n/setlang/` (Django's built-in URL include).

---

## 📦 Build & Deployment

### Production checklist

| Setting | Production value |
| --- | --- |
| `DEBUG` | `False` |
| `SECRET_KEY` | Long random string from `get_random_secret_key()` |
| `ALLOWED_HOSTS` | Your domain(s), comma-separated |
| `ACCOUNT_DEFAULT_HTTP_PROTOCOL` | `https` |
| Static files | Served by **WhiteNoise** (already wired in middleware) |
| Media | Persistent volume or object storage (S3, GCS) for `media_images/` |
| WSGI | `lash_store.wsgi:application` via **Gunicorn** |
| Email | SMTP creds + `DEFAULT_FROM_EMAIL` validated |

### Run locally with Docker

```bash
# Build the image
docker build -t lash-store .

# Run (PostgreSQL must be reachable; example uses host network on Linux)
docker run --rm -p 8000:8000 --env-file .env lash-store
```

The image is multi-stage, runs as a non-root user, and bakes `collectstatic` at build time. Migrations run on container start.

---

## 🚂 Deploy to Railway (step-by-step)

[Railway](https://railway.com/) is the recommended target for this project: free tier, one-click PostgreSQL, automatic HTTPS, and native Dockerfile support. Total time: **~10 minutes**.

### Step 1 — Sign up & create a project

1. Sign in at **[railway.com](https://railway.com)** with GitHub.
2. Click **New Project** → **Deploy from GitHub repo** → select `django-ecommerce-eyelash`.
3. Railway will detect the `Dockerfile` and start the first build automatically.

### Step 2 — Add PostgreSQL

1. In the project dashboard, click **+ New** → **Database** → **Add PostgreSQL**.
2. Open the new **Postgres** service → **Variables** tab.
3. Note the connection variables Railway exposes (`PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`).

### Step 3 — Configure environment variables

Open your **web service → Variables** and add:

| Key | Value |
| --- | --- |
| `SECRET_KEY` | _generate a fresh random string_ |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-app.up.railway.app` (Railway domain) |
| `DB_NAME` | `${{Postgres.PGDATABASE}}` |
| `DB_USER` | `${{Postgres.PGUSER}}` |
| `DB_PASSWORD` | `${{Postgres.PGPASSWORD}}` |
| `DB_HOST` | `${{Postgres.PGHOST}}` |
| `DB_PORT` | `${{Postgres.PGPORT}}` |
| `EMAIL_HOST` | `smtp.gmail.com` |
| `EMAIL_HOST_USER` | _your sender email_ |
| `EMAIL_HOST_PASSWORD` | _SMTP app password_ |
| `GOOGLE_CLIENT_ID` | _from Google Cloud Console_ |
| `GOOGLE_CLIENT_SECRET` | _from Google Cloud Console_ |
| `ACCOUNT_DEFAULT_HTTP_PROTOCOL` | `https` |

> The `${{Postgres.PG*}}` syntax is a Railway **reference variable** — values stay in sync if the database is recreated.

### Step 4 — Generate a public domain

1. **Service → Settings → Networking → Generate Domain**.
2. Railway returns something like `lash-store-production.up.railway.app`.
3. Add this hostname to `ALLOWED_HOSTS` (Step 3) and redeploy if needed.

### Step 5 — Create a Django superuser

Open the service shell from the Railway UI (**⋮ → Shell**), or run via CLI:

```bash
railway run python manage.py createsuperuser
```

### Step 6 — Configure Google OAuth callback

In **Google Cloud Console → Credentials → OAuth 2.0 Client**, add the production redirect URI:

```
https://<your-app>.up.railway.app/accounts/google/login/callback/
```

### Step 7 — Verify

- Visit `https://<your-app>.up.railway.app/` — storefront should load.
- Visit `/admin/` and log in with your superuser.
- Place a test order to confirm the email flow works.

### Maintenance

- **Logs**: Service → **Deployments** → live tail.
- **Redeploy**: pushed commits to `main` trigger automatic builds.
- **Migrations**: run on container start (see `CMD` in `Dockerfile`). For zero-downtime, switch to a Railway _release command_ instead.
- **Media uploads**: Railway containers are ephemeral — attach a **Volume** to `/app/media_images/` or migrate to S3 for persistent uploads.

---

## ☁️ Other deployment options

| Platform | Best for |
| --- | --- |
| **Render** | Free tier alternative to Railway; native Dockerfile + managed Postgres |
| **Fly.io** | Edge deployment, multi-region, strong CLI workflow |
| **DigitalOcean App Platform** | Production workloads with predictable pricing |
| **VPS + Docker Compose** | Maximum control; demonstrates DevOps skills (Nginx + Let's Encrypt + volumes) |

---

## 🌐 URL Overview

| Path | Purpose |
| --- | --- |
| `/` | Homepage |
| `/about/` | About page |
| `/admin/` | Django admin |
| `/accounts/` | django-allauth (login, signup, password reset, social) |
| `/profile/` | User profile detail |
| `/profile/edit/` | Edit profile |
| `/i18n/` | Language switching |
| `/product/` | Product list |
| `/product/<slug>/` | Product detail |
| `/checkout/` | Checkout |
| `/checkout/cart/` | Cart summary |
| `/checkout/add_to_cart/<id>/` | AJAX add-to-cart |
| `/checkout/cart/<id>/update/` | AJAX update quantity |
| `/checkout/cart/<id>/delete/` | Remove cart item |
| `/checkout/orders/` | Order history |
| `/checkout/orders/<id>/` | Order details |
| `/checkout/confirmation/<id>/` | Order confirmation |
| `/contact/` | Contact page |
| `/blog/` | Blog list |
| `/blog/<slug>/` | Blog post detail |
| `/cookie_consent/` | Cookie consent endpoints |

---

## 🌳 Project Structure

```
django-ecommerce-eyelash/
├── lash_store/                # Project package
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py / asgi.py
│   ├── accounts/              # Custom user, profile, allauth glue
│   ├── blog/                  # Blog posts + images
│   ├── common/                # Home & About (template-only)
│   ├── contact/               # ContactInfo + SocialLink
│   ├── orders/                # Cart, Order, OrderItem, ShippingAddress
│   ├── product/               # Product + ProductImages
│   └── utils/
│       └── user_mixins.py     # GetProfileIdMixin
├── templates/                 # All HTML templates (root level)
├── staticfiles/               # Source static assets (CSS / JS / images)
├── tests/                     # Tests organized by app & layer
├── locale/                    # i18n .po / .mo files
├── media_images/              # User-uploaded product images
├── blog_images/               # User-uploaded blog images
├── manage.py
├── requirements.txt
├── LICENSE                    # AGPL-3.0
└── README.md
```

---

## 🔮 Future Improvements

- 💳 Online payment provider integration (Stripe / PayPal)
- 📊 Admin analytics dashboard (revenue, top products, low stock alerts)
- ⭐ Product reviews & ratings
- ❤️ Wishlist / favorites
- 🔍 Full-text product search and category filters
- 📧 Order status notifications beyond confirmation (shipped, delivered)
- 🧩 `docker-compose` for local Postgres + app dev
- 🧪 CI pipeline (GitHub Actions) for tests, linting, and migrations check
- 📁 Object-storage backend (S3) for media in production

---

## 🤝 Contributing

Contributions are welcome! To get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/awesome-thing`
3. Make your changes and add tests
4. Run the test suite: `python manage.py test`
5. Commit and push your branch
6. Open a Pull Request describing the change and the motivation

> 📋 A formal `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` are recommended additions but not yet present in this repo.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for full terms.

> The MIT License is a permissive license. You are free to use, modify, distribute, and sublicense the code for any purpose, provided that the original copyright notice and license text are retained.

---

## 👤 Author

**Nikolay S. Nikolov**

- GitHub: [@Nikolay-S-Nikolov](https://github.com/Nikolay-S-Nikolov)
- Email: nikolay.s.nikolov@gmail.com
- Project: [django-ecommerce-eyelash](https://github.com/Nikolay-S-Nikolov/django-ecommerce-eyelash)

---

<p align="center">Built with ❤️ using Django.</p>
