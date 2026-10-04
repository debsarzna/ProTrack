<h1 align="center">ProTrack</h1>

## About

ProTrack lets you sign in, manage your product stock, manage the employees who can access the system, and keep an eye on everything through a live dashboard with a recent-activity feed.

Each part of the app (products, employees) lives in its own feature folder and is split into model, repository, service, and view layers. The interface and the database are kept apart, which keeps the code easy to read, test, and extend.

A default admin account is created automatically on first run, so you can log in right away.

<br>

<p align="center">
  <img src="screenshots/login.png" width="300" alt="ProTrack login screen">
  <img src="screenshots/dashboard.png" width="300" alt="ProTrack dashboard">
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
