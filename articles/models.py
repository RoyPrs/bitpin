from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models import Avg
from django.contrib.auth import get_user_model


from common.model_mixins import ValidateOnSaveMixin
from common import generate_public_key

UserModel = get_user_model()


class Article(ValidateOnSaveMixin, models.Model):
    public_id = models.CharField(
        verbose_name=_("Public Article ID"),
        max_length=30,
        unique=True,
        blank=True,
        editable=False,
        help_text=_("Public ID to identify an individual article"),
    )
    title = models.CharField(
        verbose_name=_("Article Title"),
        max_length=50,
        help_text=_("The title of the article"),
    )
    body = models.TextField(
        verbose_name=_("Article Body"),
        max_length=1000,
        blank=True,
        help_text=_("The body of the article"),
    )
    rankers = models.ManyToManyField(
        UserModel,
        verbose_name=_("Ranker"),
        help_text=_("The user who has ranked this article"),
        blank=True,
    )

    class Meta:
        ordering = ("title",)
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")

    def clean(self):
        # Populate the public_id on record creation only.
        if self.pk is None and not self.public_id:
            self.public_id = generate_public_key()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_avg_rank(self):
        """This method retrieves the average ranks given to the article"""
        from django.apps import apps

        Ranking = apps.get_model("articles", "Ranking")
        avg = Ranking.objects.get(article=self).aggregate(Avg("rank"))
        return avg["rank__avg"]

    def count_rankers(self, prerequesits):
        """This method returns the count of users ranked the article"""
        from django.apps import apps

        Ranking = apps.get_model("article", "Ranking")
        count = Ranking.objects.get(article=self).count()
        return count

    def rank(self, ranker, rank):
        """Through this method, a user can rank the article"""
        msg = _("Rank must be an integer in the [1,5] interval.")
        if type(rank) != int or rank > 5 or rank < 1:
            raise ValidationError({"rank": msg})

        from django.apps import apps

        Ranking = apps.get_model("articles", "Ranking")
        try:
            ranking = Ranking.objects.get(ranker=ranker, article=self)
            ranking.update(rank=rank)
        except Ranking.DoesNotExist:
            Ranking.objects.create(ranker=ranker, article=self, rank=rank)


class Ranking(models.Model):
    public_id = (
        models.CharField(
            verbose_name=_("Public Ranking ID"),
            max_length=30,
            unique=True,
            blank=True,
            editable=False,
            help_text=_("Public ID to identify an individual ranking"),
        ),
    )

    ranker = (models.ForeignKey(UserModel, on_delete=models.CASCADE),)
    article = (models.ForeignKey(Article, on_delete=models.CASCADE),)
    rank = models.PositiveSmallIntegerField(
        verbose_name=_("Article Rank"),
        help_text=_("Ranking of the article by user"),
    )
