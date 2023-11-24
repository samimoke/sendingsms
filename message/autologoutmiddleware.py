import json
from datetime import datetime, timedelta
from django.contrib.auth import logout
from django.conf import settings

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            if last_activity is not None:
                last_activity = datetime.strptime(last_activity, "%Y-%m-%dT%H:%M:%S.%f")
                inactive_duration = datetime.now() - last_activity
                if inactive_duration > timedelta(seconds=settings.SESSION_COOKIE_AGE):
                    logout(request)
                    request.session.flush()
            request.session['last_activity'] = datetime.now().isoformat()

        response = self.get_response(request)
        return response

