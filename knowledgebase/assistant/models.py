from django.db import models

class Document(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Embedding(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    chunk = models.TextField()
    vector = models.BinaryField()

    def __str__(self):
        return f"Embedding for {self.document.name}"
