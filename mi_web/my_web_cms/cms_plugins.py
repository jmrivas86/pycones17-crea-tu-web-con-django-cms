from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from .models import EmpleadosPluginModel, Empleado


class EmpleadoInlineAdmin(admin.StackedInline):
    model = Empleado


class EmpleadosPlugin(CMSPluginBase):
    model = EmpleadosPluginModel
    name = _("Empleados Plugin")
    render_template = "plugins/empleados_plugin.html"
    inlines = (EmpleadoInlineAdmin, )
    cache = False

    def render(self, context, instance, placeholder):
        context = super(EmpleadosPlugin, self).render(context, instance, placeholder)
        empleados = instance.empleado_item.all()
        context.update({
            'empleados': empleados
        })
        return context

plugin_pool.register_plugin(EmpleadosPlugin)
