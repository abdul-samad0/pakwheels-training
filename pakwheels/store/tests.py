from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from pakwheels.accounts.models import User
from pakwheels.store.models import Category, Product


class StoreAPITests(APITestCase):
    def setUp(self):
        self.user = User(
            email="seller@example.com",
            first_name="Seller",
            last_name="User",
        )
        self.user.set_password("StrongPass123!")
        self.user.save()

        self.category = Category.objects.create(name="Cars", slug="cars")

    def test_create_category_api(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("api-category-create")
        payload = {"name": "SUV"}

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Category.objects.filter(name="SUV").exists())
        self.assertTrue(response.data["slug"])

    def test_create_product_api_sets_seller_and_slug(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("api-product-create")
        payload = {
            "title": "Honda Civic 2020",
            "description": "Clean car, single owner.",
            "price": "4500000.00",
            "location": "Lahore",
            "condition": "used",
            "category": self.category.id,
            "status": "active",
            "year": 2020,
            "mileage": 45000,
            "engine_capacity_cc": 1800,
            "registered_city": "Lahore",
            "body_type": "Sedan",
            "color": "White",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product = Product.objects.get(title="Honda Civic 2020")
        self.assertEqual(product.seller_id, self.user.id)
        self.assertTrue(product.slug)

    def test_product_list_search_filter_and_sort(self):
        Product.objects.create(
            title="Toyota Corolla",
            slug="toyota-corolla",
            description="Reliable family car",
            price=3000000,
            location="Karachi",
            condition="used",
            status="active",
            year=2018,
            mileage=70000,
            category=self.category,
            seller=self.user,
            color="Silver",
        )
        Product.objects.create(
            title="Honda City",
            slug="honda-city",
            description="Neat and clean",
            price=2500000,
            location="Lahore",
            condition="used",
            status="active",
            year=2019,
            mileage=50000,
            category=self.category,
            seller=self.user,
            color="White",
        )

        url = reverse("api-product-list")
        response = self.client.get(
            url,
            {
                "q": "Honda",
                "max_price": 3000000,
                "sort": "price_asc",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["title"], "Honda City")
