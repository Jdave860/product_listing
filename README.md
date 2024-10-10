# Minimalist Product Listing Website

A minimalist web application built with Python 3, Django, and PostgreSQL for managing product listings.

## Features

- **Product Listing**: Displays products available from different suppliers.
- **Product Management Actions**: Administrators can manage products (add, edit, delete).
- **User Authentication**: Authorization for users through username and password.
- **Roles**:
  - **Buyer**: Can view the product listing.
  - **Supplier**: Can view the list of their products and cheaper analogues from other suppliers.
  - **Administrator**: Has access to the administrator interface for user and product management.
- **Product Information**:
  - Supplier
  - Name
  - Product/Symbol Code (unique per supplier)
  - Price
  - Stock Status (In stock or Out of stock)
  - Images (optional, with one marked as the main/default)

## Sections

- **Main Section**: Landing page with login for unauthorized users.
- **Administrator Section**: 
  - User management (list, add, edit, delete users).
  - Product management (list, add, edit, delete products).
- **Supplier Section**: 
  - List of the supplier's products showing Name, Product Code, Price, Stock Status, and Image availability.
  - List of supplier products that have cheaper analogues in stock among other suppliers.
- **Buyer Section**: 
  - General list of products in stock from all suppliers showing Name, Product Code, Price, Supplier, and Main product image.

## Technologies Used

- Python 3
- Django
- PostgreSQL
