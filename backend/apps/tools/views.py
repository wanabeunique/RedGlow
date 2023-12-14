import json
from django.http import JsonResponse


def openapi_spec(request):
    with open('apiSpecification.json')as f:
        openapi = json.load(f)

    return JsonResponse(openapi, safe=False)
