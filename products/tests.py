from django.test import TestCase
from products.models import Product
from users.models import User


class ProductRelationshipTest(TestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:

        cls.product_data = {
                "description": "produto teste",
                "price": 124.32,
                "quantity": 10,
                "is_active": True
            }

        cls.user_data = {
                "username": "Test",
                "password": "12345",
                "first_name": "Test",
                "last_name": "User",
                "is_seller": True
            }

        cls.user2_data = {
                "username": "Test2",
                "password": "12345",
                "first_name": "Test2",
                "last_name": "User2",
                "is_seller": True
        }
        
        cls.products = [Product(**cls.product_data) for _ in range(10)]

        cls.user = User.objects.create(**cls.user_data)

        cls.product_testing = cls.products[0]


    def test_max_digits_price(self):               

        max_digits = self.product_testing._meta.get_field("price").max_digits

        self.assertEqual(max_digits, 10)


    def test_decimal_places(self):

        decimal_places = self.product_testing._meta.get_field("price").decimal_places

        self.assertEqual(decimal_places, 2)


    def test_is_active_null(self):

        is_null = self.product_testing._meta.get_field("is_active").null

        self.assertTrue(is_null)


    def test_is_active_default(self):

        is_default_true = self.product_testing._meta.get_field("is_active").default

        self.assertTrue(is_default_true) 


    def test_is_active_blank(self):

        is_blank = self.product_testing._meta.get_field("is_active").blank

        self.assertTrue(is_blank)

    


    def test_relationship_onde_to_many(self):
        
        for product in self.products:
            product.seller = self.user
            product.save()

        self.assertEquals(
            len(self.products),
            self.user.products_on_sale.count()
        )

        for product in self.products:
            self.assertIs(product.seller, self.user)

        

    def test_product_cannot_belong_to_more_than_one_user(self):

        for product in self.products:
            product.seller = self.user
            product.save()

        
        user2 = User.objects.create(**self.user2_data)

        for product in self.products:
            product.seller = user2
            product.save()

        for product in self.products:
            self.assertIn(product, user2.products_on_sale.all())
            self.assertNotIn(product, self.user.products_on_sale.all())

