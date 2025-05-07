# Grocery Store

A simple web application for managing grocery store products built with Django.

## Description

This is a Django-based web application for managing a grocery store's inventory. It allows for the creation, updating, viewing, and deletion of products.

## Features

- Product inventory management
- Admin interface for product management
- Basic CRUD operations for products

## Technologies Used

- Django 5.2
- Python
- SQLite database

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

5. Start the development server
   ```
   python manage.py runserver
   ```

6. Access the application at http://127.0.0.1:8000/

## License

This project is licensed under the MIT License.