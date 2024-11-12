from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from datetime import date, timedelta

# Create your models here.

class QuestionManager(models.Manager):

    def get_tag(self, tag):
        return self.filter(tags__name=tag)
    
    def get_hot(self):
        return self.filter(rating__gte=90000).order_by('-rating')
    
    def get_new(self):
        return self.order_by('-date')

class AnswerManager(models.Manager):
    
    def get_answers(self, question):
        return self.filter(question=question).order_by('-date')
    
class TagManager(models.Manager):

    def get_popular_tags(self):
        return self.annotate(num_question = Count('question')).order_by('-num_question')[:10]
    
class ProfileManager(models.Manager):

    def get_popular_profiles(self):
        return list(self.all())[0:10]
        # startdate = date.today()
        # enddate = startdate + timedelta(days=6)
        # return self.filter(date__range=[startdate, enddate]).order_by('-rating')[:10]

class QuestionLikeManager(models.Manager):
    def toggle_like(self, profile, question):
        if not(self.filter(profile=profile, question=question).exists()) or self.filter(profile=profile, question=question, like=0).exists() or self.filter(profile=profile, question=question, like=None).exists():
            if not(self.filter(profile=profile, question=question).exists()):
                ql = QuestionLike(profile=profile, question=question)
                ql.save()
            elif self.filter(profile=profile, question=question, like=0).exists():
                question.rating += 1
                question.save()
            QuestionLike.objects.filter(profile=profile, question=question).update(like=1)
            question.rating += 1
            question.save()
        elif self.filter(profile=profile, question=question, like=1).exists():
            QuestionLike.objects.filter(profile=profile, question=question).update(like=None)
            question.rating -= 1
            question.save()

    def toggle_dislike(self, profile, question):
        if not(self.filter(profile=profile, question=question).exists()) or self.filter(profile=profile, question=question, like=1).exists() or self.filter(profile=profile, question=question, like=None).exists():
            if not(self.filter(profile=profile, question=question).exists()):
                ql = QuestionLike(profile=profile, question=question)
                ql.save()
            elif self.filter(profile=profile, question=question, like=1).exists():
                question.rating -= 1
                question.save()
            QuestionLike.objects.filter(profile=profile, question=question).update(like=0)
            question.rating -= 1
            question.save()
            
        elif self.filter(profile=profile, question=question, like=0).exists():
            QuestionLike.objects.filter(profile=profile, question=question).update(like=None)
            question.rating += 1
            question.save()

class AnswerLikeManager(models.Manager):
    def toggle_like(self, profile, answer):
        if not(self.filter(profile=profile, answer=answer).exists()) or self.filter(profile=profile, answer=answer, like=0).exists() or self.filter(profile=profile, answer=answer, like=None).exists():
            if not(self.filter(profile=profile, answer=answer).exists()):
                al = AnswerLike(profile=profile,answer=answer)
                al.save()
            elif self.filter(profile=profile, answer=answer, like=0).exists():
                answer.rating += 1
                answer.save()
            AnswerLike.objects.filter(profile=profile, answer=answer).update(like=1)
            answer.rating += 1
            answer.save()
            
        elif self.filter(profile=profile, answer=answer, like=1).exists():
            AnswerLike.objects.filter(profile=profile, answer=answer).update(like=None)
            answer.rating -= 1
            answer.save()

    def toggle_dislike(self, profile, answer):
        if not(self.filter(profile=profile, answer=answer).exists()) or self.filter(profile=profile, answer=answer, like=1).exists() or self.filter(profile=profile, answer=answer, like=None).exists():
            if not(self.filter(profile=profile, answer=answer).exists()):
                al = AnswerLike(profile=profile, answer=answer)
                al.save()
            elif self.filter(profile=profile, answer=answer, like=1).exists():
                answer.rating -= 1
                answer.save()
            AnswerLike.objects.filter(profile=profile, answer=answer).update(like=0)
            answer.rating -= 1
            answer.save()
            
        elif self.filter(profile=profile, answer=answer, like=0).exists():
            AnswerLike.objects.filter(profile=profile, answer=answer).update(like=None)
            answer.rating += 1
            answer.save()

class Question(models.Model):
    title = models.CharField(max_length=50, blank=False)
    content = models.TextField(blank=False, max_length=200)
    profile = models.ForeignKey('Profile', on_delete=models.PROTECT, blank=True, null=True, default="")
    rating = models.IntegerField(default=0)
    tags = models.ManyToManyField('Tag', blank=True)
    date = models.DateTimeField(blank=False, null=True)
    

    objects = QuestionManager()

    def __str__(self):
        return f'Question: {self.title}'



class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, blank=False, default="")
    content = models.TextField(blank=False)
    profile = models.ForeignKey('Profile' , on_delete=models.PROTECT, blank=True, null=True, default="")
    rating = models.IntegerField(default=0)
    date = models.DateTimeField(blank=False, null=True)

    objects = AnswerManager()

    def __str__(self):
        return f'Answer: {self.profile}'


class Profile(models.Model):
    profile = models.OneToOneField(User, null=True, on_delete=models.PROTECT, default="")
    avatar = models.ImageField(null=True, blank=True, default="avatar.png", upload_to="avatar/%Y/%M/%D")

    def __str__(self):
        return f'Profile: {self.profile}'
    
    objects = ProfileManager()
    

class Tag(models.Model):
    name = models.CharField(blank=False, max_length=32, unique=True)

    objects = TagManager()

    def __str__(self):
        return f'Tag: {self.name}'

class QuestionLike(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    like = models.BooleanField(null=True, blank=True)

    objects = QuestionLikeManager()

    class Meta:
        unique_together = ('profile', 'question')

class AnswerLike(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    like = models.BooleanField(null=True, blank=True)

    objects = AnswerLikeManager()

    class Meta:
        unique_together = ('profile', 'answer')
    


    


    


