<h1 align="center">ProTrack</h1>
A desktop inventory and employee management app built with PyQt6 and SQLite. ProTrack lets you sign in, manage your product stock, manage the employees who can access the system, and keep an eye on everything through a live dashboard with a recent-activity feed.

<br>

<p align="center">
  <img src="screenshots/login.png" width="300" alt="ProTrack login screen">
  <img src="screenshots/dashboard.png" width="450" alt="ProTrack dashboard">
</p>

<br>
### Features
Secure login – employees sign in with a username and password. Passwords are never stored in plain text; they are hashed with PBKDF2-HMAC-SHA256 (200,000 iterations) and a unique random salt.
Product management – add, update, delete, and search products (name, price, quantity).
Automatic stock status – each product's status is computed from its quantity and color-coded in the table:
Quantity	Status
0	Out of Stock (red)
1–9	Low Stock (yellow)
10+	In Stock (green)
Employee management – add, update, delete, and search employees. Usernames are unique, and leaving the password blank when editing keeps the current one.
Dashboard – at-a-glance totals for products and employees, a breakdown of In Stock / Low Stock / Out of Stock items, and the 10 most recent actions.
Activity log – every add, update, and delete is recorded with a timestamp and shown on the dashboard.
Input validation – negative prices/quantities, empty fields, and duplicate usernames are rejected with clear messages.
Default admin account – created automatically on first run so you can log in right away.
