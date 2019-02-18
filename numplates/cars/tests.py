from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory

from .models import Car
from .serializers import CarSerializer
from .views import CarViewSet


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

        response = self.client.get(reverse('car-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

        results = response.data.get('results')

        self.assertEqual(len(results), 1)

        car_data = results[0]

        self.assertEqual(car_data.get('model'), 'Mercedes Benz')

    def test_retrieve_car(self):
        """Car can be retrieved"""

        response = self.client.get(
            reverse('car-list') + str(self.car.id) + '/',
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
            reverse('car-list'),
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
            reverse('car-list') + str(self.car.id) + '/',
            {'model': 'Mercedes Benz'},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        car_data = response.data

        self.assertEqual(car_data.get('model'), 'Mercedes Benz')

    def test_partial_update_car(self):
        """Car can be partially updated"""

        response = self.client.patch(
            reverse('car-list') + str(self.car.id) + '/',
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
            reverse('car-list') + str(self.car.id) + '/',
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Car.objects.count(), 0)


class CarImageLoadTestCase(TestCase):
    def tearDown(self):
        Car.objects.all().delete()

    @patch('numplates.cars.tasks.load_image.apply_async')
    def test_create_car_with_image(self, _):
        """Car with image can be created"""
        factory = APIRequestFactory()

        request = factory.post(
            reverse('car-list'),
            {
                'model': 'Mercedes Benz',
                'image': 'https://myimages.com/image.png',
            },
        )

        view = CarViewSet.as_view(actions={'post': 'create'})

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Image name is uuid with type
        self.assertRegex(
            response.data.get('image'),
            r'^[0-9a-fA-F\-]{36}\.png$',
        )

    @patch('numplates.cars.tasks.load_image.apply_async')
    def test_on_image_load_random_name_is_generated(self, _):
        """Image name must be random and unique"""
        image_url = 'https://myimages.com/image.png'
        image_name = CarSerializer._load_image(image_url)

        # Image name is uuid4 format
        self.assertRegex(
            image_name,
            r'^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12}.png$'
        )
