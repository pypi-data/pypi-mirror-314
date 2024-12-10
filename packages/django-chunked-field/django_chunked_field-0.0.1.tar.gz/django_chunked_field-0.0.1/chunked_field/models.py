from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class DataChunk(models.Model):
    """
    Model to store chunks of data for a field in a Django model.

    Attributes:
        content_type (ForeignKey): Reference to the ContentType of the model.
        object_id (PositiveIntegerField): ID of the model instance.
        field_name (CharField): Name of the field being chunked.
        sequence (PositiveIntegerField): Sequence number of the chunk.
        content (CharField): The actual chunk of data.
        content_object (GenericForeignKey): Generic foreign key to the model instance.
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    field_name = models.CharField(max_length=100)
    sequence = models.PositiveIntegerField()
    content = models.CharField(max_length=4000)

    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('content_type', 'object_id', 'field_name', 'sequence')
        ordering = ['sequence']

    def __str__(self):
        return f"Chunk {self.sequence} for {self.content_object}"
