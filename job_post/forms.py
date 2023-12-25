from django import forms 
from job_post.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title', 'description', 'content']
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.TextInput(attrs={'class':'form-control'}),
            'content':forms.Textarea(attrs={'class':'form-control'}),
        }