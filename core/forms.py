from django import forms
from .models import PDFDocument

class PDFUploadForm(forms.ModelForm):
    """Form for uploading PDF files"""
    
    class Meta:
        model = PDFDocument
        fields = ['title', 'file', 'summary_length']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = False
        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Optional document title'
        })
        self.fields['file'].widget.attrs.update({
            'class': 'form-control',
            'accept': 'application/pdf'
        })
        self.fields['summary_length'].widget.attrs.update({
            'class': 'form-select'
        })
        
    def clean_file(self):
        """Validate that the uploaded file is a PDF"""
        file = self.cleaned_data.get('file')
        if file:
            if not file.name.endswith('.pdf'):
                raise forms.ValidationError("Only PDF files are allowed.")
            return file
        else:
            raise forms.ValidationError("No file was uploaded.")