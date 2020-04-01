from django.urls import path

from .views import BlockListView, BlockDetailView

urlpatterns = [
    path('', BlockListView.as_view(), name='block_list'),
    path('<uuid:pk>', BlockDetailView.as_view(), name='block_detail'),
]