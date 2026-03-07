from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
import json

from services.auth_service.application.use_cases.register_user import register_user, RegistrationError
from services.auth_service.application.use_cases.login_user import login_user, AuthenticationError
from services.auth_service.application.use_cases.reset_password import reset_password, ResetError
from services.auth_service.infrastructure.repositories import UserRepository, RefreshTokenRepository
from shared.message_bus import InMemoryMessageBus


_bus = InMemoryMessageBus()
_user_repo = UserRepository()
_token_repo = RefreshTokenRepository()


def _parse_body(request: HttpRequest) -> dict:
    try:
        return json.loads(request.body)
    except:
        return {}


@csrf_exempt
def register(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({"error": "method not allowed"}, status=405)
    data = _parse_body(request)
    try:
        result = register_user(data.get("email"), data.get("password"),
                               user_repo=_user_repo, bus=_bus)
        return JsonResponse(result, status=201)
    except RegistrationError as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def login(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({"error": "method not allowed"}, status=405)
    data = _parse_body(request)
    try:
        return JsonResponse(login_user(data.get("email"), data.get("password"),
                                       is_admin=data.get("is_admin", False),
                                       user_repo=_user_repo, token_repo=_token_repo, bus=_bus))
    except AuthenticationError as e:
        return JsonResponse({"error": str(e)}, status=401)


@csrf_exempt
def password_reset(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({"error": "method not allowed"}, status=405)
    data = _parse_body(request)
    try:
        reset_password(data.get("email"), data.get("new_password"),
                       user_repo=_user_repo, bus=_bus)
        return JsonResponse({"status": "ok"})
    except ResetError as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def admin_login(request: HttpRequest):
    # reuse login with is_admin flag
    request.META["HTTP_IS_ADMIN"] = True
    return login(request)
