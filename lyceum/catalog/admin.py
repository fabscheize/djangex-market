from django.contrib import admin

from catalog import models

__all__ = []


class MainImageInline(admin.StackedInline):
    model = models.ItemMainImage
    extra = 0
    readonly_fields = (models.ItemMainImage.get_image_300x300,)
    fields = ('image', models.ItemMainImage.get_image_300x300)


class ItemImageInline(admin.TabularInline):
    model = models.ItemImageGallery
    extra = 0
    readonly_fields = (models.ItemImageGallery.get_image_300x300,)
    fields = (models.ItemImageGallery.get_image_300x300, 'image')


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
