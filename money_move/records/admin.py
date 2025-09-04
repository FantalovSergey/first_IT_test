from django.contrib import admin

from .models import Category, Record, Status, Subcategory, Type


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_filter = ('created_at', 'status', 'type', 'category', 'subcategory')
    readonly_fields = ('type', 'category')
    date_hierarchy = 'created_at'
    autocomplete_fields = ('subcategory',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'status', 'subcategory__category__type'
        )

    def category(self, obj):
        return obj.subcategory.category

    def type(self, obj):
        return obj.subcategory.category.type


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('type__name', 'name')


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    search_fields = ('category__name', 'category__type__name', 'name')


class StatusTypeAdmin(admin.ModelAdmin):
    search_fields = ('name',)


admin.site.register((Status, Type), StatusTypeAdmin)
