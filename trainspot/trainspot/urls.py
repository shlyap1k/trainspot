"""trainspot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework import routers
from api import views


router = routers.DefaultRouter()

router.register(r'users', views.UserViewSet)
router.register(r'trainers', views.TrainersListViewSet)
router.register(r'lessons', views.LessonViewSet)
router.register(r'specializations', views.SpecializationViewSet)
router.register(r'gyms', views.GymViewSet)
router.register(r'roomtypes', views.RoomTypeViewSet)
router.register(r'rooms', views.RoomViewSet)
router.register(r'inventories', views.InventoryViewSet)
router.register(r'plans', views.PlanViewSet)
router.register(r'subscriptions', views.SubscriptionViewSet)
router.register(r'financialrecords', views.FinancialRecordViewSet)
router.register(r'exercises', views.ExerciseViewSet)
router.register(r'exercisesets', views.ExerciseSetViewSet)
router.register(r'trainingprograms', views.TrainingProgramViewSet)
router.register(r'trainingsessions', views.TrainingSessionViewSet)
router.register(r'chats', views.ChatViewSet)
router.register(r'messages', views.MessageViewSet)
router.register(r'reactions', views.ReactionViewSet)
router.register(r'mailinglists', views.MailingListViewSet)
router.register(r'newsletters', views.NewsletterViewSet)
router.register(r'mailing', views.MailingViewSet)
# router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('streams/', views.StreamList.as_view(), name='stream-list'),
    path('send_signal/', views.send_signal, name='send-signal'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('start-stream', views.start_stream),
    path('api/', include((router.urls, 'api'), namespace='instance_name')),
    path('api/', include('rest_registration.api.urls')),
    path('get-message-reactions/', views.getMessageReactions, name='message-reactions-api'),
]
