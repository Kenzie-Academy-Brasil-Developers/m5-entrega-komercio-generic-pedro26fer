from django.test import TestCase

from users.models import User

class UserTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_data = {
            "username": "Test",
            "password": "12345",
            "first_name": "Test",
            "last_name": "User",
            "is_seller": True
        }

        cls.user = User.objects.create(**cls.user_data)

    def test_username_max_length(self):

        max_length = self.user._meta.get_field("username").max_length

        self.assertEqual(max_length, 50)


    def test_usename_unique(self):
        
        is_unique = self.user._meta.get_field("username").unique

        self.assertTrue(is_unique)


    def test_password_max_length(self):

        max_length = self.user._meta.get_field("password").max_length

        self.assertEqual(max_length, 20)


    def test_first_name_max_length(self):

        max_length = self.user._meta.get_field("first_name").max_length

        self.assertEqual(max_length, 50)


    def test_last_name_max_length(self):

        max_length = self.user._meta.get_field("last_name").max_length

        self.assertEqual(max_length, 50)


    def test_is_seller_blank(self):
        
        is_blank = self.user._meta.get_field("is_seller").blank

        self.assertTrue(is_blank)


    def test_is_seller_null(self):
    
        is_null = self.user._meta.get_field("is_seller").null

        self.assertTrue(is_null)


    def test_is_seller_default(self):
    
        is_default_false = self.user._meta.get_field("is_seller").default

        self.assertFalse(is_default_false)