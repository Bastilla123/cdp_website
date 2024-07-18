from django.conf import settings
def middleware(request):
    context = {}
    context['app_title'] = settings.APP_TITLE
    return context