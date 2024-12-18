from django import forms
from django.contrib.auth.models import User
from django.forms import ImageField, ValidationError
from django.core.validators import validate_email
from app.models import Answer, Profile, Question, Tag
from datetime import datetime


class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(min_length=3, label="Password", widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not(User.objects.filter(username=username).all().count()):
            raise ValidationError("Wrong username!")
        return username
    

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_check']
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).all().count():
            raise ValidationError('Username is already exists!')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        validate_email(email)
        if User.objects.filter(email=email).all().count():
            raise ValidationError('Email is already exists!')
        return email

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()

        password = cleaned_data.get('password')
        password_check = cleaned_data.get('password_check')

        if password and password_check:
            if password != password_check:
                raise ValidationError("The two password fields must match!")
        return cleaned_data
    
    def save(self):
        self.cleaned_data.pop('password_check')
        user = User.objects.create_user(**self.cleaned_data)
        Profile.objects.create(profile=user)
        return user
    
class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_username(self, **kwargs):
        user = super().save(**kwargs)
        new_username = self.cleaned_data.get('username')
        if User.objects.filter(username=new_username).all().count() and new_username != user.username:
            raise ValidationError('Username is already exists!')
        return new_username
    
    def clean_email(self, **kwargs):
        user = super().save(**kwargs)
        new_email = self.cleaned_data.get('email')
        validate_email(new_email)
        if User.objects.filter(email=new_email).all().count() and new_email != user.email:
            raise ValidationError('Email is already exists!')
        return new_email
    
    def save(self, **kwargs):
        user = super().save(**kwargs)

        profile = user.profile
        received_avatar = self.cleaned_data.get('avatar')
        new_username = self.cleaned_data.get('username')
        new_email = self.cleaned_data.get('email')
        if new_username != user.username:
            user.username = new_username
        if new_email != user.email:
            user.email = new_email
        if received_avatar:
            profile.avatar = self.cleaned_data.get('avatar')
            profile.save()

        return user

class AskForm(forms.ModelForm):
    tags = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Example: python, mail.ru, c++'}))

    def __init__(self, user, *args, **kwargs):
        self.user: User = user
        super().__init__(*args, **kwargs)

    class Meta:
        model = Question
        fields = ['title', 'content']

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        tags_list = tags.strip().split(',')
        if len(tags_list) > 3:
            raise ValidationError('No more than 3 tags')
        if len(tags_list) < 1:
            raise ValidationError('Question must have some tags')
        return tags

    def get_tags(self):
        form_tags_str = self.cleaned_data.get('tags')
        from_tags_list = form_tags_str.strip().split(' ')
        db_tags = []
       
        for tag in from_tags_list:
            db_tags.append(
                Tag.objects.get_or_create(
                    name=tag.strip()
                )
            )
        return list(map(lambda x: x[0], db_tags))

    def save(self):
        datetime_now = datetime.now()
        profile = Profile.objects.get(profile=self.user)
        question = Question(profile=profile, title=self.cleaned_data['title'], content=self.cleaned_data['content'], date=datetime_now)
        question.save()

        tags = self.cleaned_data.get('tags')
        tags_list = tags.strip().split(',')

        tags_set = set()
        for i in tags_list:
            tags_set.add(Tag.objects.get_or_create(name=i.strip())[0])

        question.tags.set(list(tags_set))
        return question
    
class AnswerForm(forms.ModelForm):
    
    def __init__(self, user, question_id, *args, **kwargs):
        self.user: User = user
        self.question_id = question_id
        super().__init__(*args, **kwargs)

    class Meta:
        model = Answer
        fields = ['content']

    def save(self):
        datetime_now = datetime.now()
        question = Question.objects.get(id=self.question_id)
        profile = Profile.objects.get(profile=self.user)
        answer = Answer(profile=profile, question=question, content=self.cleaned_data['content'], date=datetime_now)
        answer.save()
        return answer
    
    def content(self):
        return self.cleaned_data['content']
    

