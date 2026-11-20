import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from mysql.connector import pooling, Error as MySQLError
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database connection pool
db_pool = pooling.MySQLConnectionPool(
    pool_name="bookstore_pool",
    pool_size=5,
    pool_reset_session=True,
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
    database=os.getenv("DB_NAME", "library_db"),
)


def get_db():
    """Get a connection from the pool."""
    return db_pool.get_connection()


# ─── Routes ───────────────────────────────────────────────

@app.route("/")
def index():
    """Home page – show all books available in the store."""
    books = []
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books_in_store ORDER BY title")
        books = cursor.fetchall()
        for b in books:
            if hasattr(b.get('price'), '__float__'):
                b['price'] = float(b['price'])
        cursor.close()
        conn.close()
    except MySQLError as e:
        flash(f"Database error: {e}", "danger")
    return render_template("index.html", books=books)


@app.route("/book/<int:book_id>")
def book_detail(book_id):
    """Show a single book's details and booking form."""
    book = None
    reservations = []
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books_in_store WHERE book_id = %s", (book_id,))
        book = cursor.fetchone()
        if book:
            if hasattr(book.get('price'), '__float__'):
                book['price'] = float(book['price'])
            cursor.execute(
                "SELECT * FROM book_reservation WHERE book_id = %s ORDER BY reservation_date DESC",
                (book_id,),
            )
            reservations = cursor.fetchall()
        cursor.close()
        conn.close()
    except MySQLError as e:
        flash(f"Database error: {e}", "danger")

    if not book:
        flash("Book not found.", "warning")
        return redirect(url_for("index"))

    return render_template("book.html", book=book, reservations=reservations)


@app.route("/reserve", methods=["POST"])
def reserve_book():
    """Handle a new book reservation."""
    book_id = request.form.get("book_id", type=int)
    customer_name = request.form.get("customer_name", "").strip()
    customer_email = request.form.get("customer_email", "").strip()
    quantity = request.form.get("quantity", type=int, default=1)
    reservation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not customer_name or not customer_email:
        flash("Please enter your name and email.", "warning")
        return redirect(url_for("book_detail", book_id=book_id))

    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        # Check availability
        cursor.execute(
            "SELECT quantity FROM books_in_store WHERE book_id = %s", (book_id,)
        )
        book = cursor.fetchone()
        if not book:
            flash("Book not found.", "warning")
            cursor.close()
            conn.close()
            return redirect(url_for("index"))

        if book["quantity"] < quantity:
            flash(f"Only {book['quantity']} copies available.", "warning")
            cursor.close()
            conn.close()
            return redirect(url_for("book_detail", book_id=book_id))

        # Calculate due date (14 days from now)
        from datetime import timedelta
        due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

        # Insert reservation
        cursor.execute(
            """INSERT INTO book_reservation
               (book_id, customer_name, customer_email, reservation_date, due_date)
               VALUES (%s, %s, %s, %s, %s)""",
            (book_id, customer_name, customer_email, reservation_date, due_date),
        )

        # Decrease stock
        cursor.execute(
            "UPDATE books_in_store SET quantity = quantity - %s WHERE book_id = %s",
            (quantity, book_id),
        )

        conn.commit()
        cursor.close()
        conn.close()

        flash(f"Successfully reserved {quantity} book(s)!", "success")
    except MySQLError as e:
        flash(f"Reservation failed: {e}", "danger")

    return redirect(url_for("book_detail", book_id=book_id))


@app.route("/my-reservations")
def my_reservations():
    """Show all reservations (admin view)."""
    reservations = []
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """SELECT br.*, b.title, b.author
               FROM book_reservation br
               JOIN books_in_store b ON br.book_id = b.book_id
               ORDER BY br.reservation_date DESC"""
        )
        reservations = cursor.fetchall()
        cursor.close()
        conn.close()
    except MySQLError as e:
        flash(f"Database error: {e}", "danger")

    return render_template("reservations.html", reservations=reservations)


@app.route("/cancel/<int:reservation_id>", methods=["POST"])
def cancel_reservation(reservation_id):
    """Cancel a reservation and restore stock."""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT book_id FROM book_reservation WHERE reservation_id = %s",
            (reservation_id,),
        )
        res = cursor.fetchone()
        if not res:
            flash("Reservation not found.", "warning")
            cursor.close()
            conn.close()
            return redirect(url_for("my_reservations"))

        # Restore stock
        cursor.execute(
            "UPDATE books_in_store SET quantity = quantity + 1 WHERE book_id = %s",
            (res["book_id"],),
        )

        # Update reservation status to cancelled
        cursor.execute(
            "UPDATE book_reservation SET status = 'cancelled' WHERE reservation_id = %s",
            (reservation_id,),
        )

        conn.commit()
        cursor.close()
        conn.close()

        flash("Reservation cancelled. Stock restored.", "success")
    except MySQLError as e:
        flash(f"Cancel failed: {e}", "danger")

    return redirect(url_for("my_reservations"))


# ─── Run ──────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True, port=5000)
