from django.contrib.auth import get_user_model
from rest_framework.views import APIView


User = get_user_model()


class RegisterAPIView(APIView):
    def post(self, request):
        pass
