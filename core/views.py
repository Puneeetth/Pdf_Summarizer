import os
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.contrib import messages

from .models import PDFDocument
from .forms import PDFUploadForm
from .services.pdf_service import PDFService
from .services.gemini_service import GeminiService

def home(request):
    """Home page with PDF upload form"""
    form = PDFUploadForm()
    context = {
        'form': form,
        'recent_documents': PDFDocument.objects.filter(summary_completed=True)[:5]
    }
    return render(request, 'core/home.html', context)

@require_http_methods(["POST"])
def upload_pdf(request):
    """Handle PDF upload and processing"""
    form = PDFUploadForm(request.POST, request.FILES)
    
    if form.is_valid():
        # Save the document
        document = form.save(commit=False)
        document.file_size = document.file.size // 1024  # Convert to KB
        document.save()
        
        try:
            # Extract text
            pdf_service = PDFService()
            extracted_text, extraction_time = pdf_service.extract_text(document.file)
            
            # Update document with extracted text
            document.extracted_text = extracted_text
            document.extraction_completed = True
            document.processing_time += extraction_time
            document.save()
            
            # Generate summary
            gemini_service = GeminiService()
            summary, summary_time = gemini_service.generate_summary(
                extracted_text, 
                length=document.summary_length
            )
            
            # Update document with summary
            document.summary = summary
            document.summary_completed = True
            document.processing_time += summary_time
            document.save()
            
            # Redirect to summary page
            return redirect('summary', pk=document.pk)
            
        except Exception as e:
            # Handle errors
            if "extraction" in str(e).lower():
                document.extraction_error = str(e)
            else:
                document.summary_error = str(e)
            document.save()
            
            messages.error(request, f"Error processing PDF: {str(e)}")
            return redirect('home')
    else:
        # Form validation errors
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{field}: {error}")
        return redirect('home')

def summary_view(request, pk):
    """Display summary results for a specific document"""
    document = get_object_or_404(PDFDocument, pk=pk)
    context = {'document': document}
    return render(request, 'core/summary.html', context)

# API endpoints for AJAX requests
@require_http_methods(["GET"])
def check_processing_status(request, pk):
    """API endpoint to check document processing status"""
    try:
        document = PDFDocument.objects.get(pk=pk)
        data = {
            'id': document.id,
            'extraction_completed': document.extraction_completed,
            'extraction_error': document.extraction_error,
            'summary_completed': document.summary_completed,
            'summary_error': document.summary_error,
            'processing_time': document.processing_time
        }
        return JsonResponse(data)
    except PDFDocument.DoesNotExist:
        return JsonResponse({'error': 'Document not found'}, status=404)