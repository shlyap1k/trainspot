# from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.serializers import *
from api.models import *
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


class ReadOnlyOrAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all() #  .order_by('-date_joined')
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]
    def get_permissions(self):
        if self.action == 'list':
            return [ReadOnlyOrAuthenticated()]
        else:
            return [IsAuthenticated()]


class TrainersListViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.filter(role='trainer')
    serializer_class = UserSerializer
    # permission_classes = [permissions.AllowAny]
    def get_permissions(self):
        if self.action == 'list':
            return [ReadOnlyOrAuthenticated()]
        else:
            return [IsAuthenticated()]


class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    permission_classes = [permissions.IsAuthenticated]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # permission_classes = [permissions.IsAuthenticated]
    def get_permissions(self):
        if self.action == 'list':
            return [ReadOnlyOrAuthenticated()]
        else:
            return [IsAuthenticated()]


class GymViewSet(viewsets.ModelViewSet):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer
    # permission_classes = [permissions.AllowAny]
    def get_permissions(self):
        if self.action == 'list':
            return [ReadOnlyOrAuthenticated()]
        else:
            return [IsAuthenticated()]


class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    # permission_classes = [permissions.IsAuthenticated]
    def get_permissions(self):
        if self.action == 'list':
            return [ReadOnlyOrAuthenticated()]
        else:
            return [IsAuthenticated()]


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    # permission_classes = [permissions.IsAuthenticated]
    def get_permissions(self):
        if self.action == 'list':
            return [ReadOnlyOrAuthenticated()]
        else:
            return [IsAuthenticated()]


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    # permission_classes = [permissions.IsAuthenticated]
    def get_permissions(self):
        if self.action == 'list':
            return [ReadOnlyOrAuthenticated()]
        else:
            return [IsAuthenticated()]


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    # permission_classes = [permissions.IsAuthenticated]
    def get_permissions(self):
        if self.action == 'list':
            return [ReadOnlyOrAuthenticated()]
        else:
            return [IsAuthenticated()]


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'user__id'


class FinancialRecordViewSet(viewsets.ModelViewSet):
    queryset = FinancialRecord.objects.all()
    serializer_class = FinancialRecordSerializer
    permission_classes = [permissions.IsAuthenticated]


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]


class ExerciseSetViewSet(viewsets.ModelViewSet):
    queryset = ExerciseSet.objects.all()
    serializer_class = ExerciseSetSerializer
    permission_classes = [permissions.IsAuthenticated]


class TrainingProgramViewSet(viewsets.ModelViewSet):
    queryset = TrainingProgram.objects.all()
    serializer_class = TrainingProgramSerializer
    permission_classes = [permissions.IsAuthenticated]


class TrainingSessionViewSet(viewsets.ModelViewSet):
    queryset = TrainingSession.objects.all()
    serializer_class = TrainingSessionSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance.name)
        serializer = ChatSerializer(instance=instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = (Chat.objects.filter(creator=user) | Chat.objects.filter(members__in=[user])).distinct()
        serializer = ChatSerializer(queryset, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]


class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer
    permission_classes = [permissions.IsAuthenticated]


class MailingListViewSet(viewsets.ModelViewSet):
    queryset = MailingList.objects.all()
    serializer_class = MailingListSerializer
    permission_classes = [permissions.IsAuthenticated]


class NewsletterViewSet(viewsets.ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = [permissions.IsAuthenticated]


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]
