# -*- coding: UTF-8 -*-
from decorator import decorator
from rest_framework import status
from rest_framework.response import Response


@decorator
def mutable_request(function, view, request, *args, **kwargs):
    """
    Make the django request.DATA and request.POST objects mutable to allow us
    to change and add and or remove values to the request object.
    @ANTIPATTERN
    see: https://stackoverflow.com/questions/12611345/django-why-is-the-request-post-object-immutable
    """
    if hasattr(request.DATA, '_mutable'):
        request.DATA._mutable = True
    if hasattr(request.POST, '_mutable'):
        request.POST._mutable = True

    return function(view, request, *args, **kwargs)


@decorator
def valid_request_filesize(function, view, request, *args, **kwargs):
    """
    Check django request.FILES are all greater than bytesize 0
    """
    # if len(request.FILES.keys()) == 0 and len(request.POST.keys()) == 0 and len(request.GET.keys()) == 0:
    #     return Response({
    #         'executed_file': ["File appears to be corrupt filesize is 0 (no file presented)"],
    #         'attachment': ["File appears to be corrupt filesize is 0 (no file presented)"]
    #         }, status=status.HTTP_400_BAD_REQUEST)

    for file_name in request.FILES:
        try:

            if request.FILES.get(file_name).size <= 0:
                return Response({file_name: ["File appears to be corrupt filesize is 0"]}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({file_name: [e]}, status=status.HTTP_400_BAD_REQUEST)

    return function(view, request, *args, **kwargs)
