# Shopapi

An E-commerce API built using Django Rest Framework

## Features

- Basic e-commerce features 
- User profile and registration
- JWT based authentication
- Custom permissions set for necessary endpoints
- Payment integration using Stripe
- Customized Admin Panel
- Caching using Redis
- Tested API endpoints using pytest
- Performance test and stress test [on gunicorn]
- Logged essential external service call
- Documentation using DRF spectacular
- Dockerized for local development and production



## Technologies Used

| Technology | Purpose 
| --------- | ----------- |  
Django Rest Framework | APIs Building
Poetry | Dependency Management
PostgresSQL | Database
Celery | Background Task 
Redis | Caching
Pytest | API Testing
Locust | Performance Testing
Djoser | User Registration
Simple-JWT | User Authentication
Stripe | Payment
DRF spectacular | Documentation
Docker | Virtualization


## How to set up 

#### Manually For Development

This process assumes you have python `poetry` installed in your machine. Visit here to learn more about how to install poetry

1. Clone the project `https://github.com/chapainaashish/shopapi`

2. Install the dependencies  `poetry install`
   
3. Enter into the virtual environment `poetry shell`

4. Rename the `.env_example` to `.env` and update the environment variables accordingly

5. Set `DJANGO_SETTINGS_MODULE = 'shopapi.settings.development'` 

6. Run `python manage.py migrate` 
   
7. Run the development server `python manage.py runserver`

8. Create the superuser `python manage.py createsuperuser`

9. Head over to `http://localhost:8000/admin` on your browser

10. Run redis on docker for caching and as a message broker for celery `docker run -d  -p 6379:6379 redis` 

11. Start the celery worker `celery -A shopapi worker --loglevel=info`

12. Run the stripe webhook `stripe listen --forward-to localhost:8000/store/webhooks/stripe/`


**OPTIONAL**
   
13. Run the test using command `pytest` 

14. Generate test coverage in html `pytest --cov --cov-report=html` 

15. Run celery flower to manage celery workers `celery flower`

16. Run the performance test `locust -f locustfiles/browse_product.py`


**Docker**



$ docker-compose up
$ docker-compose exec web python manage.py createsuperuser