from django.contrib.sessions.models import Session
from django.utils import timezone
from .models import SessionProfile

class SessionBlockMiddleware:
    """
    Middleware for blocking duplicate sessions that are created when logging in multiple access
    To use:
        Add it to settings.MIDDLEWARE collection

    Main logic:
        If user dont have session -> create session
        else -> block all sessions except latest 
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Получаем текущую сессию пользователя
            session_key = request.session.session_key

            # Получаем профиль сессии пользователя
            profile = SessionProfile.objects.filter(session_key=session_key).first()

            # Если профиль сессии не найден, создаем новый
            if not profile:
                profile = SessionProfile(user_id=request.user.id, session_key=session_key, ip_address=request.META.get('REMOTE_ADDR'))
                profile.save()

            # Удаляем все активные сессии пользователя, кроме текущей
            active_sessions = SessionProfile.objects.filter(user_id=request.user.id).exclude(session_key=session_key)
            for session in active_sessions:
                session_key = session.session_key
                Session.objects.filter(session_key=session_key).delete()
                session.delete()

            # Обновляем информацию о последнем доступе
            profile.last_accessed = timezone.now()
            profile.save()

        response = self.get_response(request)
        return response