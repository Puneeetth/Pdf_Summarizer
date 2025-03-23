from django.db import models
from django.utils import timezone
import uuid
import os

def pdf_upload_path(instance, filename):
    """Generate unique path for uploaded PDFs"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('pdfs', filename)

class PDFDocument(models.Model):
    """Model to store information about uploaded PDFs and their summaries"""
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to=pdf_upload_path)
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_size = models.IntegerField(default=0)  # Size in KB
    
    # Extracted content
    extracted_text = models.TextField(blank=True)
    extraction_completed = models.BooleanField(default=False)
    extraction_error = models.TextField(blank=True)
    
    # Summary data
    summary = models.TextField(blank=True)
    summary_completed = models.BooleanField(default=False)
    summary_length = models.CharField(
        max_length=10,
        choices=[('short', 'Short'), ('medium', 'Medium'), ('long', 'Long')],
        default='medium'
    )
    summary_error = models.TextField(blank=True)
    
    # Processing metadata
    processing_time = models.FloatField(default=0)  # Time in seconds
    
    def __str__(self):
        return self.title or f"PDF Document {self.id}"
    
    class Meta:
        ordering = ['-uploaded_at']