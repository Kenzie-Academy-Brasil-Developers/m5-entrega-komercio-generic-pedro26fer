from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from products.models import Product
from users.models import User
from django.db import IntegrityError

from products.serializers import ProductDetailSerializer, ProductGeneralSerializer


class ProductRelationshipAndAttrTest(APITestCase):
    
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



class ProductsPermissionsTest(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:

        cls.seller_data = {
            "username": "Seller",
            "password": "12345",
            "first_name": "Seller",
            "last_name": "Test",
            "is_seller": True
        }

        cls.seller2_data = {
            "username": "Other",
            "password": "12345",
            "first_name": "Seller2",
            "last_name": "test",
            "is_seller": True
        }

        
        cls.common_user = {
            "username": "Test2",
            "password": "12345",
            "first_name": "Test2",
            "last_name": "Common User",
            "is_seller": False
        }
        cls.other_user = {
            "username": "other",
            "password": "12345",
            "first_name": "Other",
            "last_name": "User",
            "is_seller": False
        }

        cls.product_data = {
            "description": "produto teste",
            "price": 124.32,
            "quantity": 10,
            "is_active": True
        }


        cls.product_data_wrong = {
            "descript": "produto teste",
            "price": 124.32,
            "amount": 10,
            "is_active": True
        }

        cls.product_data_negative_quantity= {
            "description": "produto teste",
            "price": 124.32,
            "quantity": -10,
            "is_active": True
        }

        cls.seller = User.objects.create_user(**cls.seller_data)
        cls.seller2 = User.objects.create_user(**cls.seller2_data)
        cls.user = User.objects.create_user(**cls.common_user)
        cls.other = User.objects.create_user(**cls.other_user)
        cls.product = Product.objects.create(**cls.product_data, seller = cls.seller)


    def test_if_only_sellers_can_post_products(self):

        token = Token.objects.create(user=self.other)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

        post_products = client.post('/api/products/', self.product_data, format='json')

        self.assertEqual(post_products.status_code, 403)


    def test_if_only_product_owner_can_update_it(self):

        token = Token.objects.create(user=self.seller2)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

        update_product = client.patch(f'/api/products/{self.product.id}/', {"quantity":5}, format='json')

        self.assertEqual(update_product.status_code, 403)


    def test_anyone_can_retrive_and_list_products(self):

        client = APIClient()

        retrieve_product = client.get(f'/api/products/{self.product.id}/')
        list_products = client.get(f'/api/products/')

        self.assertEqual(retrieve_product.status_code, 200)
        self.assertEqual(list_products.status_code, 200)


    def test_serializer_post_get_products(self):

        token = Token.objects.create(user=self.seller2)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

        post_products = client.post('/api/products/', self.product_data, format='json')
        get_products = client.get('/api/products/')

        response_post = ProductDetailSerializer(data=post_products.data)  
        response_get_products = ProductGeneralSerializer(data=get_products.data["results"][0])   
       

        self.assertTrue(response_post.is_valid())
        self.assertTrue(response_get_products.is_valid())


    def test_post_with_wrong_keys(self):

        with self.assertRaises(TypeError):
            post_product_wrong_keys = Product.objects.create(**self.product_data_wrong, seller= self.seller)

    
    def test_post_with_negative_quantity(self):

        with self.assertRaises(IntegrityError):
            post_product_with_negative_quantity = Product.objects.create(**self.product_data_negative_quantity, seller= self.seller)







        


        




    


    

    