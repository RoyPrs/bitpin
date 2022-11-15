import datetime

from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


from rest_framework import serializers

from common.serializer_mixin import SerializerMixin
from articles import models

UserModel = get_user_model()


def get_user(request):
    user = None
    if hasattr(request, "user"):
        user = request.user
    return user


# ------------------------------Project------------------------------


class ArticleSerializer(SerializerMixin, serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()

    def get_avg_rank(self, obj):
        return obj.get_avg_rank()

    def get_rankers(self, obj):
        return obj.count_rankers()

    class Meta:
        model = models.Article
        fields = ["public_id", "title", "avg_rank", "rankers"]
        read_only_fields = "public_id"

    def validate_ranker(self, manager):
        msg = _(
            f"Manager must be MANAGER :-D you should either sigin as a manager or specify a manager"
        )
        if manager.role != "MANAGER":
            raise serializers.ValidationError(msg)
        return manager


# ------------------------------Ranking------------------------------
class RankingSerializer(SerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Ranking
        fields = [
            "public_id",
            "ranker",
            "rank",
            "article",
        ]
        read_only_fields = ("public_id",)

    # def create(self, validated_data):
    #     return obj

    # def update(self, instance, validated_data):
    #     return instance

    # def to_representation(self, instance):
    # def validate(self, data):
