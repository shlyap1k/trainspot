# from django.contrib.auth.models import User, Group
from wsgiref.util import FileWrapper
import jinja2
import pdfkit
import os
from calendar import monthrange
from django.db.models import Sum, Case, When, F, DecimalField
from django.db.models.functions import TruncYear, TruncMonth
from django.http import HttpResponse, FileResponse
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import viewsets, renderers
from rest_framework import permissions
from rest_framework.decorators import api_view, action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from xhtml2pdf import pisa

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


class PassthroughRenderer(renderers.BaseRenderer):
    """
        Return data as-is. View should supply a Response.
    """
    media_type = 'application/pdf'
    format = 'pdf'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


def get_pricelist_pdf(context):
    template_loader = jinja2.FileSystemLoader('C:\\Users\\4dtya\Pycharmprojects\\trainspot1111\\trainspot\static\pdf\\price_list')
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template('price_list.html')
    output_text = template.render(context)
    config = pdfkit.configuration(wkhtmltopdf='C:\Program Files\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    pdfkit.from_string(output_text,
                       f'C:\\Users\\4dtya\Pycharmprojects\\trainspot1111\price_list.pdf',
                       configuration=config,
                       css='C:\\Users\\4dtya\Pycharmprojects\\trainspot1111\\trainspot\static\pdf\\price_list\\price_list.css')


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    # permission_classes = [permissions.IsAuthenticated]
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
        file_handle = open(f'C:\\Users\\4dtya\Pycharmprojects\\trainspot1111\price_list.pdf', "rb")
        response = FileResponse(file_handle, content_type='application/pdf')
        response['Content-Length'] = os.stat(
            f"C:\\Users\\4dtya\Pycharmprojects\\trainspot1111\price_list.pdf").st_size
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
    template_loader = jinja2.FileSystemLoader('C:\\Users\\4dtya\Pycharmprojects\\trainspot1111\\trainspot\static\pdf\\user_report')
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template('report.html')
    output_text = template.render(context)
    config = pdfkit.configuration(wkhtmltopdf='C:\Program Files\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    pdfkit.from_string(output_text,
                       f'C:\\Users\\4dtya\Pycharmprojects\\trainspot1111\personal_report_{user_id}.pdf',
                       configuration=config,
                       css='C:\\Users\\4dtya\Pycharmprojects\\trainspot1111\\trainspot\static\pdf\\user_report\\report.css')


def get_overall_report_pdf(context):
    template_loader = jinja2.FileSystemLoader('C:\\Users\\4dtya\Pycharmprojects\\trainspot1111\\trainspot\static\pdf\\company_report')
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template('report.html')
    output_text = template.render(context)
    config = pdfkit.configuration(wkhtmltopdf='C:\Program Files\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    pdfkit.from_string(output_text,
                       f'C:\\Users\\4dtya\Pycharmprojects\\trainspot1111\overall_report.pdf',
                       configuration=config,
                       css='C:\\Users\\4dtya\Pycharmprojects\\trainspot1111\\trainspot\static\pdf\\company_report\\report.css')



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
        file_handle = open(f'C:\\Users\\4dtya\Pycharmprojects\\trainspot1111\personal_report_{user.id}.pdf', "rb")
        response = FileResponse(file_handle, content_type='application/pdf')
        response['Content-Length'] = os.stat(
            f"C:\\Users\\4dtya\Pycharmprojects\\trainspot1111\personal_report_{user.id}.pdf").st_size
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
        file_handle = open(f'C:\\Users\\4dtya\Pycharmprojects\\trainspot1111\overall_report.pdf', "rb")
        response = FileResponse(file_handle, content_type='application/pdf')
        response['Content-Length'] = os.stat(
            f"C:\\Users\\4dtya\Pycharmprojects\\trainspot1111\overall_report.pdf").st_size
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
            queryset = FinancialRecord.objects.filter(user=user)
            serializer = FinancialRecordSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            queryset = FinancialRecord.objects.all()
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


class MailingListViewSet(viewsets.ModelViewSet):
    queryset = MailingList.objects.all()
    serializer_class = MailingListSerializer
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
