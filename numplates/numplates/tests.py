from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import NumPlate


class NumPlateListRetrieveTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.num_plate = NumPlate.objects.create(
            number='AAA000',
        )

    def tearDown(self):
        NumPlate.objects.all().delete()

    def test_list_num_plates(self):
        """Num plates can be listed"""

        response = self.client.get('/api/v1/numplates/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

        results = response.data.get('results')

        self.assertEqual(len(results), 1)

        plate_data = results[0]

        self.assertEqual(plate_data.get('number'), 'AAA000')

    def test_retrieve_num_plate(self):
        """Num plate can be retrieved"""

        response = self.client.get(
            '/api/v1/numplates/' + str(self.num_plate.id) + '/',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        plate_data = response.data

        self.assertEqual(plate_data.get('number'), 'AAA000')


class NumPlateCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        NumPlate.objects.all().delete()

    def test_create_num_plate(self):
        """Num plate can be created"""

        response = self.client.post(
            '/api/v1/numplates/',
            {'number': 'AAA000'},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        plate_data = response.data

        self.assertEqual(plate_data.get('number'), 'AAA000')


class NumPlateUpdateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.num_plate = NumPlate.objects.create(
            number='AAA000',
        )

    def tearDown(self):
        NumPlate.objects.all().delete()

    def test_update_num_plate(self):
        """Num plate can be updated"""

        response = self.client.put(
            '/api/v1/numplates/' + str(self.num_plate.id) + '/',
            {'number': 'AAA000'},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        plate_data = response.data

        self.assertEqual(plate_data.get('number'), 'AAA000')

    def test_partial_update_num_plate(self):
        """Num plate can be partially updated"""

        response = self.client.patch(
            '/api/v1/numplates/' + str(self.num_plate.id) + '/',
            {'number': 'AAA000'},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        plate_data = response.data

        self.assertEqual(plate_data.get('number'), 'AAA000')


class NumPlateDeleteTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.num_plate = NumPlate.objects.create(
            number='AAA000',
        )

    def test_delete_num_plate(self):
        """Num plate can be deleted"""

        response = self.client.delete(
            '/api/v1/numplates/' + str(self.num_plate.id) + '/',
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(NumPlate.objects.count(), 0)
