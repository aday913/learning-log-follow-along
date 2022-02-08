# from socket import fromshare
from django import forms
# from matplotlib import widgets

from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    '''
    Form to create a new topic given user input
    '''
    class Meta:
        model = Topic
        fields = ['text', 'public']
        labels = {'text' : '', 'public': 'Make Public?'}

class EntryForm(forms.ModelForm):
    '''
    Form to add in a new entry for a given topic
    '''
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}