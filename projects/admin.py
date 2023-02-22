from django.contrib import admin
from .models import Project

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at',)
    list_filter = ('created_at', 'public_status',)
    search_fields = ('name', 'owner', 'public_status',)
    date_hierarchy = 'created_at'

admin.site.register(Project, ProjectAdmin)