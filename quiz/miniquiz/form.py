from django import forms

from .models import *
class ImageForm(forms.ModelForm):
    categoryName=forms.CharField(widget=forms.TextInput(attrs={"class": "form-control","placeholder":"Category Name"}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':3,"placeholder":"Category Description"}))


    class Meta:
        model=Category
        fields=['categoryImage','categoryName','description']
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)


        


