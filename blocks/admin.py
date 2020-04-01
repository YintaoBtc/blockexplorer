from django.contrib import admin
from .models import Block

class BlockAdmin(admin.ModelAdmin):
    list_display = ("hash_block", "height", "weight",)

admin.site.register(Block, BlockAdmin)