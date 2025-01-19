from rest_framework import serializers

class QuerySerializer(serializers.Serializer):
    query = serializers.CharField(max_length=1000, required=True)

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
