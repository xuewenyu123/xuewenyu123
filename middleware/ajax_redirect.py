from django.http import JsonResponse


# pylint: disable=C0111,R1710,W0613


class AJAXRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print('ajax_redirect')
        response = self.get_response(request)
        if response.status_code in [301, 302] and (request.is_ajax() or request.META.get('X-Requested-With') == "XMLHttpRequest"):
            return JsonResponse(
                {
                    "_redirected": True,
                    "_location": response["LOCATION"],
                },
            ) # status=302)   # pragma: no cover
        return response
