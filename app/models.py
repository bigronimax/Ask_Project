from django.db import models
from django.contrib.auth.models import User
from django.core.paginator import Paginator

# Create your models here.

class QuestionManager(models.Manager):

    def get_tag(self, tag):
        return self.filter(tags__name=tag)
    
    def get_hot(self):
        return self.filter(like__amount__gte=90000).order_by('-like__amount')
    
    def get_new(self):
        return self.order_by('-date')

class AnswerManager(models.Manager):
    
    def get_answers(self, question):
        return self.filter(question=question).order_by('-date')

class Question(models.Model):
    title = models.CharField(max_length=255, blank=False)
    content = models.TextField(blank=False)
    profile = models.ForeignKey('Profile', on_delete=models.PROTECT, blank=True, null=True, default="")
    like = models.ForeignKey('Like' , on_delete=models.PROTECT)
    tags = models.ManyToManyField('Tag', blank=True)
    date = models.DateField(blank=False, null=True)

    objects = QuestionManager()

    def __str__(self):
        return f'Question: {self.title}'


class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, blank=False, default="")
    content = models.TextField(blank=False)
    profile = models.ForeignKey('Profile' , on_delete=models.PROTECT, blank=True, null=True, default="")
    like = models.ForeignKey('Like' , on_delete=models.PROTECT)
    date = models.DateField(blank=False, null=True)

    objects = AnswerManager()

    def __str__(self):
        return f'Answer: {self.profile}'


class Profile(models.Model):
    profile = models.OneToOneField(User, null=True, on_delete=models.PROTECT, default="")
    avatar = models.ImageField(blank=True)

    def __str__(self):
        return f'Profile: {self.profile}'
    

class Tag(models.Model):
    name = models.CharField(blank=False, max_length=32)

    def __str__(self):
        return f'Tag: {self.name}'

class Like(models.Model):
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.amount}'
    


def paginate(request, objects, per_page=3):
    paginator = Paginator(objects, per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    page_items = paginator.page(page_number)
    return {'items': page_items, 'obj': page_obj}
    


    


