from django import forms
from .models import Company

class CompanyProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name', 'phone', 'logo', 'address'] # Exclude email as it's the USERNAME_FIELD
        widgets = {
            'address': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'