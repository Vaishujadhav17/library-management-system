from django.contrib import admin

from .models import BookIssue, BookRequest


admin.site.register(BookRequest)
admin.site.register(BookIssue)