-- BookStore Database Schema
-- Safe to upload to GitHub (no passwords or sensitive data)

-- Create the database
CREATE DATABASE IF NOT EXISTS library_db;
USE library_db;

-- Table: books_in_store
CREATE TABLE IF NOT EXISTS books_in_store (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    isbn VARCHAR(20) UNIQUE,
    genre VARCHAR(100),
    publication_year INT,
    quantity INT DEFAULT 0,
    price DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table: book_reservation
CREATE TABLE IF NOT EXISTS book_reservation (
    reservation_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    customer_email VARCHAR(255),
    reservation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date DATE NOT NULL,
    return_date DATE,
    status ENUM('active', 'returned', 'cancelled') DEFAULT 'active',
    FOREIGN KEY (book_id) REFERENCES books_in_store(book_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Sample book data
INSERT INTO books_in_store (title, author, isbn, genre, publication_year, quantity, price) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', '978-0743273565', 'Fiction', 1925, 5, 12.99),
('To Kill a Mockingbird', 'Harper Lee', '978-0061120084', 'Fiction', 1960, 5, 14.99),
('1984', 'George Orwell', '978-0451524935', 'Dystopian', 1949, 7, 11.99),
('Pride and Prejudice', 'Jane Austen', '978-0141439518', 'Romance', 1813, 5, 9.99),
('The Catcher in the Rye', 'J.D. Salinger', '978-0316769488', 'Fiction', 1951, 5, 13.99);
