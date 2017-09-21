# Crea tu web con django CMS

For full documentation visit [mkdocs.org](http://mkdocs.org).

## Índice
* Instalación con djangocms-installer
* Páginas:
    * Estructura y contenido
    * Borrador & público
    * Internacionalización
* Permisos
* Templates & Placeholders
* Menús
* Plugins
* Third party aplications & Apphooks: Integración de aplicaciones Django en Django-CMS
* Páginas tipo para facilitar a los editores de contenido la creación de páginas a partir de tipos predefinidos.
* Extender el modelo de Página:
    * Page (campos con los mismos valores en todos los idiomas)
    * Title (campos con valores distintos por idioma)
* Extender el Toolbar
* Extender el menú de navegación
* Cache en Django-CMS

# Enlace a la documentación

[https://jmrivas86.github.io/pycones17-crea-tu-web-con-django-cms](https://jmrivas86.github.io/pycones17-crea-tu-web-con-django-cms).

# Enlace al proyecto finalizado

[https://github.com/jmrivas86/pycones17-crea-tu-web-con-django-cms-code](https://github.com/jmrivas86/pycones17-crea-tu-web-con-django-cms-code).

Para ejecutarlo simplemente clone el proyecto o descargue el zip y siga los siguientes pasos:

`git clone https://github.com/jmrivas86/pycones17-crea-tu-web-con-django-cms.git`

`virtualenv env`

`source env/bin/activate`

`python manage.py runserver`

# Instalando django CMS

Primero crearemos nuestro entorno virtual con virtualenv:

`mkvirtualenv -p /usr/local/bin/python3 pycones2017`

`virtualenv env`

`source env/bin/activate`

## Requisitos
django CMS necesita Django 1.8, 1.9 or 1.10 y Python 2.7, 3.3, 3.4, 3.5 o 3.6

## El entorno de trabajo
Instalaremos un entorno virtual con *virtualenv* donde instalaremos todas nuestras dependencias.


## Creamos y activamos nuestro entorno virtual
`virtualenv env`

`source env/bin/activate`

Si estás usando Windows para activar el virtualenv necesitarás:

`env\Scripts\activate`

Seguidamente actualizamos pip

`pip install --upgrade pip`

Usamos django CMS installer para crear nuestro proyecto. Django CMS installer es un script que se encarga de configurar un nuevo proyecto de django CMS

`pip install djangocms-installer`

Esto nos proporcionará un nuevo comando con el que arrancaremos nuestro proyecto, [**djangocms**](https://djangocms-installer.readthedocs.io/en/latest/)

`djangocms -f mi_web`

Ahora ya podemos arrancar nuestro servidor de desarrollo:

`python manage.py runserver`

Para entrar en el CMS accedemos a [localhost:8000?edit](http://localhost:8000/es/?edit) y entramos con las credenciales que el script nos ha creado automaticamente:

* usuario: admin
* contraseña: admin

Por último vamos a añadir algunas configuraciones al `settings.py` del proyecto que nos hará en los siguientes pasos:

~~~
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters'
)

DJANGOCMS_STYLE_CHOICES = ['container', 'content', 'teaser', 'row']
DJANGOCMS_STYLE_TAGS = ['div', 'article', 'section', 'header', 'footer',
                        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'i']
~~~
