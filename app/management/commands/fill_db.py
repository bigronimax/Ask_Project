from django.core.management import BaseCommand
from faker import Faker
from datetime import datetime
from app.models import Question, Answer, Like, Tag, Profile, User

fake = Faker()


class Command(BaseCommand):
    help = "Fills database with fake data"

    def add_arguments(self, parser):
        parser.add_argument("num", type=int)

    def handle(self, *args, **kwargs):
        num = kwargs['num']

        tags = [
            Tag(
                name = fake.word()
            ) for i in range(num)
        ]

        Tag.objects.bulk_create(tags)
        tags = Tag.objects.all()
        tags_count = tags.count()

        likes = [
            Like(
                amount = fake.random_int(0, 100000)
            ) for i in range(num*200)
        ]

        Like.objects.bulk_create(likes)
        likes = Like.objects.all()
        likes_count = likes.count()

        profiles = [
            Profile(
                profile = User.objects.create_user(username=f'{fake.unique.name()} + {i}')
            ) for i in range(num)
        ]

        Profile.objects.bulk_create(profiles)
        profiles = Profile.objects.all()
        profiles_count = profiles.count()

        
        questions = []
        
        for i in range(num*10):
            q = Question(
                title = fake.sentence(nb_words=3),
                content = fake.text(),
                like = likes[fake.random_int(min=0, max=likes_count-1)],
                profile = profiles[fake.random_int(min=0, max=profiles_count-1)],
                date = str(fake.date_between(datetime(2022,1,1), datetime(2023,12,31)))
            ) 
            q.save()
            q.tags.add(tags[fake.random_int(min=0, max=tags_count-1)])
            questions.append(q)
     
        questions = Question.objects.all()
        questions_count = questions.count()

        answers = [
            Answer(
                question = questions[fake.random_int(min=0, max=questions_count-1)],
                content = fake.text(),
                like = likes[fake.random_int(min=0, max=likes_count-1)],
                profile = profiles[fake.random_int(min=0, max=profiles_count-1)],
                date = str(fake.date_between(datetime(2022,1,1), datetime(2023,12,31)))
            ) for i in range(num*100)
        ]
        Answer.objects.bulk_create(answers)