# BrandBazaar — Modern Full-Stack E-Commerce Platform

> **"Discover Your Style. Shop Your World."**  
> A complete, production-ready, full-stack multi-category e-commerce web application tailored for the Indian retail market, built with Python, Django 5.1, SQLite/PostgreSQL, and modern Bootstrap 5 responsive UI.

---

## 🌟 Key Highlights & Architecture

- **Full-Stack Django Integration:** Traditional, robust Django Template Language (DTL) frontend integrated with full Django ORM models and server-side ModelForm validation.
- **Hierarchical Category Engine:** Supports deep category nesting:
  - *Clothes* &rarr; *Men* / *Women* / *Kids* &rarr; *Jeans*, *Shirts*, *T-Shirts*, *Jackets*, *Hoodies*, *Shorts*, *Accessories*.
  - *Footwear* &rarr; *Men's Footwear* / *Women's Footwear* &rarr; *Sneakers*, *Running*, *Formals*, *Heels*.
  - *Beauty & Personal Care* &rarr; *Skincare*, *Haircare*, *Makeup*, *Fragrances*.
  - *Electronics* &rarr; *Audio & Headphones*, *Smartwatches & Wearables*, *Mobile Accessories*.
- **Brand Catalog Management:** Multi-brand architecture (Levi's, Nike, Puma, Sony, boAt, Samsung, Zara, Allen Solly, L'Oréal, Maybelline) with official brand storefront pages.
- **Dynamic Product Filtering & Sorting:** Real-time database queries by Category, Brand, Price Range, and In-Stock status, plus sorting by Newest, Price (Low &rarr; High, High &rarr; Low), and Name.
- **Session & Persistent Carts:** Seamless guest-to-authenticated cart merging upon login with server-enforced stock limits.
- **Wishlist System:** One-click wishlist toggling, duplicate prevention, and direct "Move to Cart" workflow.
- **Secure Checkout & Order Snapshots:** 
  - Server recalculates all product prices and order totals—never trusts client values.
  - Automatically preserves product name and unit price historical snapshots at the time of purchase.
  - Decrements live inventory from Products and Variants upon confirmed order placement.
  - User order cancellation with automatic inventory restoration.
- **Modular Payment Integration:** Safe Cash on Delivery (COD) flow and clearly labeled Sandbox Test Gateway for development, architected for plug-and-play Razorpay production integration.
- **Strict Privacy & Ownership:** Users can only view and manage their own orders and profile data.
- **Automated Test Suite:** 23 comprehensive tests covering core flows, catalog search, filters, authentication, cart inventory limits, order placement, and authorization checks.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend Framework** | Python 3.12, Django 5.1 |
| **Database** | SQLite 3 (Development default), PostgreSQL-ready for Production |
| **API / Endpoints** | Django REST Framework 3.15 |
| **Imaging Engine** | Pillow 13.0 |
| **Frontend UI** | HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3, Bootstrap Icons |
| **Config & Security** | `python-dotenv`, Django CSRF protection, PBKDF2 SHA-256 password hashing |

---

## 📁 Project Directory Structure

```text
mybrandbazaar/
├── manage.py                     # Django management utility
├── requirements.txt              # Production & development dependencies
├── .env.example                  # Environment variable template
├── .gitignore                    # Git ignore file
├── config/                       # Core Django project configuration
│   ├── settings.py               # Global settings, apps, middleware, databases
│   ├── urls.py                   # Root URL routing, static/media serving
│   ├── wsgi.py / asgi.py         # Deployment gateways
├── apps/                         # Modular Django applications
│   ├── core/                     # Home, About, Contact, Policies, 404, Newsletter
│   ├── catalog/                  # Category, Brand, Product, Variant, Search, Reviews
│   ├── accounts/                 # UserProfile, Register, Login, Profile updates
│   ├── cart/                     # Cart, CartItem, stock checks, session merge
│   ├── wishlist/                 # Wishlist, WishlistItem, Move-to-cart
│   └── orders/                   # Checkout, Order snapshots, Order tracking, Cancel
├── templates/                    # Modular Django Template Language files
│   ├── base.html                 # Master layout (Bootstrap 5, CDN, meta tags)
│   ├── includes/                 # Reusable components (Navbar, Footer, Messages)
│   ├── core/                     # Informational pages & Home
│   ├── catalog/                  # Product grid, Category detail, Brand detail, Search
│   ├── accounts/                 # Login, Register, Profile
│   ├── cart/                     # Shopping cart table & subtotal box
│   ├── wishlist/                 # Wishlist grid
│   └── orders/                   # Checkout form, Success confirmation, History, Detail
├── static/                       # Static assets
│   ├── css/                      # Custom design system & responsive styling
│   └── js/                       # Client interactions (Gallery, cart quantity, toasts)
└── media/                        # User uploads & generated placeholder SVGs
    ├── categories/
    ├── brands/
    └── products/
```

### Purpose of Each Application
- **`apps.core`**: Manages universal marketing pages (Home hero banner, brand partner showcases, customer benefits), contact forms, FAQ accordion, legal drafts, and newsletter signups.
- **`apps.catalog`**: Manages categories (with recursive self-referencing tree), brands, products, product variants (sizes/colors), image galleries, and real buyer reviews.
- **`apps.accounts`**: Handles secure user registration, session authentication, profile editing, and default Indian shipping addresses.
- **`apps.cart`**: Manages guest session carts, authenticated user carts, live quantity adjustment, and stock validation.
- **`apps.wishlist`**: Allows customers to save items for later and move them into their shopping bag with a single click.
- **`apps.orders`**: Manages the complete checkout pipeline, order number generation (`BB-YYYYMMDD-XXXX`), line-item snapshots, stock deduction, and private user order history.

---

## 🚀 Setup & Installation Instructions (Windows PowerShell)

Follow these exact steps in your PowerShell terminal to set up and run BrandBazaar locally:

### Step 1: Open PowerShell in the project directory
```powershell
cd c:\Users\techno\Downloads\mybrandbazaar
```

### Step 2: Create and activate a Virtual Environment
```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```
*(If you encounter a script execution restriction, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first).*

### Step 3: Install Required Packages
```powershell
pip install -r requirements.txt
```

### Step 4: Run Database Migrations
Create the SQLite tables:
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Load Realistic Demo Data & Test Accounts
Run the built-in management command to seed categories, brands (Levi's, Nike, Puma, Sony, etc.), demo products with variants, and create demo user accounts:
```powershell
python manage.py load_demo_data
```

### Step 6: Start the Development Server
```powershell
python manage.py runserver
```
Visit **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your web browser.

---

## 🔑 Demo & Admin Credentials

When `python manage.py load_demo_data` is executed, the following pre-configured accounts are ready to use:

### 1. Store Administrator (Access to Django Admin)
- **URL:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Username:** `admin`
- **Password:** `Admin@12345`

### 2. Demo Customer (Pre-filled Shipping Address & Past Review)
- **URL:** [http://127.0.0.1:8000/accounts/login/](http://127.0.0.1:8000/accounts/login/)
- **Username:** `customer`
- **Password:** `Customer@12345`

*(You can also register brand-new customer accounts at any time via `/accounts/register/`).*

---

## 🧪 Running Automated Tests

Run the full suite of 23 automated tests to verify catalog filtering, stock management, cart calculations, orders, and authentication security:

```powershell
python manage.py test
```

Expected output:
```text
Found 23 test(s).
System check identified no issues (0 silenced).
.......................
----------------------------------------------------------------------
Ran 23 tests in 34.572s

OK
```

---

## 💳 Payment Gateway Architecture & Production Configuration

BrandBazaar utilizes a decoupled payment structure:
1. **Cash on Delivery (COD):** Fully functional out of the box with stock checks, order confirmation, and status updates.
2. **Sandbox Test Mode:** Included for development verification without charging real credit cards or UPI accounts.
3. **Production Razorpay Setup:** To connect real Indian payment processing:
   - Create a free account at [Razorpay Dashboard](https://dashboard.razorpay.com).
   - Add your API keys to `.env`:
     ```env
     RAZORPAY_KEY_ID=rzp_live_your_key_id
     RAZORPAY_KEY_SECRET=your_key_secret
     ```
   - In `apps/orders/views.py`, hook the Razorpay Client verification callback into `order.payment_status = 'paid'`.

---

## 🐘 Switching from SQLite to PostgreSQL

BrandBazaar is PostgreSQL-ready. In your `.env` file, simply configure:

```env
DB_ENGINE=postgresql
DB_NAME=brandbazaar_db
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
```
Install `psycopg2-binary` (`pip install psycopg2-binary`) and execute `python manage.py migrate`.

---

## 🛡️ Security Best Practices Implemented

- **CSRF Protection:** Active on all forms, login actions, cart modifications, and checkout requests.
- **Price Tampering Protection:** All line totals, subtotals, and order amounts are strictly computed on the server from database model values; browser submissions of total prices are ignored.
- **Stock Depletion Guards:** Inventory counts are decremented atomically inside database transactions. Users cannot order more units than exist in stock.
- **User Ownership Isolation:** Users are strictly forbidden from viewing another user's order details or order history.
- **Password Protection:** Standard Django PBKDF2 with SHA-256 password hashing.
