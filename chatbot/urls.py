# urls.py của app: địa chỉ nào thì gọi hàm nào trong views.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.trang_chat, name="trang_chat"),      # http://127.0.0.1:8000/
    path("chat/", views.chat_api, name="chat_api"),     # http://127.0.0.1:8000/chat/?q=...
]
