from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Car


class CarListRetrieveTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.car = Car.objects.create(
            model='Mercedes Benz',
        )

    def tearDown(self):
        Car.objects.all().delete()

    def test_list_cars(self):
        """Cars can be listed"""

        response = self.client.get('/api/v1/cars/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

        results = response.data.get('results')

        self.assertEqual(len(results), 1)

        car_data = results[0]

        self.assertEqual(car_data.get('model'), 'Mercedes Benz')

    def test_retrieve_car(self):
        """Car can be retrieved"""

        response = self.client.get(
            '/api/v1/cars/' + str(self.car.id) + '/',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        car_data = response.data

        self.assertEqual(car_data.get('model'), 'Mercedes Benz')


class CarCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        Car.objects.all().delete()

    def test_create_car(self):
        """Car can be created"""

        response = self.client.post(
            '/api/v1/cars/',
            {'model': 'Mercedes Benz'},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        car_data = response.data

        self.assertEqual(car_data.get('model'), 'Mercedes Benz')


class CarUpdateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.car = Car.objects.create(
            model='Mercedes Benz',
        )

    def tearDown(self):
        Car.objects.all().delete()

    def test_update_car(self):
        """Car can be updated"""

        response = self.client.put(
            '/api/v1/cars/' + str(self.car.id) + '/',
            {'model': 'Mercedes Benz'},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        car_data = response.data

        self.assertEqual(car_data.get('model'), 'Mercedes Benz')

    def test_partial_update_car(self):
        """Car can be partially updated"""

        response = self.client.patch(
            '/api/v1/cars/' + str(self.car.id) + '/',
            {'model': 'Mercedes Benz'},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        car_data = response.data

        self.assertEqual(car_data.get('model'), 'Mercedes Benz')


class CarDeleteTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.car = Car.objects.create(
            model='Mercedes Benz',
        )

    def test_delete_car(self):
        """Car can be deleted"""

        response = self.client.delete(
            '/api/v1/cars/' + str(self.car.id) + '/',
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Car.objects.count(), 0)
