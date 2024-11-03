from django.contrib import admin
from .models import *
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin


# admin.sites.AdminSite.site_header = 'پنل مدیریت جنگو'
# admin.sites.AdminSite.site_title ='پنل'
# admin.sites.AdminSite.index_title = 'پنل مدیریت'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publish', 'status']
    list_filter = ['status', ('publish', JDateFieldListFilter), 'author']
    ordering = ['title', 'publish']
    search_fields = ['title',]
    raw_id_fields = ['author']
    list_editable = ['status']
    date_hierarchy = 'publish'
    prepopulated_fields = {'slug': ['title']}
    list_display_links = ['author']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['name', 'message', 'subject']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'name', 'created', 'active']
    list_filter = ['active', ('created', JDateFieldListFilter), ('modified', JDateFieldListFilter)]
    search_fields = ['name', 'text']
    list_editable = ['active']
    date_hierarchy = 'created'

