from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from users.models import User



class UserTest(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:

        cls.seller_data = {
            "username": "Test",
            "password": "12345",
            "first_name": "Test",
            "last_name": "Seller",
            "is_seller": True
        }

        cls.common_user = {
            "username": "Test2",
            "password": "12345",
            "first_name": "Test2",
            "last_name": "Common User",
            "is_seller": False
        }

        cls.seller = User.objects.create_user(**cls.seller_data)

        cls.common_user = User.objects.create_user(**cls.common_user)

    def test_username_max_length(self):

        max_length = self.seller._meta.get_field("username").max_length

        self.assertEqual(max_length, 50)

    def test_usename_unique(self):

        is_unique = self.seller._meta.get_field("username").unique

        self.assertTrue(is_unique)

    def test_first_name_max_length(self):

        max_length = self.seller._meta.get_field("first_name").max_length

        self.assertEqual(max_length, 50)

    def test_last_name_max_length(self):

        max_length = self.seller._meta.get_field("last_name").max_length

        self.assertEqual(max_length, 50)

    def test_is_seller_blank(self):

        is_blank = self.seller._meta.get_field("is_seller").blank

        self.assertTrue(is_blank)

    def test_is_seller_null(self):

        is_null = self.seller._meta.get_field("is_seller").null

        self.assertTrue(is_null)

    def test_is_seller_default(self):

        is_default_false = self.seller._meta.get_field("is_seller").default

        self.assertFalse(is_default_false)

    def test_creating_seller_account(self):

        seller_true = self.seller.is_seller

        self.assertTrue(seller_true)

    def test_creating_common_account(self):

        seller_false = self.common_user.is_seller

        self.assertFalse(seller_false)

    def test_if_could_create_an_account_with_wrong_key(self):

        with self.assertRaises(TypeError):
            wrong_keys_user = User.objects.create(
                name="Wrong",
                first_name="Wrong",
                last_name="Key",
                is_seller=False
            )


class SellerLoginTest(APITestCase):
    @classmethod
    def setUpTestData(cls):

        cls.seller_data = {
            "username": "Test",
            "password": "12345",
            "first_name": "Test",
            "last_name": "Seller",
            "is_seller": True
        }

        cls.seller = User.objects.create_user(**cls.seller_data)

    def test_if_login_seller_returning_token(self):

        response = self.client.post(
            '/api/login/', {"username": self.seller_data["username"], "password": self.seller_data["password"]}, format='json')

        self.assertTrue(response.data["token"])


class CommomUserLoginTest(APITestCase):

    @classmethod
    def setUpTestData(cls):

        cls.common_user = {
            "username": "Test2",
            "password": "12345",
            "first_name": "Test2",
            "last_name": "Common User",
            "is_seller": False
        }

        cls.user = User.objects.create_user(**cls.common_user)

    def test_if_login_commom_user_returning_token(self):

        login_response = self.client.post(
            '/api/login/', {"username": self.common_user["username"], "password": self.common_user["password"]}, format='json')

        self.assertTrue(login_response.data["token"])


class PermissionsAccountsTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

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

        cls.user = User.objects.create_user(**cls.common_user)
        cls.other = User.objects.create_user(**cls.other_user)

    def test_if_just_owner_account_can_update(self):
        token = Token.objects.create(user=self.other)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

        update = client.patch(
            f'/api/accounts/{self.user.id}', {"username": "Test3"}, format='json')


        self.assertEqual(update.status_code, 403)


    def test_if_just_admin_can_deactivate_accounts(self):

        token = Token.objects.create(user=self.other)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token '+token.key)   

        soft_delete = client.patch(f'/api/accounts/{self.other.id}/management/', {"is_active": False}, format='json')  

        self.assertEqual(soft_delete.status_code, 403)  


    def test_if_just_admin_can_reactivate_accounts(self):

        token = Token.objects.create(user=self.other)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token '+token.key)   

        soft_delete = client.patch(f'/api/accounts/{self.other.id}/management/', {"is_active": True}, format='json')  

        self.assertEqual(soft_delete.status_code, 403)  


    def test_anyone_can_list_accounts(self):

        client = APIClient()

        list_accounts = client.get(f'/api/accounts/')

        self.assertEqual(list_accounts.status_code, 200)






        


