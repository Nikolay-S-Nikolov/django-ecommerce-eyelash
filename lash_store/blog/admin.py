from django.contrib import admin

from lash_store.blog.models import BlogImage, BlogPost


class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1
    show_change_link = True

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    # fields = ['title', 'excerpt', 'content', 'slug', 'published']
    list_display = ('title', 'slug', 'author','created_at','published','short_excerpt')
    list_filter = ('author', 'published', 'created_at')
    list_display_links = ('title', 'slug')
    search_fields = ('title', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('author',)
    date_hierarchy = 'created_at'
    inlines = [BlogImageInline]

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'published')
        }),
        ('Съдържание', {
            'fields': ('excerpt', 'content')
        }),
    )

    def short_excerpt(self, obj):
        return (obj.excerpt[:50] + "...") if obj.excerpt else ""

    short_excerpt.short_description = "Откъс"

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)
