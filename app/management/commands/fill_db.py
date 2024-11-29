from django.core.management import BaseCommand
from random import randint
from faker import Faker
from random import shuffle
from faker.providers.person.en import Provider
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

        first_names = list(set(Provider.first_names))
        shuffle(first_names)
        tag_names = first_names[0:tags_size]

        tags = [
            Tag(
                name = f'{tag_names[i]}_{i}'
            ) for i in range(tags_size)
        ]

        Tag.objects.bulk_create(tags)
        tags = list(Tag.objects.all())
        tags_count = len(tags)
        profiles = [
            Profile(
                profile = User.objects.create_user(username=f'{fake.name()}_{i}')
            ) for i in range(profiles_size)
        ]

        Profile.objects.bulk_create(profiles)
        profiles = list(Profile.objects.all())
        profiles_count = len(profiles)
        
        for i in range(questions_size):
            q = Question(
                title = fake.sentence(nb_words=3),
                content = fake.text(),
                rating = randint(0, 100000),
                profile = profiles[randint(0, profiles_count-1)],
                date = str(fake.date_time_between(datetime(2022,1,1, 0, 0, 0, 0), datetime(2023,12,31, 0, 0, 0, 0)))
            ) 
            q.save()
            q.tags.add(tags[randint(0, tags_count-1)])
     
        questions = list(Question.objects.all())
        questions_count = len(questions)

        answers = [
            Answer(
                question = questions[randint(0, questions_count-1)],
                content = fake.text(),
                rating = randint(0, 100000),
                profile = profiles[randint(0, profiles_count-1)],
                date = str(fake.date_time_between(datetime(2022,1,1, 0, 0, 0, 0), datetime(2023,12,31, 0, 0, 0, 0))),
                correct = False,
            ) for i in range(answers_size)
        ]
        Answer.objects.bulk_create(answers)
        answers = list(Answer.objects.all())
        answers_count = len(answers)

        questionLikes = []
        cnt = 0
        profiles_cnt = 0
        while (QuestionLike.objects.filter(profile=profiles[profiles_cnt]).exists()):
            profiles_cnt += 1
        
        while (cnt != likes_size):
            profile = profiles[profiles_cnt]
            profiles_cnt += 1
            for i in range(questions_count):
                question = questions[i]
                questionLikes.append(QuestionLike(
                    profile = profile,
                    question = question,
                    like = randint(0, 1)
                )) 
                cnt += 1
                if (cnt == likes_size):
                    break     

        QuestionLike.objects.bulk_create(questionLikes)

        answerLikes = []
        cnt = 0
        profiles_cnt = 0
        while (AnswerLike.objects.filter(profile=profiles[profiles_cnt]).exists()):
            profiles_cnt += 1

        while (cnt != likes_size):
            profile = profiles[profiles_cnt]
            profiles_cnt += 1
            for i in range(answers_count):
                answer = answers[i]
                answerLikes.append(AnswerLike(
                    profile = profile,
                    answer = answer,
                    like = randint(0, 1)
                ))  
                cnt += 1
                if (cnt == likes_size):
                    break     
                
        AnswerLike.objects.bulk_create(answerLikes)
        