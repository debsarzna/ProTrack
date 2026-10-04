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


## Status

ProTrack is stable for everyday use as a small inventory and staff tracker. Here are some points you may have questions about:

* Database: SQLite, stored in a single local file. No server setup needed.
* Passwords: hashed before storage, never saved or logged in plain text.
* Stock status rules: Out of Stock at `0`, Low Stock at 10 below, In Stock above that.
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
