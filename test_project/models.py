from django.db import models
import bcrypt, jwt, time, urllib.parse, datetime
from . import utils
from django.core import validators
# Create your models here.



class User(models.Model):
    ROLES = (
        ('m', 'Moderator'),
        ('a', 'Admin'),
    )
    first_name = models.CharField(max_length=20, blank=False, null=False)
    last_name = models.CharField(max_length=20, blank=False, null=False)
    email = models.CharField(max_length=50, blank=False, null=False, unique=True, validators=[validators.validate_email])
    phone_number = models.CharField(max_length=15, blank=False, null=False, unique=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=1, blank=False, null=False, default='m', choices=ROLES)
    approved = models.BooleanField(default=False)
    avatar = models.ImageField(blank=False, null=False, default='https://www.shareicon.net/data/128x128/2016/06/25/786525_people_512x512.png', upload_to='./static', validators=[validators.validate_image_file_extension])


    __original_email = None
    __original_password = None


    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.__original_email = self.email
        self.__original_password = self.password

    def get_avatar_url(self):
        if self.avatar == 'https://www.shareicon.net/data/128x128/2016/06/25/786525_people_512x512.png':
            return 'https://www.shareicon.net/data/128x128/2016/06/25/786525_people_512x512.png'
        else:
            return "/{}".format(self.avatar)

    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        self.full_clean()

        payload = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }

        if self.password is None or self.password == '':
            plainPassword = utils.password_generator()
            self.password = bcrypt.hashpw(plainPassword.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        elif self.password == self.__original_password:
            pass
        else:
            self.password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


        if self.email != self.__original_email:

            utils.send_confirm_email(payload, self.email)
            self.email_verified = False


        super(User, self).save(*args, **kwargs)


    def clean(self, *args, **kwargs):
        super(User, self).clean(*args, **kwargs)


    def __str__(self):
        return self.email


    class Meta:
        db_table = 'users'


class Group(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    users = models.ManyToManyField(User)
    description = models.TextField(blank=True, null=True)
    posts = models.ManyToManyField('test_project.Post', related_name='+', blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'groups'

class Post(models.Model):
    text = models.TextField(blank=False, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='+')
    created_at = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    pinned = models.BooleanField(default=False)
    file = models.FileField(blank=True, null=True, upload_to='./static')
    replays = models.ManyToManyField('test_project.Replay', related_name='+', blank=False, null=False)

    def __str__(self):
        return self.text

    def get_date(self):
        time = datetime.datetime.now()
        if self.created_at.day == time.day:
            return str(time.hour - self.created_at.hour) + " hours ago"
        else:
            if self.created_at.month == time.month:
                return str(time.day - self.created_at.day) + " days ago"
            else:
                if self.created_at.year == time.year:
                    return str(time.month - self.created_at.month) + " months ago"
        return self.created_at

    class Meta:
        db_table = 'posts'
        ordering = ['pinned', '-created_at']


class Roles(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_date(self):
        time = datetime.datetime.now()
        if self.created_at.day == time.day:
            return str(time.hour - self.created_at.hour) + " hours ago"
        else:
            if self.created_at.month == time.month:
                return str(time.day - self.created_at.day) + " days ago"
            else:
                if self.created_at.year == time.year:
                    return str(time.month - self.created_at.month) + " months ago"
        return self.created_at

    class Meta:
        db_table = 'roles'
        ordering = ['-created_at']





class ChatRoom(models.Model):
    subject = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    text = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class PostFiles(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='+')
    file = models.FileField(blank=False, null=False, upload_to='./static')

    def __str__(self):
        return self.post

class Replay(models.Model):
    subject = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='+', null=False, blank=False)
    text = models.TextField(blank=False, null=False)
    file = models.FileField(blank=True, null=True, upload_to='./static')
    created_at = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class QuickLinks(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', null=True, blank=True)