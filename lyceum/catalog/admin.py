from catalog import models
from django.contrib import admin
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail


class ItemImageInline(admin.TabularInline):
    model = models.ItemImage
    extra = 0
    fields = (models.ItemImage.get_image, 'image')
    readonly_fields = (models.ItemImage.get_image,)


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        models.Item.name.field.name,
        models.Item.is_published.field.name,
        models.Item.get_main_image,
    )
    list_editable = (models.Item.is_published.field.name,)
    list_display_links = (models.Item.name.field.name,)
    filter_horizontal = (models.Item.tags.field.name,)
    inlines = [ItemImageInline]
    readonly_fields = (models.Item.get_main_image,)



@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        models.Tag.name.field.name,
        models.Tag.is_published.field.name,
    )
    list_editable = (models.Tag.is_published.field.name,)
    list_display_links = (models.Tag.name.field.name,)


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        models.Category.name.field.name,
        models.Category.is_published.field.name,
    )
    list_editable = (models.Category.is_published.field.name,)
    list_display_links = (models.Category.name.field.name,)
    list_display_links = (models.Category.name.field.name,)
