# coding: utf-8
# vim: ai ts=4 sts=4 et sw=4
#from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.conf.urls.defaults import *
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import  render_to_response, get_object_or_404
import os
from django.conf import settings
from django.utils.encoding import force_unicode
from django.utils import simplejson
from django import template
from django.contrib.auth.decorators import permission_required

class TreeAdmin(admin.ModelAdmin):

    def __init__(self,*args,**kargs):
        super(TreeAdmin,self).__init__(*args,**kargs)
        if not hasattr(self,'tree_display'):
            self.tree_display = ()
        if self.tree_display and not hasattr(self,'tree_title_field'):
            self.tree_title_field = self.tree_display[0]
        if not hasattr(self,'tree_title_field'):
            title_field = ''
        else:
            title_field = '.'+self.tree_title_field
        extra_fields = '&nbsp;'.join('<span title="%s">{{ node.%s }}</span>' % (field,field) for field in self.tree_display if not hasattr(self,'tree_title_field') or field!=self.tree_title_field)
        model = '%s.%s' % (self.Meta.model._meta.app_label, self.Meta.model._meta.object_name)
        self._node_tpl = template.Template("""{% for node in nodes %}<li class="{% if not node.is_leaf_node %} jstree-closed{% endif %}{% if not node.visible %} HiddenNode{% endif %}" id="n{{node.pk}}"><ins>&nbsp;</ins><a href="{{node.pk}}/">{{ node"""+title_field+""" }}</a>"""+extra_fields+"""</li>{% endfor %}""")

    def changelist_view(self, request, extra_context=None):
        model = '%s.%s' % (self.Meta.model._meta.app_label, self.Meta.model._meta.object_name)
        opts = self.model._meta
        app_label = opts.app_label

        media = self.media

        module_name = force_unicode(opts.verbose_name_plural)

        permissions = simplejson.dumps({
            'renameable' : self.has_change_permission(request, None) and hasattr(self,'tree_title_field'),\
            'deletable'	: self.has_delete_permission(request, None),
            'creatable'	: self.has_add_permission(request),
            'draggable'	: self.has_change_permission(request, None),
        })
        root = self._node_tpl.render(template.Context({
            'nodes':self.Meta.model.tree.root_nodes()
        }))

        context = {
            'module_name': module_name,
            'title': module_name,
            'is_popup': False,
            'cl': {'opts':{'verbose_name_plural': module_name}},
            'media': media,
            'has_add_permission': self.has_add_permission(request),
            'root_path': self.admin_site.root_path,
            'app_label': app_label,
            'tree': root,
            'permissions': permissions,
            'parent_attr': self.Meta.model._meta.parent_attr,
        }
        context.update(extra_context or {})
        context_instance = template.RequestContext(request, current_app=self.admin_site.name)
        context_instance.update(context)
        return render_to_response('tree_list.html', context,
                                  context_instance=context_instance)

    def get_urls(self):
        urls = super(TreeAdmin, self).get_urls()

        my_urls = patterns('',
            (r'^tree/$', self.get_tree),
            (r'^move_node/$', self.move_node),
            (r'^rename_node/$', self.rename_node),
            (r'^add_node/$', self.add_node),
            (r'^remove_node/$', self.remove_node),
            (r'^hide/$', self.hide_node),
            (r'^show/$', self.show_node),
            (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': os.path.join(os.path.dirname(__file__),'media'), 'show_indexes': True}),
        )
        return my_urls + urls

    def get_tree(self,request):
        if 'id' in request.POST:
            if int(request.POST['id']):
                node = get_object_or_404(self.Meta.model,pk=request.POST['id'])
                nodes = node.get_children()
            else:
                nodes = self.Meta.model.tree.root_nodes()
            c = template.Context({'nodes':nodes})
            return HttpResponse(self._node_tpl.render(c))
        HttpResponse('')

    def move_node(self,request):
        if not self.has_change_permission(request, None):
            raise PermissionDenied
        node = get_object_or_404(self.Meta.model,pk=request.POST.get('node'))
        target = get_object_or_404(self.Meta.model,pk=request.POST.get('target'))
        position = request.POST.get('position')
        if position not in ('left','right','last-child','first-child'):
            return HttpResponseBadRequest('bad position')
        self.Meta.model.tree.move_node(node,target,position)
        return HttpResponse('')

    def add_node(self,request):
        if not self.has_add_permission(request):
            raise PermissionDenied
        try:
            parent = self.Meta.model.allpages.get(pk=request.POST.get('parent'))
        except:
            parent = None
        node = self.Meta.model(name=request.POST.get('name'), parent=parent)
        node.save()
        return HttpResponse(simplejson.dumps({'id': node.id }))
    
    def rename_node(self,request):
        if not self.has_change_permission(request, None):
            raise PermissionDenied
        node = get_object_or_404(self.Meta.model,pk=request.POST.get('node'))
        setattr(node,self.tree_title_field, request.POST.get('name'))
        node.save()
        return HttpResponse(simplejson.dumps({'id': node.id }))
    
    def hide_node(self,request):
        if not self.has_change_permission(request, None):
            raise PermissionDenied
        node = get_object_or_404(self.Meta.model,pk=request.POST.get('node'))
        node.visible = False
        node.save()
        return HttpResponse('')
    
    def show_node(self,request):
        if not self.has_change_permission(request, None):
            raise PermissionDenied
        node = get_object_or_404(self.Meta.model,pk=request.POST.get('node'))
        node.visible = True
        node.save()
        return HttpResponse('')

    def remove_node(self,request):
        if not self.has_delete_permission(request, None):
            raise PermissionDenied
        node = get_object_or_404(self.Meta.model,pk=request.POST.get('node'))
        node.delete()
        return HttpResponse('')


