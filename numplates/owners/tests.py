from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.serializers import ValidationError
from rest_framework.test import APIClient

from .models import Owner
from .serializers import OwnerSerializer


class OwnerListRetrieveTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.owner = Owner.objects.create(
            first_name='Foo',
            last_name='Bar'
        )

    def tearDown(self):
        Owner.objects.all().delete()

    def test_list_owners(self):
        """Owners can be listed"""

        response = self.client.get(reverse('owner-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

        results = response.data.get('results')

        self.assertEqual(len(results), 1)

        owner_data = results[0]

        self.assertEqual(owner_data.get('first_name'), 'Foo')
        self.assertEqual(owner_data.get('last_name'), 'Bar')

    def test_retrieve_owner(self):
        """Owner can be retrieved"""

        response = self.client.get(
            reverse('owner-list') + str(self.owner.id) + '/',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        owner_data = response.data

        self.assertEqual(owner_data.get('first_name'), 'Foo')
        self.assertEqual(owner_data.get('last_name'), 'Bar')


class OwnerCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        Owner.objects.all().delete()

    def test_create_owner(self):
        """Owner can be created"""

        response = self.client.post(
            reverse('owner-list'),
            {
                'first_name': 'Foo',
                'last_name': 'Bar',
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        owner_data = response.data

        self.assertEqual(owner_data.get('first_name'), 'Foo')
        self.assertEqual(owner_data.get('last_name'), 'Bar')


class OwnerUpdateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.owner = Owner.objects.create(
            first_name='Foo',
            last_name='Bar'
        )

    def tearDown(self):
        Owner.objects.all().delete()

    def test_update_owner(self):
        """Owner can be updated"""

        response = self.client.put(
            reverse('owner-list') + str(self.owner.id) + '/',
            {
                'first_name': 'Foo',
                'last_name': 'Bar',
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        owner_data = response.data

        self.assertEqual(owner_data.get('first_name'), 'Foo')
        self.assertEqual(owner_data.get('last_name'), 'Bar')

    def test_partial_update_owner(self):
        """Owner can be partially updated"""

        response = self.client.put(
            reverse('owner-list') + str(self.owner.id) + '/',
            {
                'first_name': 'Foo',
                'last_name': 'Bar',
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        owner_data = response.data

        self.assertEqual(owner_data.get('first_name'), 'Foo')
        self.assertEqual(owner_data.get('last_name'), 'Bar')


class OwnerDeleteTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.owner = Owner.objects.create(
            first_name='Foo',
            last_name='Bar'
        )

    def test_delete_owner(self):
        """Owner can be deleted"""

        response = self.client.delete(
            reverse('owner-list') + str(self.owner.id) + '/',
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Owner.objects.count(), 0)


class OwnerSerializerValidationsTestCase(TestCase):
    def test_first_name_must_start_with_capital(self):
        """Validation error is raised if first name does not start with capital
        letter"""

        self.assertRaises(
            ValidationError,
            OwnerSerializer.validate_last_name,
            OwnerSerializer(),
            'jhon',
        )

    def test_last_name_must_start_with_capital(self):
        """Validation error is raised if last name does not start with capital
        letter"""

        self.assertRaises(
            ValidationError,
            OwnerSerializer.validate_last_name,
            OwnerSerializer(),
            'snow',
        )
