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
- Performance test and stress test [On local server]
- Logged essential external Service call
- Documentation using DRF spectacular
- Dockerized for local development and production



## Technologies Used

| Technology | Purpose 
| --------- | ----------- |  
Django Rest Framework | APIs Building
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

**Manual**


1. clone the project

2. create virtual env

3. set up the setting

3. migrate

4. start celery and redis

5. run the server 

**Docker**


## Development

1. to run pytest [terminal]
`pytest`

2. to generate test coverage [terminal]
`pytest --cov --cov-report=html`

3. to run celery [terminal]
`celery -A shopapi worker --loglevel=info`

4. to run redis [docker]
`docker run -d  -p 6379:6379 redis`

5. to run celery flower [http://locahost:5500]
`celery flower`

6. to run locust [http://localhost:8089/]
`locust -f directory/file.py`

7. to run stripe webhook
`stripe listen --forward-to localhost:8000/store/webhooks/stripe/`


$ docker-compose up
$ docker-compose exec web python manage.py createsuperuser