# Seed Game Store

Seed Game Store is a web application developed using Django, designed for selling video games. It allows users to browse a game catalogue, purchase games, and play them directly in the browser. Developers can add their games to the store, set prices, and track sales statistics.

## Main Features

**For users:**

* Browse the game catalogue with filters and sorting.
* View detailed game information, including descriptions, screenshots, and videos.
* Purchase games online.
* Play games directly in the browser.
* Create an account and track purchase history.

**For developers:**

* Add and edit games in the catalogue.
* Set prices for games.
* View sales and revenue statistics.
* REST API for integration with other services.

## Technologies

**Backend:** Django (Python), SQLite

**Frontend:** HTML, CSS, JavaScript

**Cloud Storage:** Cloudinary

**Email:** Django SMTP

## Installation and Setup

1. Clone the repository:

``` Powershell
git clone https://github.com/your-username/seed-game-store.git
```

2. Create and activate a virtual environment:

``` Powershell
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows
```

3. Install dependencies:

``` Powershell
pip install -r requirements.txt
```

4. Apply database migrations:

``` Powershell
python manage.py migrate
```

5. Run the development server:

``` PowerShell
python manage.py runserver
```

6. Open your browser and go to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## License

This project is distributed under the MIT License.

## Contact Information

If you have any questions or suggestions, please contact us:

Email: [seedgamestore1@outlook.com](mailto:seedgamestore1@outlook.com)
