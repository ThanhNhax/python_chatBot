from django.contrib import admin
from .models import Intent, UnresolvedQuestion

@admin.register(Intent)
class IntentAdmin(admin.ModelAdmin):
    list_display = ('tag', 'answer_preview')
    search_fields = ('tag', 'keywords')

    def answer_preview(self, obj):
        return obj.answer[:50] + '...' if len(obj.answer) > 50 else obj.answer
    answer_preview.short_description = 'Câu trả lời'

@admin.register(UnresolvedQuestion)
class UnresolvedQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at')
    search_fields = ('question',)
    ordering = ('-created_at',)

