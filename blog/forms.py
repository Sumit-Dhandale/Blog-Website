from django import forms
from .models import Post,Comments

class PostForm(forms.ModelForm):

    class Meta():
        model=Post
        # fields=('author','title','text')
        fields=('title','text')

        widgets={
            'title':forms.TextInput(attrs={'class':'border border-dark textinputclass'}),
            'text':forms.Textarea(attrs={'class':'border border-dark editable medium-editor-textarea postcontent'})
        }

class CommentsForm(forms.ModelForm):

    class Meta():
        model=Comments
        fields=('author','text')

        widgets={
            'author':forms.TextInput(attrs={'class':'border border-dark textinputclass'}),
            'text':forms.Textarea(attrs={'class':'border border-dark editable medium-editor-textarea postcontent'})
        }



