from django.db import models
from django.contrib.auth.models import User
from django.core.paginator import Paginator
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

class Question(models.Model):
    title = models.CharField(max_length=50, blank=False)
    content = models.TextField(blank=False, max_length=200)
    profile = models.ForeignKey('Profile', on_delete=models.PROTECT, blank=True, null=True, default="")
    rating = models.IntegerField(default=0)
    tags = models.ManyToManyField('Tag', blank=True)
    date = models.DateField(blank=False, null=True)
    

    objects = QuestionManager()

    def __str__(self):
        return f'Question: {self.title}'



class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, blank=False, default="")
    content = models.TextField(blank=False)
    profile = models.ForeignKey('Profile' , on_delete=models.PROTECT, blank=True, null=True, default="")
    rating = models.IntegerField(default=0)
    date = models.DateField(blank=False, null=True)

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
    name = models.CharField(blank=False, max_length=32)

    objects = TagManager()

    def __str__(self):
        return f'Tag: {self.name}'

class QuestionLike(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    like = models.BooleanField()

class AnswerLike(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    like = models.BooleanField()
    

def paginate(request, objects, per_page=3):
    paginator = Paginator(objects, per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    page_items = paginator.page(page_number)
    return {'items': page_items, 'obj': page_obj}
    


    


