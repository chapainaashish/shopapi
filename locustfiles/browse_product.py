from random import randint

from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task(3)
    def view_product(self):
        category_id = randint(1, 2)
        self.client.get(
            f"/store/product/?category_id={category_id}", name="/store/product"
        )

    @task(4)
    def view_product_instance(self):
        product_id = randint(1, 10)
        self.client.get(f"/store/product/{product_id}", name="/store/product/:id")

    @task(2)
    def view_product_reviews(self):
        product_id = randint(1, 10)
        self.client.get(
            f"/store/product/{product_id}/reviews", name="/store/product/:id/reviews"
        )
