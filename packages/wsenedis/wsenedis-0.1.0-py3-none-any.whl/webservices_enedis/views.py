
from rest_framework.response import Response
from rest_framework.views import APIView



class Health(APIView):

    def get(self, request, format=None):
        return Response('ok')



