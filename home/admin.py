from django.contrib import admin
from .models import Skill, Profile, SwapRequest


# ==========================
# Skill Admin
# ==========================
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "skill_have",
        "skill_want",
        "created_at",
        "short_description",
    )

    list_display_links = (
        "id",
        "skill_have",
    )

    list_filter = (
        "created_at",
        "skill_have",
        "skill_want",
    )

    search_fields = (
        "user__username",
        "skill_have",
        "skill_want",
        "description",
    )

    ordering = ("-created_at",)

    list_per_page = 15

    readonly_fields = ("created_at",)

    def short_description(self, obj):
        if len(obj.description) > 50:
            return obj.description[:50] + "..."
        return obj.description

    short_description.short_description = "Description"


# ==========================
# Profile Admin
# ==========================
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "is_premium",
    )

    list_filter = (
        "is_premium",
    )

    search_fields = (
        "user__username",
    )

    ordering = ("user",)


# ==========================
# Swap Request Admin
# ==========================
@admin.register(SwapRequest)
class SwapRequestAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "sender",
        "receiver",
        "skill",
        "status",
        "created_at",
    )

    list_display_links = (
        "id",
        "sender",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "sender__username",
        "receiver__username",
        "skill__skill_have",
    )

    ordering = ("-created_at",)

    list_per_page = 15

    readonly_fields = (
        "created_at",
    )