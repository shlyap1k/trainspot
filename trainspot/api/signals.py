from django.core.mail import send_mail


def send_email_on_post(sender, instance, **kwargs):
    print('sender', sender)
    print(dir(sender))
    print('instance', instance)
    print(dir(instance))
    # send_mail(
    #     'Subject here',
    #     'Here is the message.',
    #     'mail-for-test-sending-emails@yandex.ru',
    #     ['4d.tyan@gmail.com'],
    #     fail_silently=False,
    # )