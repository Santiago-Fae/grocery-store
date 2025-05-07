# Grocery Store

A simple web application for managing grocery store products built with Django.

## Description

This is a Django-based web application for managing a grocery store's inventory. It allows for the creation, updating, viewing, and deletion of products, as well as customer basket management and purchase tracking.

## Features

- User authentication (customers and staff)
- Product inventory management (product ID, name, and price)
- Admin interface for product management
- Customer features:
  - Adding products to baskets
  - Viewing basket status
  - Viewing purchase history
- Staff features:
  - Adding/updating products
  - Approving or denying customer baskets
  - Querying customer information
  - Viewing customer purchase history

## Technologies Used

- Django 5.2
- Python
- SQLite database
- Bootstrap 5
- Font Awesome

## Getting Started

### Prerequisites

- Python 3.x
- pip

### Installation

1. Clone the repository
   ```
   git clone https://github.com/yourusername/grocery-store.git
   cd grocery-store
   ```

2. Create and activate a virtual environment
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Run migrations
   ```
   python manage.py migrate
   ```

5. Create a superuser for admin access
   ```
   python manage.py createsuperuser
   ```

6. Start the development server
   ```
   python manage.py runserver
   ```

7. Access the application at http://127.0.0.1:8000/

## Usage

### Customer Actions
- Register/login to your account
- Browse available products
- Add products to your basket
- View your basket status and purchase history

### Staff Actions
- Login as a staff member
- Add or update products
- View customer baskets
- Approve or deny customer baskets
- View customer information and purchase history

## License

This project is licensed under the MIT License.