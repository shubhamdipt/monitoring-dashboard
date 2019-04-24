from django.urls import path
from servers.views import add_server_data

app_name = "servers"
urlpatterns = [
    path('data', add_server_data, name='add_server_data'),
]
