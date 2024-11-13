from django.contrib import admin

from feedback import models

__all__ = []


class FeedbackAuthorInline(admin.StackedInline):
    model = models.FeedbackAuthor
    extra = 0
    can_delete = False
    readonly_fields = (
        models.FeedbackAuthor.name.field.name,
        models.FeedbackAuthor.mail.field.name,
    )


class FeedbackFileInline(admin.TabularInline):
    model = models.FeedbackFile
    extra = 0
    max_num = 0
    can_delete = False
    readonly_fields = (models.FeedbackFile.file.field.name,)


@admin.register(models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        models.Feedback.text.field.name,
        models.Feedback.status.field.name,
    )
    readonly_fields = (
        models.Feedback.text.field.name,
        models.Feedback.created_on.field.name,
    )
    list_display_links = (models.Feedback.text.field.name,)
    inlines = [FeedbackAuthorInline, FeedbackFileInline]

    def save_model(self, request, obj, form, change):
        if change:
            old_status = models.Feedback.objects.get(pk=obj.pk).status
            if old_status != obj.status:
                models.StatusLog.objects.create(
                    user=request.user,
                    feedback=obj,
                    from_status=old_status,
                    to=obj.status,
                )

        super().save_model(request, obj, form, change)


@admin.register(models.StatusLog)
class StatusLogAdmin(admin.ModelAdmin):
    list_display = (
        models.StatusLog.timestamp.field.name,
        models.StatusLog.feedback.field.name,
        models.StatusLog.from_status.field.name,
        models.StatusLog.to.field.name,
    )
    readonly_fields = (
        models.StatusLog.feedback.field.name,
        models.StatusLog.from_status.field.name,
        models.StatusLog.to.field.name,
        models.StatusLog.user.field.name,
    )
    list_display_links = (models.StatusLog.timestamp.field.name,)
