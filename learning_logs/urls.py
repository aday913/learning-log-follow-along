''' urls for learning_logs app '''

from django.urls import path

from . import views

urlpatterns = [
    # home page
    path('', views.index, name='index'),
    # page displaying all topics
    path('topics', views.topics, name='topics'),
    # page displaying all entries for a topic
    path('topics/<int:topic_id>', views.topic, name='topic'),
    # page for adding new topics
    path('new_topic', views.new_topic, name='new_topic'),
    # page for adding new entry for a given topic
    path('new_entry/<int:topic_id>', views.new_entry, name='new_entry'),
    # page to edit existing entries
    path('edit_entry/<int:entry_id>', views.edit_entry, name='edit_entry'),
]
