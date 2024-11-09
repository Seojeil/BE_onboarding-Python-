from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "nickname", "role"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance

    # 출력 데이터를 보여주도록 변환
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["role"] = instance.get_role_display()
        return representation

    # 닉네임 검증
    def validate_nickname(self, value):
        # 길이 검증
        if len(value) < 2 or len(value) > 20:
            raise serializers.ValidationError(
                "닉네임은 최소 2글자 이상, 최대 20글자 이하이어야 합니다."
            )

        return value

    # 비밀번호 검증
    def validate_password(self, value):
        # 길이 검증
        if len(value) < 8:
            raise serializers.ValidationError("비밀번호는 최소 8자 이상이어야 합니다.")

        return value
