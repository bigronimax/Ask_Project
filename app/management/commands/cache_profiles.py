from django.core.management.base import BaseCommand
from django.utils.timezone import now
from datetime import timedelta
from django.core.cache import cache
from django.db.models import Sum
from app.models import Profile, Question, Answer


class Command(BaseCommand):
    help = 'Update profile cache'

    def handle(self, *args, **kwargs):
        cache_key = "best_profiles"
        one_week_ago = now() - timedelta(days=7)
        
        question_ratings = (
            Question.objects.filter(date__gte=one_week_ago)
            .values('profile')
            .annotate(rating=Sum('rating'))
        )
        answer_ratings = (
            Answer.objects.filter(date__gte=one_week_ago)
            .values('profile')
            .annotate(rating=Sum('rating'))
        )

        print(question_ratings)
        print(answer_ratings)
        
        total_scores = {}
        for entry in question_ratings:
            total_scores[entry['profile']] = total_scores.get(entry['profile'], 0) + entry['rating']
        for entry in answer_ratings:
            total_scores[entry['profile']] = total_scores.get(entry['profile'], 0) + entry['rating']
       
        best_profiles = sorted(total_scores.items(), key=lambda x: x[1], reverse=True)[:10]
        best_profiles_data = [{'id': profile_id, 'rating': rating} for profile_id, rating in best_profiles]
       
        cache.set(cache_key, best_profiles_data, 60 * 60 * 24)  
        