# from django.contrib.auth.models import User, Group
from wsgiref.util import FileWrapper
import jinja2
import pdfkit
import os
from calendar import monthrange
from django.db.models import Sum, Case, When, F, DecimalField
from django.db.models.functions import TruncYear, TruncMonth
from django.http import HttpResponse, FileResponse, HttpResponseForbidden
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, renderers, status, generics
from rest_framework import permissions
from rest_framework.decorators import api_view, action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from xhtml2pdf import pisa

from api.serializers import *
from api.models import *
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.http import StreamingHttpResponse
from django.views.decorators import gzip
import cv2
from django.http import JsonResponse
import django_eventstream
from pusher import Pusher
from trainspot.settings import PUSHER_APP_ID, PUSHER_API_KEY, PUSHER_SECRET_KEY, PUSHER_CLUSTER

# @csrf_exempt
def pusher_auth(request):
    print({'test': 'success',
                'user_info': {  # We can put whatever we want here
                                'username': request.user.username,
                                'first_name': request.user.first_name,
                                'last_name': request.user.last_name,
                            }
                })
    print(request.POST)
    # print(request.data)
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    pusher_client = Pusher(app_id=PUSHER_APP_ID, key=PUSHER_API_KEY,
                           secret=PUSHER_SECRET_KEY, cluster=PUSHER_CLUSTER, ssl=False)

    # We must generate the token with pusher's service
    payload = pusher_client.authenticate(
        channel=request.POST['channel_name'],
        socket_id=request.POST['socket_id'],
        custom_data={
            'user_id': request.user.id,
            'user_info': {  # We can put whatever we want here
                'username': request.user.username,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
            }
        })
    # payload = {'test': 'success',
    #            'user_info': {  # We can put whatever we want here
    #                            'username': request.user.username,
    #                            'first_name': request.user.first_name,
    #                            'last_name': request.user.last_name,
    #                        }
    #            }
    return JsonResponse(payload)

@csrf_exempt
def send_signal(request):
    data = request.POST
    django_eventstream.send_event('stream', 'signal', data)
    return JsonResponse({'status': 'ok'})

class StreamList(generics.ListCreateAPIView):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer


# Функция для получения видео потока с вебки
def generate_video():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Преобразование кадра в байты
        frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
        # Отправка кадра на фронтенд потоково
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@gzip.gzip_page
def video_feed(request):
    print('TEST')
    resp = StreamingHttpResponse(generate_video(), content_type="multipart/x-mixed-replace;boundary=frame")
    print(resp.streaming_content)
    return resp


def start_stream(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'stream_group',
        {'type': 'stream_message', 'message': 'video_data'}
    )
    return Response({'status': 'success'})


class ReadOnlyOrAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    def get_permissions(self):
        if self.action == 'list':
            return [ReadOnlyOrAuthenticated()]
        else:
            return [IsAuthenticated()]

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
        return [AllowAny()]


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


class PassthroughRenderer(renderers.BaseRenderer):
    """
        Return data as-is. View should supply a Response.
    """
    media_type = 'application/pdf'
    format = 'pdf'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


def get_pricelist_pdf(context):
    template_loader = jinja2.FileSystemLoader(f'{os.getcwd()}/trainspot/static/pdf/price_list')
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template('price_list.html')
    output_text = template.render(context)
    config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_PATH)
    pdfkit.from_string(output_text,
                       f'{os.getcwd()}/price_list.pdf',
                       configuration=config,
                       css=f'{os.getcwd()}/trainspot/static/pdf/price_list/price_list.css')


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def paginate_queryset(self, queryset):
        if 'limit' not in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)
    def get_permissions(self):
        if self.action == 'list' or self.action == 'download':
            return [ReadOnlyOrAuthenticated()]
        else:
            return [IsAuthenticated()]

    @action(methods=['GET'], detail=True, renderer_classes=(PassthroughRenderer,))
    def download(self, request, *args, **kwargs):
        plans = Plan.objects.all()
        context = {"plans": plans}
        get_pricelist_pdf(context)
        file_handle = open(f'{os.getcwd()}/price_list.pdf', "rb")
        response = FileResponse(file_handle, content_type='application/pdf')
        response['Content-Length'] = os.stat(
            f"{os.getcwd()}/price_list.pdf").st_size
        response['Content-Disposition'] = f'attachment; filename="price_list.pdf"'
        print(response['Content-Disposition'])
        return response



class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'user__id'



def get_personal_report_pdf(context):
    user_id = context['user'].id
    template_loader = jinja2.FileSystemLoader(f'{os.getcwd()}/trainspot/static/pdf/user_report')
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template('report.html')
    output_text = template.render(context)
    config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_PATH)
    pdfkit.from_string(output_text,
                       f'{os.getcwd()}/personal_report_{user_id}.pdf',
                       configuration=config,
                       css=f'{os.getcwd()}/trainspot/static/pdf/user_report/report.css')


def get_overall_report_pdf(context):
    print(os.getcwd())
    template_loader = jinja2.FileSystemLoader(f'{os.getcwd()}/trainspot/static/pdf/company_report')
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template('report.html')
    output_text = template.render(context)
    config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_PATH)
    pdfkit.from_string(output_text,
                       f'{os.getcwd()}/overall_report.pdf',
                       configuration=config,
                       css=f'{os.getcwd()}/trainspot/static/pdf/company_report/report.css')



class FinancialRecordViewSet(viewsets.ModelViewSet):
    queryset = FinancialRecord.objects.all()
    serializer_class = FinancialRecordSerializer
    permission_classes = [permissions.IsAuthenticated]


    def _download_personal_report(self, user):
        finances = FinancialRecord.objects.filter(user=user)
        data = {
            'user': user,
            'finances': sorted(finances, key=lambda f: f.date),
            'sum': sum([f.amount for f in finances]),
            'today': str(timezone.now())[0:11]
        }
        get_personal_report_pdf(data)
        file_handle = open(f'{os.getcwd()}\personal_report_{user.id}.pdf', "rb")
        response = FileResponse(file_handle, content_type='application/pdf')
        response['Content-Length'] = os.stat(
            f"{os.getcwd()}\personal_report_{user.id}.pdf").st_size
        response['Content-Disposition'] = f'attachment; filename="personal_report_{user.id}.pdf"'
        print(response['Content-Disposition'])
        return response


    def _download_overall_report(self, start=None, end=None):
        if start:
            finances = sorted(FinancialRecord.objects.filter(date__range=(start, end)),
                              key=lambda f: f.date)


            records = FinancialRecord.objects.filter(date__range=(start, end)).annotate(
                month=TruncMonth('date')
            ).values('month').annotate(
                total_income=Sum(
                    Case(When(type=FinancialRecord.INCOME, then=F('amount')), default=0, output_field=DecimalField())
                ),
                total_expense=Sum(
                    Case(When(type=FinancialRecord.EXPENSE, then=F('amount')), default=0, output_field=DecimalField())
                )
            ).annotate(
                total_profit=F('total_income') - F('total_expense')
            ).order_by('month')
        else:
            start = 'открытия'
            end = 'текущий момент'
            finances = sorted(FinancialRecord.objects.all(),
                              key=lambda f: f.date)
            records = FinancialRecord.objects.all().annotate(
                month=TruncMonth('date')
            ).values('month').annotate(
                total_income=Sum(
                    Case(When(type=FinancialRecord.INCOME, then=F('amount')), default=0, output_field=DecimalField())
                ),
                total_expense=Sum(
                    Case(When(type=FinancialRecord.EXPENSE, then=F('amount')), default=0, output_field=DecimalField())
                )
            ).annotate(
                total_profit=F('total_income') - F('total_expense')
            ).order_by('month')

        for r in records:
            month = FinancialRecord(user_id=1, date=r['month'], amount=r['total_profit'],
                                    description=f'<b>Итог месяца {r["month"].month}</b>', type=3)
            month.date = month.date.replace(day=monthrange(month.date.year, month.date.month)[1])
            finances.append(month)

        data = {
            'finances': sorted(finances, key=lambda f: f.date),
            'sum': sum([f.amount for f in finances if f.type == 1]) - sum([f.amount for f in finances if f.type == 2]),
            'today': str(timezone.now())[0:11],
            'start': start,
            'end': end
        }
        get_overall_report_pdf(data)
        file_handle = open(f'{os.getcwd()}/overall_report.pdf', "rb")
        response = FileResponse(file_handle, content_type='application/pdf')
        response['Content-Length'] = os.stat(
            f"{os.getcwd()}/overall_report.pdf").st_size
        response['Content-Disposition'] = f'attachment; filename="overall_report.pdf"'
        print(response)
        return response


    @action(methods=['GET'], detail=True, renderer_classes=(PassthroughRenderer,))
    def download(self, request, *args, **kwargs):
        print(request)
        user = request.user
        if user.role == 'client':
            print('client')
            return self._download_personal_report(user)
        else:
            try:
                return self._download_overall_report(request.GET['start'], request.GET['end'])
            except MultiValueDictKeyError:
                return self._download_overall_report()


    def list(self, request, *args, **kwargs):
        user = request.user
        if user.role == 'client':
            queryset = FinancialRecord.objects.filter(user=user).order_by('date')
            serializer = FinancialRecordSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            queryset = FinancialRecord.objects.all().order_by('date')
            serializer = FinancialRecordSerializer(queryset, many=True)
            return Response(serializer.data)


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

    def create(self, request, *args, **kwargs):
        to_save = True
        try:
            current = Reaction.objects.filter(message_id=request.data['message'], author_id=request.data['author'])
        except Reaction.DoesNotExist:
            current = None
        if current:
            for c in current:
                if c.type == request.data['type']:
                    to_save = False
                c.delete()
        reaction = Reaction(type=request.data['type'], author_id=request.data['author'], message_id=request.data['message'])
        if (to_save):
            reaction.save()
        return Response(status=200)


import logging

logger = logging.getLogger(__name__)
class MailingListViewSet(viewsets.ModelViewSet):
    queryset = MailingList.objects.all()
    serializer_class = MailingListSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        # Исключаем subscribers из полей, передаваемых для валидации
        request_data = request.data.copy()
        subscribers_data = request_data.pop('subscribers', [])
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        mailing_list = self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['POST'], detail=True)
    def subscribe(self, request, *args, **kwargs):
        mailing_list = self.get_object()
        user = request.user
        if user:
            mailing_list.subscribers.add(user)
            return Response({'detail': 'Successfully subscribed.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'User is not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['POST'], detail=True)
    def unsubscribe(self, request, *args, **kwargs):
        mailing_list = self.get_object()
        user = request.user
        if user:
            mailing_list.subscribers.remove(user)
            return Response({'detail': 'Successfully unsubscribed.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'User is not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)


class MailingViewSet(viewsets.ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer
    permission_classes = [permissions.IsAuthenticated]


class NewsletterViewSet(viewsets.ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
def getMessageReactions(request):
    return Response({"message": "Hello, world!"})
# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]
