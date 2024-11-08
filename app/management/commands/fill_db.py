from django.core.management import BaseCommand
from random import randint
from faker import Faker
from datetime import datetime
from app.models import Question, Answer, QuestionLike, AnswerLike, Tag, Profile, User

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
                rating = randint(0, 100000),
                profile = profiles.get(pk=randint(1, profiles_count)),
                date = str(fake.date_time_between(datetime(2022,1,1, 0, 0, 0, 0), datetime(2023,12,31, 0, 0, 0, 0)))
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
                rating = randint(0, 100000),
                profile = profiles.get(pk=randint(1, profiles_count)),
                date = str(fake.date_time_between(datetime(2022,1,1, 0, 0, 0, 0), datetime(2023,12,31, 0, 0, 0, 0)))
            ) for i in range(answers_size)
        ]
        Answer.objects.bulk_create(answers)
        answers = Answer.objects
        answers_count = answers.count()

        questionLikes = []
        cnt = 0
        profiles_cnt = 0
        while (cnt != likes_size // 2):
            profiles_cnt += 1
            profile = profiles.get(pk=profiles_cnt)
            for i in range(1, questions_count+1):
                question = questions.get(pk=i)
                questionLikes.append(QuestionLike(
                    profile = profile,
                    question = question,
                    like = randint(0, 1)
                )) 
                cnt += 1
                if (cnt == likes_size // 2):
                    break     

        QuestionLike.objects.bulk_create(questionLikes)

        answerLikes = []
        cnt = 0
        profiles_cnt = 0
        while (cnt != likes_size // 2):
            profiles_cnt += 1
            profile = profiles.get(pk=profiles_cnt)
            for i in range(1, answers_count+1):
                answer = answers.get(pk=i)
                answerLikes.append(AnswerLike(
                    profile = profile,
                    answer = answer,
                    like = randint(0, 1)
                ))  
                cnt += 1
                if (cnt == likes_size // 2):
                    break     
                
        AnswerLike.objects.bulk_create(answerLikes)
        