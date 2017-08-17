from django.contrib import admin

from .models import Post

# Register your models here.

# This class will tweek how the Post will be displayed in the admin site
# when in a list of all the Posts or when adding/editing a new one
class PostAdmin(admin.ModelAdmin):
    # the default is a to show just the Post.__str__() value
    # but we can change it with
    list_display = ('title', 'slug', 'status')

    # this will add a search bar that will search in the specified fields
    search_fields = ('title', 'body')

    # this will populate the slug field when addding new post with
    # the same value as in the title field
    prepopulated_fields = {'slug': ('title',)}

    ordering = ('status', 'published', 'slug')


admin.site.register(Post, PostAdmin)
