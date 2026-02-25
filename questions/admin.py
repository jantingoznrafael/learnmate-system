from django.contrib import admin
from .models import Question, Answer, ReportedQuestion


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin configuration for Question model."""
    list_display = ['title', 'author', 'strand', 'status', 'created_at', 'answer_count']
    list_filter = ['status', 'strand', 'created_at']
    search_fields = ['title', 'body', 'author__username']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['approve_questions', 'reject_questions']

    def approve_questions(self, request, queryset):
        queryset.update(status='APPROVED')
        self.message_user(request, f'{queryset.count()} question(s) approved.')
    approve_questions.short_description = 'Approve selected questions'

    def reject_questions(self, request, queryset):
        queryset.update(status='REJECTED')
        self.message_user(request, f'{queryset.count()} question(s) rejected.')
    reject_questions.short_description = 'Reject selected questions'

    def answer_count(self, obj):
        return obj.answer_count
    answer_count.short_description = 'Answers'


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """Admin configuration for Answer model."""
    list_display = ['question', 'author', 'created_at']
    list_filter = ['created_at']
    search_fields = ['body', 'author__username', 'question__title']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ReportedQuestion)
class ReportedQuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'strand', 'status', 'created_at', 'report_reason']
    readonly_fields = ['created_at', 'updated_at', 'report_reason']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_reported=True)

    def has_add_permission(self, request):
        return False
