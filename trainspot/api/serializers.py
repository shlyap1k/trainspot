# from django.contrib.auth.models import User, Group
from api.models import *
from rest_framework import serializers
from django.core.exceptions import ValidationError
import datetime


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'


class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        fields = ['id', 'title', 'description', 'user', 'is_live']


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'


class TrainerForeignKey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return User.objects.filter(role='trainer')


class ClientsForeignKey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return User.objects.filter(role='client')


class UserSerializer(serializers.ModelSerializer):
    trainer = TrainerForeignKey()
    # clients = serializers.ChoiceField(User.objects.filter(role=1))
    # field_name = serializers.ChoiceField(*args, **kwargs)
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'specialization', 'role', 'trainer', 'clients', 'date_joined']
        # depth = 1


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    # room_type = RoomTypeSerializer()

    class Meta:
        model = Room
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    trainer = TrainerForeignKey()
    class Meta:
        model = Lesson
        fields = '__all__'

    def validate(self, data):
        start_time = data['start_time']
        end_time = start_time + data['duration']
        data['end_time'] = end_time

        # Check if start time is during work hours
        work_start = timezone.make_aware(datetime.datetime.combine(start_time.date(), datetime.time(9, 0)))
        work_end = timezone.make_aware(datetime.datetime.combine(start_time.date(), datetime.time(22, 0)))
        if start_time < work_start or start_time > work_end:
            raise ValidationError('Начало занятия должно быть в рабочее время (9:00 - 22:00)')

        # Check if start time is at an even hour
        if start_time.minute != 0:
            raise ValidationError('Занятие должно начинаться в 0 минут.')

        # Check if trainer is available
        trainer = data['trainer']
        if trainer.lesson_set.filter(start_time__lt=start_time, end_time__gt=end_time).exists():
            raise ValidationError('Тренер не доступен в это время')
        if trainer.lesson_set.filter(start_time__lt=end_time, end_time__gt=start_time).exists():
            raise ValidationError('Тренер не доступен в это время')

        # Check if end time is before end of work day
        if end_time > work_end:
            raise ValidationError('Занятие должно заканчиваться до окончания рабочего дня (22:00)')

        return data


class GymSerializer(serializers.ModelSerializer):
    # rooms = RoomSerializer(many=True)
    class Meta:
        model = Gym
        # depth = 1
        fields = '__all__'


class InventorySerializer(serializers.ModelSerializer):
    # room = RoomSerializer()

    class Meta:
        model = Inventory
        fields = '__all__'


class PlanTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanType
        fields = '__all__'


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'description', 'price', 'duration_days', 'visits_count', 'plan_type']

    def to_representation(self, instance):
        representation = super(PlanSerializer, self).to_representation(instance)
        representation['plan_type'] = PlanTypeSerializer(instance.plan_type).data
        return representation


class SubscriptionSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    # plan = PlanSerializer()

    days_left = serializers.SerializerMethodField('get_days_left')

    def get_days_left(self, obj):
        return obj.days_left()

    class Meta:
        model = Subscription
        fields = ['id', 'start_date', 'days_left', 'visits_left', 'user', 'plan']

    def validate(self, data):
        if self.context['request'].user.role == 'client':
            data['user'] = self.context['request'].user
        data['visits_left'] = data['plan'].visits_count
        return data


class FinancialRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialRecord
        fields = '__all__'
        ordering = ['date']

    def to_representation(self, instance):
        representation = super(FinancialRecordSerializer, self).to_representation(instance)
        representation['plan'] = PlanSerializer(instance.plan).data
        return representation


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'


class ExerciseSetSerializer(serializers.ModelSerializer):
    # exercises = ExerciseSerializer(many=True)

    class Meta:
        model = ExerciseSet
        fields = '__all__'


class TrainingProgramSerializer(serializers.ModelSerializer):
    # exercise_sets = ExerciseSetSerializer(many=True)

    class Meta:
        model = TrainingProgram
        fields = '__all__'


class TrainingSessionSerializer(serializers.ModelSerializer):
    # program = TrainingProgramSerializer()
    # exercise_set = ExerciseSetSerializer(many=True)
    # trainer = UserSerializer()
    # client = UserSerializer()

    class Meta:
        model = TrainingSession
        fields = '__all__'


class ReactionSerializer(serializers.ModelSerializer):
    # author = UserSerializer()
    # message = MessageSerializer()

    class Meta:
        model = Reaction
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(ReactionSerializer, self).to_representation(instance)
        representation['author'] = UserSerializer(instance.author).data
        return representation


class MessageSerializer(serializers.ModelSerializer):
    # author = UserSerializer()
    reactions = ReactionSerializer(many=True, read_only=True)
    # chat = ChatSerializer()
    replies = 'self'

    class Meta:
        model = Message
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(MessageSerializer, self).to_representation(instance)
        representation['author'] = UserSerializer(instance.author).data
        # representation['members'] = []
        # for m in instance.members:
        #     representation['members'].append()
        return representation


class ChatSerializer(serializers.ModelSerializer):
    # members = UserSerializer(many=True)
    # creator = UserSerializer()
    # messages = MessageSerializer(many=True)
    class Meta:
        model = Chat
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(ChatSerializer, self).to_representation(instance)
        representation['creator'] = UserSerializer(instance.creator).data
        representation['messages'] = []
        representation['members'] = []
        for m in instance.members.all():
            representation['members'].append(UserSerializer(m).data)
        for m in instance.messages.all():
            representation['messages'].append(MessageSerializer(m).data)
        return representation


class MailingListSerializer(serializers.ModelSerializer):
    subscribers = serializers.SerializerMethodField()

    class Meta:
        model = MailingList
        fields = '__all__'

    def get_subscribers(self, obj):
        return UserSerializer(obj.subscribers.all(), many=True).data


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = '__all__'


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = '__all__'

# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']
