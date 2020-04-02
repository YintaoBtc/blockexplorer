from django.views.generic import ListView, DetailView

from .models import Block


class BlockListView(ListView):
    model = Block
    context_object_name = 'block_list'
    template_name = 'blocks/block_list.html'


class BlockDetailView(DetailView): 
    model = Block
    context_object_name = 'block_obj'
    template_name = 'blocks/block_detail.html'