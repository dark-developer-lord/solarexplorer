from django.contrib import admin

# Register your models here.
from .models import CustomUser, ForumCategory, ForumThread, ForumPost, NewsArticle, TeamMember

admin.site.register(CustomUser)
admin.site.register(ForumCategory)
admin.site.register(ForumThread)
admin.site.register(ForumPost)
admin.site.register(NewsArticle)
admin.site.register(TeamMember)