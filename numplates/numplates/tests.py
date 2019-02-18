from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.serializers import ValidationError
from rest_framework.test import APIClient, APIRequestFactory

from numplates.owners.models import Owner
from numplates.cars.models import Car

from .models import NumPlate
from .views import NumPlateViewSet
from .serializers import NumPlateSerializer


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

        response = self.client.get(reverse('numplate-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

        results = response.data.get('results')

        self.assertEqual(len(results), 1)

        plate_data = results[0]

        self.assertEqual(plate_data.get('number'), 'AAA000')

    def test_retrieve_num_plate(self):
        """Num plate can be retrieved"""

        response = self.client.get(
            reverse('numplate-list') + str(self.num_plate.id) + '/',
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
            reverse('numplate-list'),
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
            reverse('numplate-list') + str(self.num_plate.id) + '/',
            {'number': 'AAA000'},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        plate_data = response.data

        self.assertEqual(plate_data.get('number'), 'AAA000')

    def test_partial_update_num_plate(self):
        """Num plate can be partially updated"""

        response = self.client.patch(
            reverse('numplate-list') + str(self.num_plate.id) + '/',
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
            reverse('numplate-list') + str(self.num_plate.id) + '/',
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(NumPlate.objects.count(), 0)


class NumPlateCarsTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.num_plate = NumPlate.objects.create(
            number='AAA000',
        )

        self.car = Car.objects.create(
            model='Mercedes Benz',
        )

    def tearDown(self):
        NumPlate.objects.all().delete()
        Owner.objects.all().delete()

    def test_set_num_plate_car(self):
        """Can set number plate car"""
        request = self.factory.patch(
            reverse('numplate-list') + str(self.num_plate.id) + '/',
            {'car': str(self.car.id)},
        )

        view = NumPlateViewSet.as_view(actions={'patch': 'partial_update'})

        response = view(request, pk=self.num_plate.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('car'), self.car.id)

    def test_num_plate_car_is_not_required(self):
        """Number plate car is not required"""
        request = self.factory.put(
            reverse('numplate-list'),
            {'number': 'AAA000'},
        )

        view = NumPlateViewSet.as_view(actions={'put': 'update'})

        response = view(request, pk=self.num_plate.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('car'), None)


class NumPlateOwnersTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.num_plate = NumPlate.objects.create(
            number='AAA000',
        )

        self.owner = Owner.objects.create(
            first_name='Foo',
            last_name='Bar',
        )

    def tearDown(self):
        NumPlate.objects.all().delete()
        Owner.objects.all().delete()

    def test_set_num_plate_owner(self):
        """Can set number plate owner"""
        request = self.factory.patch(
            reverse('numplate-list') + str(self.num_plate.id) + '/',
            {'owner': str(self.owner.id)},
        )

        view = NumPlateViewSet.as_view(actions={'patch': 'partial_update'})

        response = view(request, pk=self.num_plate.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('owner'), self.owner.id)

    def test_num_plate_owner_is_not_required(self):
        """Number plate owner is not required"""
        request = self.factory.put(
            reverse('numplate-list'),
            {'number': 'AAA000'},
        )

        view = NumPlateViewSet.as_view(actions={'put': 'update'})

        response = view(request, pk=self.num_plate.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('owner'), None)


class NumPlateSerializerValidationsTestCase(TestCase):
    def test_allows_regular_lithuanian_number_format(self):
        """Regular lithuanian car numbers are allowed"""
        validated = NumPlateSerializer().validate_number('AAA000')

        self.assertEqual(validated, 'AAA000')

    def test_raise_validation_error_on_invalid_number_format(self):
        """Validation error should be raised if invalid number format is
        provided"""

        self.assertRaises(
            ValidationError,
            NumPlateSerializer.validate_number,
            NumPlateSerializer(),
            '000AAA',
        )
