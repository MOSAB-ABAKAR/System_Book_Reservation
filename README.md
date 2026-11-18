# 📚 Book Store — Library Reservation System

A modern web application for browsing and reserving books from your library, built with **Flask** and connected to a **MySQL** database.

## Features

- **Browse books** — View all available books in a clean card-based grid layout
- **Book details** — See full information including genre, price, ISBN, and stock availability
- **Reserve books** — Fill out a simple form to reserve one or more copies
- **Manage reservations** — View all reservations with status tracking and cancel active ones
- **Stock management** — Automatically decreases stock when reserved, restores on cancellation
- **Responsive design** — Works on desktop and mobile devices

## Project Structure

```
BookStore/
├── app.py              # Main Flask application
├── .env                # Database credentials (do not commit)
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── templates/
│   ├── base.html       # Base layout with navigation
│   ├── index.html      # Book listing page
│   ├── book.html       # Book detail & reservation form
│   └── reservations.html  # All reservations table
└── static/
    └── css/
        └── style.css   # Modern responsive stylesheet
```

## Setup

### Prerequisites

- Python 3.8+
- MySQL server running with the `library_db` database

### Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure database:**
   
   Edit `.env` with your MySQL credentials:
   ```
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=library_db
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open in browser:**
   
   Navigate to `http://127.0.0.1:5000`

## Database Schema

The app expects these tables in `library_db`:

### `books_in_store`
| Column | Type | Description |
|--------|------|-------------|
| book_id | INT (PK) | Auto-increment primary key |
| title | VARCHAR(255) | Book title |
| author | VARCHAR(255) | Author name |
| isbn | VARCHAR(20) | ISBN number |
| genre | VARCHAR(100) | Book genre |
| publication_year | INT | Year published |
| quantity | INT | Available copies |
| price | DECIMAL(10,2) | Book price |

### `book_reservation`
| Column | Type | Description |
|--------|------|-------------|
| reservation_id | INT (PK) | Auto-increment primary key |
| book_id | INT (FK) | References books_in_store |
| customer_name | VARCHAR(255) | Customer's name |
| customer_email | VARCHAR(255) | Customer's email |
| reservation_date | TIMESTAMP | When reserved |
| due_date | DATE | Return due date (14 days) |
| status | ENUM | 'active', 'returned', 'cancelled' |

## Pages

| Route | Description |
|-------|-------------|
| `/` | Browse all books |
| `/book/<id>` | Book details & reservation form |
| `/my-reservations` | View and manage all reservations |
