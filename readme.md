# SocialMedia-App

## Description

SocialMedia-App is a application designed for social interaction and networking. Built using Django and PostgreSQL. This project is managed with Docker Compose to streamline the development and deployment process.


## Technologies Used

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Containerization**: Docker, Docker Compose

## Installation

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/codewithmanuu/accuknox-assignment.git

2. **Build and start the services using Docker Compose:**

   ```bash
   sudo docker-compose up --build

   ```windows
   docker-compose up --build

3. **Make migrations and migrate**

   ```bash
   - sudo docker-compose exec django python manage.py makemigratios SocialMediaApp
   - sudo docker-compose exec django python manage.py migrate

   ```windows
   - docker-compose exec django python manage.py makemigratios SocialMediaApp
   - docker-compose exec django python manage.py migrate

3. **Create a superuser for accessing the Django admin panel:**

   ```bash
   sudo docker-compose exec django python manage.py createsuperuser

   ```windows
   docker-compose exec django python manage.py createsuperuser


## Usage

- Import the provided collections into any API client of your choice. 
- Access the application at http://localhost:8000/api/v1/
- Access the Django admin panel at http://localhost:8000/admin/

## Development
 
 **Make sure to use the provided .env file for local development.**

1. **Use the following command to stop and remove containers:**

   ```bash
   sudo docker-compose down

   ```windows
   docker-compose down

2. **Use the following command to rebuild images and start services:**

   ```bash
   sudo docker-compose up --build

   ```windows
   docker-compose up --build

## Contact

- For questions or comments, please reach out <mailto:manukrishna.s2001@gmail.com>
