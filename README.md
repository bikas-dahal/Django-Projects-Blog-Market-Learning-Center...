# Django Projects: Blog, Market, and Learning Center

Welcome to the **Django Projects** repository! This project showcases multiple Django applications, including a Blog, Market, Learning Center and others. Each application is built to demonstrate the versatility and power of Django for various use cases.

![Django Banner](https://th.bing.com/th/id/OIP.vofAscaAsfh4QI-2B0bq3gHaEK?rs=1&pid=ImgDetMain)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Contributing](#contributing)
- [Contact](#contact)

## Overview

This repository contains three major Django projects:

1. **Blog**: A platform where users can write, edit, and share their thoughts.
2. **Market**: An e-commerce application with product listings, cart management, and checkout functionality.
3. **Learning Center**: A portal for users to explore and enroll in various courses.

## Features

- **Blog Application**
  - User authentication and profiles
  - Create, edit, and delete posts
  - Categories and tags for posts, like and views also
  - Commenting system

- **Market Application**
  - Product catalog with search and filter options
  - Shopping cart and checkout with Stripe integration
  - Order history and tracking (to be added)
  - User reviews and ratings (to be added)

- **Learning Center**
  - Course listing and detailed descriptions
  - Enroll in courses and track progress
  - Chatrooms
  - Interactive quizzes and assessments (to be added)

## Tech Stack

- **Backend**: Django, Django REST Framework
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL
- **Others**: Docker, Celery, Redis

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.x
- Django
- Docker
- PostgreSQL
- Redis

  `I initially deployed using digital ocean app platform, later with the help of docker-compose with cluster, nginx and other required cloud services, and lastly with k8s but now is not working on it, if anyone want to work further on this and make something out of this, I welcome you. 😊`

### Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/bikas-dahal/Django-Projects-Blog-Market-Learning-Center.git
   cd Django-Projects-Blog-Market-Learning-Center
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables:**

   Create a `.env` file in the root directory and add your environment-specific variables.

5. **Run migrations:**

   ```bash
   python manage.py migrate
   ```

6. **Start the development server:**

   ```bash
   python manage.py runserver
   ```

### Usage

- Visit `http://localhost:8000` to access the applications.
- Use the admin panel (`/admin`) to manage content and users.

## Contributing
I used a lot of help from a Book called Django 5 with examples, 😁

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.


## Contact

**Bikas Dahal**  
[GitHub](https://github.com/bikas-dahal) | [LinkedIn](https://www.linkedin.com/in/bikas-dahal-2229301b3/)

