from django.contrib import admin
from .models import Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'skill_have', 'skill_want', 'short_description')
    list_filter = ('skill_have', 'skill_want', 'user')
    search_fields = ('skill_have', 'skill_want', 'description')
    ordering = ('-id',)
    list_per_page = 10

    def short_description(self, obj):
        if obj.description:
            return obj.description[:50] + "..."
        return "-"

    short_description.short_description = "Description"