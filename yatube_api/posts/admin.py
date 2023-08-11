from django.contrib import admin

from .models import Comment, Group, Post, Follow


class CommentInline(admin.TabularInline):
    model = Comment
    fk_name = "post"


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'group')
    search_fields = ('text',)
    list_filter = ('pub_date', 'group')
    ordering = ('-pub_date',)
    empty_value_display = '-пусто-'
    inlines = [
        CommentInline,
    ]


class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'description',)
    search_fields = ('slug',)
    list_filter = ('title',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'post', 'text', 'created',)
    search_fields = ('author',)
    list_filter = ('post',)
    ordering = ('-created',)
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'following',)


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
