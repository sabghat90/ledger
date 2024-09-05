# Ledger Core

This project is a comprehensive Ledger Management System built with Django and PostgreSQL. It facilitates seamless management of financial transactions and accounts. The system provides functionalities for creating, managing, and tracking orders, accounts, and agents.

## Features

- **Order Management:** Create, update, delete, and track orders.
- **Account Management:** Manage financial accounts and track transactions.
- **Agent Management:** Create and manage agents.
- **User Authentication:** Secure user authentication and authorization.
- **Responsive Design:** Mobile-friendly interface.

## Technology Stack

- **Backend:** Django
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, JavaScript
- **Environment:** Virtual Environment with `venv`
- **Deployment:** WSGI with Gunicorn

## Installation

### Prerequisites

- Python 3.x
- PostgreSQL
- Git

### Steps

1. **Clone the repository:**
    ```bash
    git clone https://github.com/sabghat90/ledger_core.git
    cd ledger_core
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Setup the PostgreSQL database:**
    - Create a PostgreSQL database.
    - Update `settings.py` with your database credentials.

5. **Apply the migrations:**
    ```bash
    python manage.py migrate
    ```

6. **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

## Usage

- Access the application at `http://127.0.0.1:8000/`.
- Login as superuser to access the admin interface at `http://127.0.0.1:8000/admin/`.

## Project Structure

```plaintext
ledger_core/
├── ledger/                # Application code for ledger management
├── ledger_core/           # Project configuration and settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── templates/             # HTML templates
├── static/                # Static files (CSS, JavaScript, images)
├── .venv/                 # Virtual environment
├── manage.py
└── requirements.txt       # Python dependencies
```

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or issues, please contact:

- **Name**: Sabghat
- **Email**: [sabghat90@gmail.com](mailto:sabghat90@gmail.com)
- **GitHub**: [sabghat90](https://github.com/sabghat90)