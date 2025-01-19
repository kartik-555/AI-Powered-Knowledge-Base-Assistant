# assistant/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import parsers, renderers, serializers, status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import QuerySerializer, FileUploadSerializer
from .utils import generate_answer_from_openai, retrieve_context, save_file
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView

class QueryView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = QuerySerializer(data=request.data)
        
        if serializer.is_valid():
            query = serializer.validated_data.get('query')
            context = retrieve_context(query) 
            answer = generate_answer_from_openai(query, context)
            return Response({"answer": answer}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DocumentUploadView(GenericAPIView):
    permission_classes = [AllowAny]
    throttle_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = FileUploadSerializer

    @swagger_auto_schema(
        operation_description="Upload a PDF file",
        manual_parameters=[
            openapi.Parameter(
                name="file",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
                description="Document"
            )
        ],
        responses={
            201: openapi.Response(description="File uploaded and processed successfully."),
            400: openapi.Response(description="No file uploaded or invalid file.")
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            file = serializer.validated_data['file']
            save_file(file)  # Custom logic for saving and indexing the file (PDF/Word)
            return Response({"message": "File uploaded and processed successfully."}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
