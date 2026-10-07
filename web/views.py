from django.http import HttpResponse, JsonResponse


def home(request):
    return HttpResponse("""
    <html>
        <head>
            <title>Jenkins Django Demo</title>
        </head>
        <body>
            <h1>Jenkins Django Deployment</h1>
            <p>The Django application is running successfully.</p>
        </body>
    </html>
    """)


def health(request):
    return JsonResponse({
        "status": "healthy",
        "application": "jenkins-django-demo"
    })
