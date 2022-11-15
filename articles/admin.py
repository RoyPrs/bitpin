from django.contrib import admin
from articles.models import Article, Ranking


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "get_avg_rank",
    )
    actions = ["do_something"]

    def do_something(self, request, queryset):
        pass

    do_something.short_description = "Do something"


@admin.register(Ranking)
class RankingAdmin(admin.ModelAdmin):
    list_display = ("pk", "ranker", "rank", "article", "public_id")
