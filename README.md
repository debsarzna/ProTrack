<h1 align="center">ProTrack</h1>

## About

ProTrack lets you sign in, manage your product stock, manage the employees who can access the system, and keep an eye on everything through a live dashboard with a recent-activity feed.

Each part of the app (products, employees) lives in its own feature folder and is split into model, repository, service, and view layers. The interface and the database are kept apart, which keeps the code easy to read, test, and extend.

A default admin account is created automatically on first run, so you can log in right away.

<br>

<p align="center">
  <img src="screenshots/login.png" width="300" alt="ProTrack login screen">
  <img src="screenshots/dashboard.png" width="450" alt="ProTrack dashboard">
</p>

<br>

## Project Objectives

* Build a desktop application that manages products and employees with full Create, Read, Update, Delete, and Search operations
* Automatically show each product's stock status (In Stock, Low Stock, Out of Stock) from its quantity
* Protect access with a login system that stores passwords securely
* Record every add, update, and delete in an activity log
* Validate user input so bad data is rejected with clear messages
* Apply object-oriented programming and a layered design (model, repository, service, view) to keep the code organized and easy to extend

<br>

## Features

* Secure login with username and password
   * Passwords are never stored in plain text
* Product management: add, update, delete, and search products (name, price, quantity)
   * Automatic stock status (In Stock, Low Stock, Out of Stock) based on quantity
* Employee management: add, update, delete, and search employees
   * Usernames are unique
   * Leaving the password blank when editing keeps the current one
* Live dashboard with totals for products and employees
   * Breakdown of In Stock, Low Stock, and Out of Stock items
   * The 10 most recent actions at a glance
* Activity log that records every add, update, and delete with a timestamp
* Input validation with clear messages for negative prices or quantities, empty fields, and duplicate usernames
* Default admin account created automatically on first run

<p align="center">
  <img src="screenshots/product.png" height="300" alt="Products page">
  &nbsp;&nbsp;
  <img src="screenshots/employee.png" height="300" alt="Employee page">
</p>

## Technologies Used

| Category | Technology |
|----------|------------|
| Programming language | Python 3.10+ |
| GUI framework | PyQt6 |
| Database | SQLite (built into Python through the `sqlite3` module) |
| Other libraries and tools | hashlib, Git and GitHub |

## Project Structure

* **`main.py`**: starts the app and opens the login window
* **`database/`**: sets up the SQLite database and its connection
* **`windows/`**: the main windows of the app
   * `login_window.py`: the login page where employees sign in
   * `main_window.py`: the main page with the dashboard and the navigation to each feature
* **`features/`**: one folder for each part of the system
   * **`Product/`**: everything for managing products
      * `model.py`: defines the data (name, price, quantity)
      * `repository.py`: reads and writes the products in SQLite
      * `service.py`: checks input and works out the stock status
      * `view.py`: the PyQt6 products page
   * **`Employee/`**: everything for managing employees
      * `model.py`: defines the data (name, username, password)
      * `repository.py`: reads and writes the employees in SQLite
      * `service.py`: checks input, keeps usernames unique, and hashes passwords
      * `view.py`: the PyQt6 employees page


## Status

ProTrack is stable for everyday use as a small inventory and staff tracker. Here are some points you may have questions about:

* Database: SQLite, stored in a single local file. No server setup needed.
* Passwords: hashed before storage, never saved or logged in plain text.
* Stock status rules: Out of Stock at `0`, Low Stock at below `10`, In Stock above that.
* Multi-user access: designed for one machine at a time. It is not a networked multi-user system.
* Roles and permissions: not yet. Every employee who can sign in has the same access.
* Platforms: runs anywhere PyQt6 does (Windows, macOS, Linux).

## Roadmap

Planned improvements:

* Roles and permissions, so admins and regular staff have different access
* Export products and the activity log to CSV
* Low-stock alerts on the dashboard
* UI improvements:
   * Light and dark theme options
   * Cleaner, more consistent styling across all pages
   * Icons on buttons and sidebar items
   * Charts on the dashboard for stock status
   * Keyboard shortcuts for common actions
