from django.contrib import admin
from blogpost.models import Post,Comment,User



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
   list_display = ('title', 'blog', 'pub_date', 'author')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
   list_display = ('username', 'comment', 'comment_date')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
   list_display = ('first_name', 'last_name', 'country', 'birth_date')

