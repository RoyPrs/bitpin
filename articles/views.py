from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from common.view_mixins import (
    TrapDjangoValidationErrorCreateMixin,
    TrapDjangoValidationErrorUpdateMixin,
)

from articles import serializers, models


UserModel = get_user_model()


def get_user(request):
    user = None
    if hasattr(request, "user"):
        user = request.user
    return user


# ------------------------------Article------------------------------


class ArticleList(TrapDjangoValidationErrorCreateMixin, generics.ListAPIView):
    """This class provides the method to list articles."""

    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ArticleSerializer
    lookup_field = "public_id"

    def get_queryset(self):
        queryset = models.Article.objects.all()
        return queryset


article = ArticleList.as_view()

# ------------------------------Ranking------------------------------


class RankingCreate(
    TrapDjangoValidationErrorCreateMixin, generics.CreateAPIView
):
    """This class provides a method to create a new task."""

    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.RankingSerializer
    lookup_field = "public_id"

    def create(self, request, *args, **kwargs):
        msg = _("Deloper/manager can only define tasks in their own project.")
        ranker = get_user(request)
        data = request.data
        article = data.get("article", None)
        if not article:
            msg = _("Article must be specified")
            raise ValidationError(msg)
        rank = data.get("rank", None)

        article.rank(ranker, rank)


rank = RankingCreate.as_view()
