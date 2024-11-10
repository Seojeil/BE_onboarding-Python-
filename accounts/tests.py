from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class UserAuthenticationTests(APITestCase):
    def setUp(self):
        """
        테스트에 필요한 기본 사용자 데이터를 설정합니다.
        """
        self.user_data = {
            "username": "testuser",
            "password": "password123",
            "nickname": "testnickname",
        }
        self.user = get_user_model().objects.create_user(
            username=self.user_data["username"],
            password=self.user_data["password"],
            nickname=self.user_data["nickname"],
        )
        self.signup_url = reverse("signup")
        self.login_url = reverse("login")

    def test_signup_success(self):
        """
        회원가입 테스트: 정상적인 데이터를 입력하면 회원가입이 성공해야 하고, role은 기본값 'U'여야 한다.
        """
        data = {
            "username": "newuser",
            "password": "password123",
            "nickname": "newnickname",
        }
        response = self.client.post(self.signup_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("username", response.data)
        self.assertIn("nickname", response.data)
        self.assertEqual(response.data["role"], "USER")

    def test_signup_invalid_nickname_length(self):
        """
        닉네임이 20글자를 초과할 경우 회원가입 시 실패해야 한다.
        """
        data = {
            "username": "validuser",
            "password": "password123",
            "nickname": "a" * 21,
        }
        response = self.client.post(self.signup_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("nickname", response.data)
        self.assertIn("이 필드의 글자 수가 20 이하인지 확인하십시오.", response.data["nickname"])

    def test_signup_invalid_password_length(self):
        """
        비밀번호가 8글자 미만일 경우 회원가입 시 실패해야 한다.
        """
        data = {
            "username": "validuser",
            "password": "short",
            "nickname": "validnickname",
        }
        response = self.client.post(self.signup_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
        self.assertIn("비밀번호는 최소 8자 이상이어야 합니다.", response.data["password"])

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
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_credentials(self):
        """
        잘못된 자격 증명으로 로그인 시 401 상태 코드와 오류 메시지가 반환되어야 한다.
        """
        data = {
            "username": self.user_data["username"],
            "password": "wrongpassword",
        }
        response = self.client.post(self.login_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "사용자 정보가 일치하지 않습니다.")

    def test_login_empty_fields(self):
        """
        로그인 시 사용자명이나 비밀번호가 비어있으면 실패해야 한다.
        """
        data = {
            "username": "",
            "password": "",
        }
        response = self.client.post(self.login_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
