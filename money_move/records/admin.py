from django.contrib import admin
from django.contrib.auth.models import Group, User
from more_admin_filters import MultiSelectRelatedFilter
from rangefilter.filters import DateRangeFilterBuilder

from .models import Category, Record, Status, Subcategory, Type


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    fields = (
        'created_at', 'status', 'type', 'category',
        'subcategory', 'amount', 'comment',
    )
    list_filter = (
        ('created_at', DateRangeFilterBuilder()),
        ('status', MultiSelectRelatedFilter),
        ('subcategory__category__type', MultiSelectRelatedFilter),
        ('subcategory__category', MultiSelectRelatedFilter),
        ('subcategory', MultiSelectRelatedFilter),
    )
    search_fields = (
        'status__name', 'subcategory__category__type__name',
        'subcategory__category__name', 'subcategory__name',
    )
    readonly_fields = ('type', 'category')
    autocomplete_fields = ('subcategory',)

    def type(self, obj):
        return obj.subcategory.category.type

    def category(self, obj):
        return obj.subcategory.category

    type.short_description = 'Тип (согласно подкатегории)'
    category.short_description = 'Категория (согласно подкатегории)'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('type__name', 'name')


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    search_fields = ('category__name', 'category__type__name', 'name')


class StatusTypeAdmin(admin.ModelAdmin):
    search_fields = ('name',)


admin.site.register((Status, Type), StatusTypeAdmin)
admin.site.unregister((Group, User))
