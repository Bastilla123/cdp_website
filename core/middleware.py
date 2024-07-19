from django.conf import settings
def middleware(request):
    context = {}
    context['app_title'] = settings.APP_TITLE
    context['base_template'] = settings.BASE_TEMPLATE
    return context