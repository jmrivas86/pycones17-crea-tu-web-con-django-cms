# Caché en django CMS

Para configurar la caché en django CMS primero tendremos que configurar un backend de caché para django.

Más detalles sobre caché en django [aquí](https://docs.djangoproject.com/en/dev/topics/cache/):

## Configuración del middleware:

* `django.middleware.cache.UpdateCacheMiddleware` en primer lugar

* `django.middleware.cache.FetchFromCacheMiddleware` en la última posición

quedando una cosa así:

```
MIDDLEWARE_CLASSES=[
    'django.middleware.cache.UpdateCacheMiddleware',
    ...
    'cms.middleware.language.LanguageCookieMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
],
```

## Plugins

Normalmente, todos los plugins serán almacenados en caché. Si tiene un plugin dinámico basado en el usuario actual u otras propiedades dinámicas de la petición, establezca el atributo `cache=False` en la clase plugin:

```
class MyPlugin(CMSPluginBase):
    name = _("MyPlugin")
    cache = False
```

> **Nota:** Si deshabilita una caché de plugin asegúrese de reiniciar el servidor y luego desactive la caché.

## Duración de la caché

Por defecto es 60 segundos pero puede ser cambiado estableciendo el valor que queramos en la settings `CMS_CACHE_DURATIONS`

## Settings

El almacenamiento en caché se establece por defecto como true. Existen varias settings para habilitar/deshabilitar varios comportamientos de caché:

### CMS_CACHE_DURATIONS

Este diccionario contiene las distintas configuraciones de duración de caché.

`'content'`: 60 segundos por defecto para `show_placeholder`, `page_url`, `placeholder` and `static_placeholder` template tags.

`'menus'`: 3600 segundos por defecto.

### CMS_CACHE_PREFIX

`cms-` por defecto.

El CMS pondrá el valor asociado a esta clave para cada acceso a la caché (set y get). Esto es útil cuando tiene varias instalaciones de django CMS, y no quiere que compartan objetos de caché.

`CMS_CACHE_PREFIX = 'mysite-live'`

### CMS_PAGE_CACHE

`True` por defecto

Las páginas no son almacenadas en caché para los usuarios logados. Si el toolbar es visible, la página no está cacheada.

### CMS_PLACEHOLDER_CACHE

`True` por defecto

### CMS_PLUGIN_CACHE

`True` por defecto
