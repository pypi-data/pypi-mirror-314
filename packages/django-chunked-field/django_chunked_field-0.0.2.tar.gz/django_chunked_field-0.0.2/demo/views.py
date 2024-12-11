from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from demo.models import MyModel
from demo.serializers import MyModelSerializer


class MyModelAPIView(APIView):
    def get(self, request, *args, **kwargs):
        mymodels = MyModel.objects.all()
        serializer = MyModelSerializer(mymodels, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = MyModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
