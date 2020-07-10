from django.contrib import admin

from .models import Thread, Reply


class ThreadAdmin(admin.ModelAdmin):

    list_display = ['title', 'author', 'created', 'modified']
    # author__email faz um join filtrando os autores com seus emails.
    search_fields = ['title', 'author__email', 'body']


class ReplyAdmin(admin.ModelAdmin):

    list_display = ['thread', 'author', 'created', 'modified']
    search_fields = ['thread__title', 'author__email', 'reply']


admin.site.register(Thread, ThreadAdmin)
admin.site.register(Reply, ReplyAdmin)