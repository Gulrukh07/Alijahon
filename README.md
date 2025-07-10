
# 🛍️ Alijahon – E-Commerce Platform

**Alijahon** is a modern and scalable e-commerce web application built using Django. It supports multiple user roles and provides functionality for product management, ordering, and delivery processes.

## 🚀 Features

- 👤 **User Roles**: Customers, Admins, Operators, Delivery Agents
- 📦 **Product Catalog**: Browse, view, and manage products
- 🛒 **Cart & Checkout**: Add products to cart and place orders
- 🧾 **Order Management**: Track order status and delivery
- 🔐 **Authentication & Authorization**: Role-based access with secure login
- 📂 **Admin Dashboard**: Manage users, products, and orders
- 🖼️ Clean and organized UI built with Django templates

## 🛠️ Tech Stack

- **Backend**: Django 4+
- **Database**: SQLite (can be upgraded to PostgreSQL/MySQL)
- **Frontend**: HTML5, CSS3, Bootstrap
- **Architecture**: Django Class-Based Views, reusable templates, modular apps

```
## 📁 Project Structure



alijahon/
├── accounts/           # User registration, login, and roles
├── products/           # Product listing and management
├── orders/             # Order processing and delivery tracking
├── templates/          # All HTML templates
├── static/             # CSS and JS files
├── manage.py
└── ...

````

## ⚙️ Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Gulrukh07/Alijahon.git
   cd Alijahon


2. **Set up a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**:

   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**:

   ```bash
   python manage.py runserver
   ```


## 🧠 Highlights

* Separation of concerns with apps for accounts, products, and orders
* Reusable templates and views
* Clean code structure for maintainability
* Easily extendable for:

    * Payment integration
    * Inventory tracking
    * REST APIs (with Django REST Framework)



## 🙋‍♀️ Author

Developed by [Gulrukh Khayrullaeva](https://github.com/Gulrukh07)
Feel free to connect and give feedback!

