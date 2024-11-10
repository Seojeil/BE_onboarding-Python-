from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse


class UserAuthenticationTests(APITestCase):
    def setUp(self):
        """
        테스트에 필요한 기본 사용자 데이터를 설정합니다.
        """
        self.user_data = {
            "username": "testuser",
            "password": "password123",
            "email": "testuser@example.com",
        }
        self.user = get_user_model().objects.create_user(
            username=self.user_data["username"],
            password=self.user_data["password"],
            email=self.user_data["email"],
        )
        self.signup_url = reverse("signup")  # 회원가입 URL
        self.login_url = reverse("login")  # 로그인 URL

    def test_signup_success(self):
        """
        회원가입 테스트: 정상적인 데이터를 입력하면 회원가입이 성공해야 한다.
        """
        data = {
            "username": "newuser",
            "password": "password123",
            "email": "newuser@example.com",
        }
        response = self.client.post(self.signup_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)

    def test_signup_duplicate_email(self):
        """
        이메일 중복 시 회원가입이 실패해야 한다.
        """
        data = {
            "username": "newuser",
            "password": "password123",
            "email": self.user_data["email"],  # 기존에 존재하는 이메일
        }
        response = self.client.post(self.signup_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_signup_invalid_data(self):
        """
        잘못된 데이터로 회원가입 시 실패해야 한다.
        """
        data = {
            "username": "",  # 비어있는 사용자명
            "password": "password123",
            "email": "invalidemail",
        }
        response = self.client.post(self.signup_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)

    def test_login_success(self):
        """
        올바른 자격 증명으로 로그인 시 토큰이 발급되어야 한다.
        """
        data = {
            "username": self.user_data["username"],
            "password": self.user_data["password"],
        }
        response = self.client.post(self.login_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)  # access token 존재 확인
        self.assertIn("refresh", response.data)  # refresh token 존재 확인

    def test_login_invalid_credentials(self):
        """
        잘못된 자격 증명으로 로그인 시 401 상태 코드와 오류 메시지가 반환되어야 한다.
        """
        data = {
            "username": self.user_data["username"],
            "password": "wrongpassword",  # 잘못된 비밀번호
        }
        response = self.client.post(self.login_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "사용자 정보가 일치하지 않습니다.")

    def test_login_empty_fields(self):
        """
        로그인 시 이메일이나 비밀번호가 비어있으면 실패해야 한다.
        """
        data = {
            "username": "",
            "password": "",
        }
        response = self.client.post(self.login_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
        self.assertIn("password", response.data)
