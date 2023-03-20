import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings


class Specialization(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class User(AbstractUser):
    CLIENT = 'client'
    MANAGER = 'manager'
    ADMIN = 'admin'
    TRAINER = 'trainer'
    ROLE_CHOICES = (
        (CLIENT, 'Client'),
        (MANAGER, 'Manager'),
        (ADMIN, 'Admin'),
        (TRAINER, 'Trainer')
    )
    # # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    specialization = models.OneToOneField(Specialization, on_delete=models.CASCADE, null=True)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, blank=True, null=True)
    trainer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='clients', null=True)
    # user.trainer - get user's trainer if user is client
    # user.clients - if user is trainer, get his clients. user may have not trainer


#  models for gym
class Gym(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    users = models.ManyToManyField(User, related_name='user_gyms')


class RoomType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Room(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)


class Lesson(models.Model):
    TYPE_CHOICES = (
        ('general', 'General'),
        ('personal', 'Personal'),
        ('group', 'Group')
    )

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    max_capacity = models.IntegerField(default=1, null=True, blank=True)
    start_time = models.DateTimeField()
    duration = models.DurationField(default=timezone.timedelta(minutes=30))
    end_time = models.DateTimeField(null=True)
    trainer = models.ForeignKey(User, on_delete=models.CASCADE)


class Inventory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField()
    weight = models.FloatField(null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='inventory_items')


#  models for subscription
class Plan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField()
    visits_count = models.PositiveIntegerField()


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    visits_left = models.PositiveIntegerField()


    def days_left(self):
        duration = timezone.timedelta(days=self.plan.duration_days)
        end_date = self.start_date + duration
        days_left = (end_date - timezone.now().date()).days
        return max(0, days_left)

    def set_plan(self, plan):
        self.plan = plan
        self.start_date = timezone.now()
        self.visits_left = plan.visits_count
        self.save()


#  model for financial records
class FinancialRecord(models.Model):
    INCOME = 1
    EXPENSE = 2
    FIN_CHOICES = (
        (INCOME, 'income'),
        (EXPENSE, 'expense'),
    )
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.CharField(max_length=255)
    type = models.PositiveSmallIntegerField(choices=FIN_CHOICES, blank=True, null=True)

#  Models for training
class TrainingProgram(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='programs')


class ExerciseSet(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    program = models.ManyToManyField(TrainingProgram, related_name='exercise_sets')


class Exercise(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    exercise_set = models.ManyToManyField(ExerciseSet, related_name='exercises')


class TrainingSession(models.Model):
    program = models.ForeignKey(TrainingProgram, on_delete=models.CASCADE, related_name='sessions')
    exercise_set = models.ManyToManyField(ExerciseSet)
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions_as_trainer')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions_as_client')
    date = models.DateTimeField()
    mark = models.PositiveIntegerField(null=True)


#  Models for chat
class Chat(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='chats', null=True)
    creator = models.ForeignKey(User, related_name="owned_chats", on_delete=models.CASCADE)


class Message(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message {self.pk} by {self.author}'

    @property
    def likes(self):
        return self.reactions.filter(type=Reaction.LIKE).count()

    @property
    def dislikes(self):
        return self.reactions.filter(type=Reaction.DISLIKE).count()


class Reaction(models.Model):
    LIKE = 'like'
    DISLIKE = 'dislike'
    TYPES = (
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    )

    type = models.CharField(max_length=10, choices=TYPES)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reactions')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='reactions')
    created_at = models.DateTimeField(auto_now_add=True)


#  models for mailing
class MailingList(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mailing_lists')
    name = models.CharField(max_length=255)
    description = models.TextField()
    subscribers = models.ManyToManyField(User, related_name='subscriptions', null=True)


class Newsletter(models.Model):
    mailing_list = models.ForeignKey(MailingList, on_delete=models.CASCADE, related_name='newsletters')
    subject = models.CharField(max_length=255)
    content = models.TextField()
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_emails')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_emails')
    created_at = models.DateTimeField(auto_now_add=True)