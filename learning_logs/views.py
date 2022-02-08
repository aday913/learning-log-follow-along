from itertools import chain

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    """The home page for Learning Log"""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    '''
    Show all the topics for the user
    '''
    topics1 = Topic.objects.filter(owner=request.user).order_by('date_added')
    topics2 = Topic.objects.filter(public=True)
    topic_list = list(chain(topics1, topics2))
    context = {'topics': topic_list}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    '''
    Show all entries for a topic
    '''
    topic = get_object_or_404(Topic, id=topic_id)
    # make sure the topic belongs to the current user
    if topic.owner != request.user and not topic.public:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    '''
    Add a new topic given user input
    '''
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    '''
    Add a new entry for a given topic
    '''
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(
                reverse('learning_logs:topic', args=[topic_id])
            )
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    '''
    Edit existing entry by entry id
    '''
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(data=request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('learning_logs:topic', args=[topic.id])
            )
    context = {'topic': topic, 'form': form, 'entry': entry}
    return render(request, 'learning_logs/edit_entry.html', context)