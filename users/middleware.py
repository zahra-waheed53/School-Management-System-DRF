from django.http import HttpResponseForbidden

class UserRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_suspended:
            return HttpResponseForbidden("Access is forbidden.")
        response = self.get_response(request)
        return response