from django.contrib import admin
from .models import Question, Choice


class ChoiceInline(admin.TabularInline):  # shows choices on the Question edit page
    model = Choice
    extra = 3


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

    # Columns on the Questions list page
    list_display = ("question_text", "pub_date")

    # Right-side filters
    list_filter = ("pub_date",)

    # Search box (top right)
    search_fields = ("question_text",)

    date_hierarchy = "pub_date"
    fieldsets = (
        (None, {"fields": ("question_text",)}),
        ("Date information", {"fields": ("pub_date",)}),
    )
