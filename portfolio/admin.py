from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Contact, Skill, Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "featured", "created_at")
    list_filter = ("featured",)
    search_fields = ("title", "technologies")


admin.site.register(User, UserAdmin)
admin.site.register(Contact)
admin.site.register(Skill)