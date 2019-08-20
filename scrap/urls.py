from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(),name='index'),
    path('add/', AddAutomation.as_view(),name='add'),
    path('show', ShowAutomations.as_view(),name='show'),
    path('linked/', Linked.as_view(),name='linked'),
    path('user', User.as_view(),name='user'),
    path('status', Changestatus.as_view(),name='status'),
    path('thread', StartThread.as_view(),name='thread'),
    path('stop', StopThread.as_view(),name='stop'),
    path('alldata', AllData.as_view(),name='alldata'),
    path('reject', Reject.as_view(),name='reject'),
    path('database', Database.as_view(),name='database'),
    path('delete-automation', DeleteAutomation.as_view(),name='delete_automation'),
    path('delete-user', DeleteUser.as_view(),name='delete_user'),
    path('edit-automation/<id>', EditAutomation.as_view(),name='edit_automation'),
    path('edit-user/<id>', EditUser.as_view(),name='edit_user'),
    path('add-cron', AddCron.as_view(),name='addcron'),
    path('pause', PauseSchduale.as_view(),name='pause'),
    path('changestatus', ChangeAllStatus.as_view(),name='changestatus'),
    path('actions', Actions.as_view(),name='actions'),
    
   


]
