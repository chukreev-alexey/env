# -*- coding: utf-8 -*-

from django.contrib import admin

from pages.models import Page, InfoBlock
from treeadmin import TreeAdmin

class PageAdmin(TreeAdmin):
    fieldsets = [
        (None, {
            'fields': ['name', 'url', 'parent', 'redirect_to', 'visible'], 'classes': ['wide']
        }),
        (u'Содержимое страницы', {
            'fields': ['content'], 'classes': ['collapse']
        }),
        (u'SEO', {
            'fields': ['title', 'meta'], 'classes': ['collapse']
        }),
    ]
    tree_title_field = 'name'
    tree_display = ('name', 'path',)

    class Meta:
        model = Page
admin.site.register(Page, PageAdmin)

class InfoBlockAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('title', 'name')
    search_fields = ('title', 'name')
    prepopulated_fields = {'name': ('title',)}
admin.site.register(InfoBlock, InfoBlockAdmin)