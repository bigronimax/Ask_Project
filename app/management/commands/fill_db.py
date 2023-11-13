from django.core.management import BaseCommand
from random import randint
from faker import Faker
from datetime import datetime
from app.models import Question, Answer, Like, Tag, Profile, User

fake = Faker()


class Command(BaseCommand):
    help = "Fills database with fake data"

    def add_arguments(self, parser):
        parser.add_argument("ratio", type=int)

    def handle(self, *args, **kwargs):
        num = kwargs['ratio']

        tags_size = num
        likes_size = num*200
        questions_size = num*10
        profiles_size = num
        answers_size = num*100

        tags = [
            Tag(
                name = fake.word()
            ) for i in range(tags_size)
        ]

        Tag.objects.bulk_create(tags)
        tags = Tag.objects
        tags_count = tags.count()

        likes = [
            Like(
                amount = fake.random_int(0, 100000)
            ) for i in range(likes_size)
        ]

        Like.objects.bulk_create(likes)
        likes = Like.objects
        likes_count = likes.count()

        profiles = [
            Profile(
                profile = User.objects.create_user(username=f'{fake.name()}_{i}')
            ) for i in range(profiles_size)
        ]

        Profile.objects.bulk_create(profiles)
        profiles = Profile.objects
        profiles_count = profiles.count()

        
        questions = []
        
        for i in range(questions_size):
            q = Question(
                title = fake.sentence(nb_words=3),
                content = fake.text(),
                like = likes.get(pk=randint(1, likes_count)),
                profile = profiles.get(pk=randint(1, profiles_count)),
                date = str(fake.date_between(datetime(2022,1,1), datetime(2023,12,31)))
            ) 
            q.save()
            q.tags.add(tags.get(pk=randint(1, tags_count)))
            questions.append(q)
     
        questions = Question.objects
        questions_count = questions.count()

        answers = [
            Answer(
                question = questions.get(pk=randint(1, questions_count)),
                content = fake.text(),
                like = likes.get(pk=randint(1, likes_count)),
                profile = profiles.get(pk=randint(1, profiles_count)),
                date = str(fake.date_between(datetime(2022,1,1), datetime(2023,12,31)))
            ) for i in range(answers_size)
        ]
        Answer.objects.bulk_create(answers)