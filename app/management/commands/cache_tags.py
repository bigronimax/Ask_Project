from django.core.management.base import BaseCommand
from django.utils.timezone import now
from django.core.cache import cache
from django.db.models import Count
from datetime import timedelta
from app.models import Tag


class Command(BaseCommand):
    help = 'Update tags cache'

    def handle(self, *args, **kwargs):
        cache_key = "popular_tags"
        three_months_ago = now() - timedelta(days=90)
        popular_tags = (
            Tag.objects.filter(questions__date__gte=three_months_ago)
            .annotate(num_question=Count('questions'))
            .order_by('-num_question')[:10]
        )
        cache.set(cache_key, list(popular_tags), 60 * 60 * 24)  

