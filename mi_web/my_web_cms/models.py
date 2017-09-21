from django.db import models
from filer.fields.image import FilerImageField
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from cms.extensions import PageExtension
from cms.extensions.extension_pool import extension_pool


class EmpleadosPluginModel(CMSPlugin):
    titulo = models.CharField(max_length=50)

    def copy_relations(self, oldinstance):
        # Before copying related objects from the old instance, the ones
        # on the current one need to be deleted. Otherwise, duplicates may
        # appear on the public version of the page
        self.empleado_item.all().delete()

        for empleado_item in oldinstance.empleado_item.all():
            # instance.pk = None; instance.pk.save() is the slightly odd but
            # standard Django way of copying a saved model instance
            empleado_item.pk = None
            empleado_item.plugin = self
            empleado_item.save()

    def __str__(self):
        return self.titulo


class Empleado(models.Model):
    nombre = models.CharField(
        max_length=250,
        verbose_name=_("Nombre"),
        null=False, blank=False
    )
    apellidos = models.CharField(
        max_length=250,
        verbose_name=_("Apellidos"),
        null=False, blank=False
    )
    cargo = models.CharField(
        max_length=250,
        verbose_name=_("Cargo"),
        null=False, blank=False
    )
    descripcion = models.CharField(
        max_length=250,
        verbose_name=_("Descripción"),
        null=False, blank=False
    )
    twitter = models.URLField(
        verbose_name=_("Usuario de twitter"),
        null=False, blank=True
    )
    email = models.EmailField(
        verbose_name=_("Correo electrónico"),
        null=False, blank=True
    )
    foto = FilerImageField(verbose_name="Foto", null=False, blank=False)
    plugin = models.ForeignKey(
        EmpleadosPluginModel,
        related_name="empleado_item"
    )

    @property
    def nombre_completo(self):
        full_name = "{nombre} {apellidos}".format(nombre=self.nombre, apellidos=self.apellidos)
        return full_name.strip()

    def __str__(self):
        return self.nombre_completo


class IconExtension(PageExtension):
    image = models.ImageField(upload_to='icons')


extension_pool.register(IconExtension)
