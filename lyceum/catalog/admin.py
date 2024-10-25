from django.contrib import admin

from catalog import models

__all__ = []


class MainImageInline(admin.StackedInline):
    model = models.MainImage
    extra = 0
    readonly_fields = (models.MainImage.get_image,)
    fields = ('image', models.MainImage.get_image)


class ItemImageInline(admin.TabularInline):
    model = models.ItemImage
    extra = 0
    readonly_fields = (models.ItemImage.get_image,)
    fields = (models.ItemImage.get_image, 'image')


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

    inlines = [MainImageInline, ItemImageInline]


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
