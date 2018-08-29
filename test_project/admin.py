from django.contrib import admin
from .models import User, Group, Post, PostFiles, ChatRoom, Roles, Replay
# Register your models here.



class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'email_verified', 'role', 'approved')
    exclude = ['password']

admin.site.register(User, UserAdmin)
admin.site.register(Group)
admin.site.register(Post)
admin.site.register(PostFiles)
admin.site.register(ChatRoom)
admin.site.register(Roles)
admin.site.register(Replay)