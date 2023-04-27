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


## How to set up ?

#### Manual Set up 


1. Clone the project `https://github.com/chapainaashish/shopapi`

2. Install poetry in your system `curl -sSL https://install.python-poetry.org | python3 -`

3. Install the dependencies  `poetry install`
   
4. Enter into the virtual environment `poetry shell`

5. Rename the `.env_example` to `.env` and update the environment variables accordingly

6. Set `DJANGO_SETTINGS_MODULE` according to your need
   - For development: `DJANGO_SETTINGS_MODULE = 'shopapi.settings.development'` 
   - For production : `DJANGO_SETTINGS_MODULE = 'shopapi.settings.production'` 
      - Set database `HOST` `USER` `PASSWORD` `PORT` in `.env` file for production

  

7. Install docker in your system `https://docs.docker.com/desktop/`

8. Run redis using docker `docker run -d  -p 6379:6379 redis` 

9. Start the celery worker `celery -A shopapi worker --loglevel=info`

10. Install stripe cli tool on your system `https://stripe.com/docs/stripe-cli#install`

11. Configure the webhook `stripe listen --forward-to localhost:8000/store/webhooks/stripe/`

12. Create the migration `python manage.py migrate` 

13. Create the superuser `python manage.py createsuperuser`

14. Run the development server `python manage.py runserver`

15. Head over to `http://localhost:8000/admin` on your browser
   
16. Run the test using command `pytest` or `pwt` for continuous testing *[Optional]*

17. Generate test coverage in html using `pytest --cov --cov-report=html` *[Optional]*

18. Run celery flower to manage celery workers `celery flower` *[Optional]*

19. Run the performance test using `locust -f locustfiles/browse_product.py` *[Optional]*
    
20. Read the API documentation on `http://127.0.0.1:8000/api/schema/swagger-ui/` *[Optional]*


#### Docker Set up


21. Clone the project `https://github.com/chapainaashish/shopapi`

22. Rename the `.env_example` to `.env` and update the environment variables accordingly

23. Set `DJANGO_SETTINGS_MODULE` according to your need
   - For development: `DJANGO_SETTINGS_MODULE = 'shopapi.settings.development'` 
   - For production : `DJANGO_SETTINGS_MODULE = 'shopapi.settings.production'` 
       - Set database `HOST` `USER` `PASSWORD` `PORT` in `.env` file for production

  
4. Install docker in your system `https://docs.docker.com/desktop/`


5. Rename `docker-compose-dev.yml` to `docker-compose.yml` for development [Skip for production]
   
6. Build docker image and run
   
```
$ docker-compose up
$ docker-compose exec web python manage.py createsuperuser
```

7. Head over to `http://localhost:8000/admin` on your browser


## Basic APIs Implementation


<table>
  <thead>
   <tr>
      <th rowspan=2>Endpoints</th>
      <th colspan=3 style='text-align:center'>User</th>
    </tr>
    <tr>
      <th>Anonymous</th>
      <th>Authenticated+Authorized</th>
      <th>Admin</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td colspan=4><strong>collection</strong></td>
    </tr>
    <tr>
      <td>store/collection</td>
      <td>GET</td>
      <td>GET</td>
      <td>GET, POST</td>
    </tr>
    <tr>
      <td>store/collection/pk</td>
      <td>GET</td>
      <td>GET</td>
      <td>GET, PUT, PATCH, DELETE</td>
    </tr>
   <tr>
      <td colspan=4><strong>product</strong></td>
    </tr>
    <tr>
      <td>store/product</td>
      <td>GET</td>
      <td>GET</td>
      <td>GET, POST</td>
    </tr>
    <tr>
      <td>store/product/pk</td>
      <td>GET</td>
      <td>GET</td>
      <td>GET, PUT, PATCH, DELETE</td>
    </tr>
    <tr>
      <td>store/product/pk/reviews</td>
      <td>GET</td>
      <td>GET, POST</td>
      <td>GET, POST</td>
    </tr>
    <tr>
      <td>store/product/pk/reviews/pk</td>
      <td>GET</td>
      <td>GET, PATCH, DELETE</td>
      <td>GET, PATCH, DELETE</td>
    </tr>
    <tr>
      <td colspan=4><strong>cart</strong></td>
    </tr>
    <tr>
      <td>store/cart</td>
      <td>-</td>
      <td>GET, POST</td>
      <td>GET, POST</td>
    </tr>
    <tr>
      <td>store/cart/pk</td>
      <td>-</td>
      <td>GET</td>
      <td>GET</td>
    </tr>
    <tr>
      <td>store/cart/pk/items</td>
      <td>-</td>
      <td>GET, POST</td>
      <td>GET, POST</td>
    </tr>
    <tr>
      <td>store/cart/pk/items/pk</td>
      <td>-</td>
      <td>GET, PATCH, DELETE</td>
      <td>GET, PATCH, DELETE</td>
    </tr>
    <tr>
      <td colspan=4><strong>order</strong></td>
    </tr>
    <tr>
      <td>store/order</td>
      <td>-</td>
      <td>GET, POST</td>
      <td>GET, POST</td>
    </tr>
    <tr>
      <td>store/order/pk</td>
      <td>-</td>
      <td>GET</td>
      <td>GET, PATCH, DELETE</td>
    </tr>
    <tr>
      <td>store/order/pk/items</td>
      <td>-</td>
      <td>GET</td>
      <td>GET</td>
    </tr>
    <tr>
      <td>store/order/pk/items/pk</td>
      <td>-</td>
      <td>GET</td>
      <td>GET, DELETE</td>
    </tr>
    <tr>
      <td colspan=4><strong>payment</strong></td>
    </tr>
   <tr>
      <td>store/payment</td>
      <td>-</td>
      <td>GET</td>
      <td>GET</td>
    </tr>
    <tr>
      <td>store/payment/pk</td>
      <td>-</td>
      <td>GET</td>
      <td>GET, PATCH, DELETE</td>
    </tr>
    <tr>
      <td>stripe/payment/pk</td>
      <td>-</td>
      <td>POST</td>
      <td>POST</td>
    </tr>
    <tr>
      <td colspan=4><strong>user</strong></td>
    </tr>
    <tr>
      <td>user/address</td>
      <td>-</td>
      <td>GET, POST</td>
      <td>GET, POST</td>
    </tr>
    <tr>
      <td>user/address/pk</td>
      <td>-</td>
      <td>GET, PUT, PATCH, DELETE</td>
      <td>GET, PUT, PATCH, DELETE</td>
    </tr>
    <tr>
      <td>user/profile</td>
      <td>-</td>
      <td>GET, POST</td>
      <td>GET, POST</td>
    </tr>
    <tr>
      <td>user/profile/pk</td>
      <td>-</td>
      <td>GET, PATCH, DELETE</td>
      <td>GET, PATCH, DELETE</td>
    </tr>

   </tbody>
</table>
   

## References

- https://docs.djangoproject.com/en/4.1/
- https://www.django-rest-framework.org/
- https://python-poetry.org/docs/
- https://docs.celeryq.dev/en/stable/getting-started/introduction.html
- https://pytest-django.readthedocs.io/en/latest/tutorial.html
- https://django-debug-toolbar.readthedocs.io/en/latest/installation.html
- https://djoser.readthedocs.io/en/latest/getting_started.html
- https://stripe.com/docs/stripe-cli
- https://docs.docker.com/engine/install/
- https://drf-spectacular.readthedocs.io/en/latest/
