from django.test import Client, TestCase
from django.urls import reverse

from .models import block


class blockTests(TestCase):

    def setUp(self):
        self.block = block.objects.create(
            title='Harry Potter',
            author='JK Rowling',
            price='25.00',
        )

    def test_block_listing(self):
        self.assertEqual(f'{self.block.title}', 'Harry Potter')
        self.assertEqual(f'{self.block.author}', 'JK Rowling')
        self.assertEqual(f'{self.block.price}', '25.00')

    def test_block_list_view(self):
        response = self.client.get(reverse('block_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Harry Potter')
        self.assertTemplateUsed(response, 'blocks/block_list.html')

    def test_block_detail_view(self):
        response = self.client.get(self.block.get_absolute_url())
        no_response = self.client.get('/blocks/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Harry Potter')
        self.assertTemplateUsed(response, 'blocks/block_detail.html')