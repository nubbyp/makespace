
import json
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase

from customers.models import Plan
from customers.management.commands.populate_plans import populate_from_csv


class CustomerTests(APITestCase):
    urls = 'customers.urls'    

    setup_done = False

    def setUp(self):
        if CustomerTests.setup_done:
            return
        CustomerTests.setup_done = True

        populate_from_csv('plan_input.csv')

    def test_get_next_billing_date(self):
 
        url = reverse('get_next_billing')
        response = self.client.get(url + '?user_id=user_lp', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_data = json.loads(response.content)
        self.assertEqual(json_data['current_plan'], '2x4')
        self.assertEqual(json_data['next_billing_date'], '11/01/2020')
        self.assertEqual(json_data['is_active'], 'Yes')

    def test_user_id_not_found(self):
 
        url = reverse('get_next_billing')
        response = self.client.get(url + '?user_id=user_xx', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_data = json.loads(response.content)
        self.assertEqual(json_data['error'], 'user_id has no storage plan records')

    def test_user_id_not_provided(self):
 
        url = reverse('get_next_billing')
        response = self.client.get(url , format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_data = json.loads(response.content)
        self.assertEqual(json_data['error'], 'user_id not provided')
