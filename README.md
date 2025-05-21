# 🛒 Amazon Product Review System

A Flask web app for managing and visualizing Amazon product data using SQLite and Plotly.

## 🔧 Features

- **User Authentication**  
  - Admin & Normal user roles  
  - Secure signup with password validation

- **Product Management (Admin Only)**  
  - Add, edit, delete, and search products

- **Interactive Visualizations**  
  - Top 5 most expensive, cheapest, highest price difference, most rated, and best-rated products

## 🛠 Tech Stack

- **Backend**: Flask, SQLite3  
- **Frontend**: HTML (Jinja2 templates)  
- **Data & Charts**: Pandas, Plotly

## 🚀 Getting Started

```bash
git clone https://github.com/AAZINSHAIKH/product_review_system.git
cd product_review_system
pip install flask pandas plotly
python app.py
```

Then open your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## 📁 Files

- `app.py` – Main application  
- `amazon_project.db` – SQLite database  
- `products.csv` – Dataset for visualizations  
- `templates/` – HTML files

## 👤 Admin Login

```
Username: admin  
Password: Password@123
```