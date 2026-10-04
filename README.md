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
   * `main_window.py`: the main page with the navigation to each feature
* **`features/`**: one folder for each part of the system
   * **`Dashboard/`**: the overview page with totals and recent activity
      * `repository.py`: reads the product and employee counts, the stock status counts, and the activity log
      * `service.py`: prepares the numbers and the 10 most recent actions for display
      * `view.py`: the PyQt6 dashboard page
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

## Installation and Setup

### Requirements

* Python 3.10 or newer
* Git (to download the project)
* Dependencies:
   * **PyQt6**: the GUI framework
   * **SQLite**: the database, which is built into Python, so you don't need to install it

### Steps

1. **Download the project**

```bash
   git clone https://github.com/<your-username>/ProTrack.git
   cd ProTrack
```

2. **Create a virtual environment** (recommended)

```bash
   python -m venv venv
```

3. **Activate the virtual environment**

   * Windows:

```bash
     venv\Scripts\activate
```

   * macOS/Linux:

```bash
     source venv/bin/activate
```

4. **Install the dependencies**

```bash
   pip install PyQt6
```

5. **Run the application**

```bash
   python main.py
```

6. **Log in**

   On first run, ProTrack creates the database and a default admin account. Sign in with:

   * Username: `admin`
   * Password: `admin123`

   Change this password after your first login.

## How to Use the System

1. **Log in**
   * Start the app and enter your username and password, then click Login.
   * On first run, use the default admin account.

2. **View the dashboard**
   * After login, the dashboard shows the totals for products and employees.
   * It also shows how many items are In Stock, Low Stock, and Out of Stock, and the 10 most recent actions.

3. **Manage products**
   * Open the Products page.
   * To add a product, enter the name, price, and quantity, then click Add.
   * To update or delete a product, select it in the table, make your changes, then click Update or Delete.
   * To find a product, type its name in the search box.
   * The stock status updates automatically from the quantity.

4. **Manage employees**
   * Open the Employees page.
   * To add an employee, fill in the details and a unique username, then click Add.
   * To update or delete an employee, select them in the table, then click Update or Delete.
   * When editing, leave the password blank to keep the current one.
   * To find an employee, type a name or username in the search box.

5. **Check recent activity**
   * Every add, update, and delete appears in the recent-activity feed on the dashboard, with a timestamp.

6. **Log out**
   * Click Logout when you are done.
  
## OOP Implementation

### Important classes and objects

* **Database layer**
   * `Database`: opens the SQLite connection and creates the `products` and `employees` tables
   * `ActivityLog`: creates the `activity_log` table, saves each action, and returns the most recent ones. The app uses one shared object, `activity_log`.
* **Model classes**: objects that hold the data
   * `Product`: name, price, quantity, status, and id
   * `Employee`: first name, username, and password hash
* **Repository classes**: objects that run the SQL queries
   * `ProductRepository`: add, list, search, update, delete
   * `EmployeeRepository`: add, list, search, get by username, update, delete
* **Service classes**: objects that apply the rules and record activity
   * `ProductService`: add, get, search, update, and delete products
   * `EmployeeService`: add, update, and delete employees, check unique usernames, hash passwords, log in, and create the default admin
* **View classes**: the PyQt6 windows and pages
   * `loginwindow`: the login page
   * `mainwindow`: the main page, with the sidebar menu and the stacked pages
   * `HoverMenu`: the sidebar menu that opens when the mouse hovers over it
   * `Dashboard`: totals, stock status counts, and recent activity
   * `ProductPage` and `AddProductDialog`: the products table and its add/update form
   * `EmployeePage` and `EmployeeDialog`: the employees table and its add/update form

### Encapsulation

Each class keeps its data and behavior together and hides the details from the other layers.

* `Database` hides the file path and connection. Other classes only call `connect()`.
* All SQL lives inside the repository classes. The views never run queries.
* `ProductService` and `EmployeeService` each create their own repository (`self.repository`), so a view only calls methods such as `add_product()` or `authenticate()`.
* The models protect their own data. `Product.__post_init__` rejects negative prices and quantities. `Employee.__post_init__` rejects an empty name or username.
* Password hashing is hidden inside the employee service. Passwords are salted and hashed with PBKDF2-HMAC-SHA256, and only the hash is stored.
* Helper methods such as `_to_employee()` and `_selected_employee()` are marked with a leading underscore, which means they are only for use inside their own class.

### Inheritance

All the view classes inherit from PyQt6 classes and call `super().__init__()`:

* `loginwindow`, `HoverMenu`, `Dashboard`, `ProductPage`, and `EmployeePage` inherit from `QWidget`
* `mainwindow` inherits from `QMainWindow`
* `AddProductDialog` and `EmployeeDialog` inherit from `QDialog`

This gives each class windows, layouts, buttons, and events without rewriting them. ProTrack has no custom base classes of its own.

### Polymorphism

* **Method overriding:** `HoverMenu` overrides `enterEvent()` and `leaveEvent()`, and `Dashboard` overrides `showEvent()`. Each one adds its own behavior and then calls `super()`, so the normal PyQt6 behavior still runs. The dashboard uses this to refresh its numbers every time the page is shown.
* **Shared method names:** `ProductRepository` and `EmployeeRepository` both provide `add`, `list`, `search`, `update`, and `delete`. The services follow the same pattern, so both features work in the same way even though each uses a different table.
* **Shared dialog behavior:** `AddProductDialog` and `EmployeeDialog` are both opened with `exec()`, which they inherit from `QDialog`.
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
