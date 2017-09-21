# Menú y breadcrumbs

## **show_menu**

El tag show_menu muestra la navegación de la página actual. Se pude adaptar el HTML si agrega una plantilla menu/menu. html a su proyecto o edita la que se proporciona con django CMS.

show_menu toma seis parámetros opcionales:

* **start_level** (default=0): Desde qué nivel se debe mostrar la navegación.  Si tenemos la home como nodo raíz (Nivel 0) y no queremos mostrarlo, configuraremos start_level a 1.

* **end_level** (default=100): En qué nivel debe detenerse la navegación

* **extra_inactive** (default=0): Especifica cuántos niveles de navegación deben mostrarse si un nodo no es un antepasado directo o descendiente del nodo activo actual.

* **extra_active** (default=100): Especifica cuántos niveles de descendientes del nodo activo actual deben visualizarse.

* namespace: Especifica el espacio de nombres del menú. Si está vacío usará todos los espacios de nombres.

* root_id: Especifica el id del nodo raíz.

* **template**: Podemos proporcionar un parámetro de plantilla para que la sustituya.

### Ejemplos:

- Navegación completa (como lista anidada):

~~~
{% load menu_tags %}
<ul>
    {% show_menu 0 100 100 100 %}
</ul>
~~~

- Navegación con árbol activo (como lista anidada):

~~~
<ul>
    {% show_menu 0 100 0 100 %}
</ul>
~~~

- Navegación con un sólo nivel extra activo:

~~~
<ul>
    {% show_menu 0 100 0 1 %}
</ul>
~~~

- Navegación de nivel 1 (como lista anidada):
~~~
<ul>
    {% show_menu 1 %}
</ul>
~~~

- Navegación con una plantilla personalizada:
~~~
{% show_menu 0 100 100 100 "myapp/menu.html" %}
~~~

Utilizaremos un sólo nivel de navegación para nuestro menú, así que añadimos `{% show_menu 0 100 0 0 %}` a nuestro `base.html`

## **show_breadcrumb**

Muestra la miga de pan de la página actual. Podemos personalizar este html como queramos pasándole el html en el template tag.

Nosotros mostraremos la miga de pan obviando el nodo raíz (la home, el 0), nos quedaría de la siguiente manera:

`{% show_breadcrumb 1 "inc/breadcrumbs_inc.html" %}`


## **Cambios en plantilla base.html**

Para crear el **menú** vamos a sacarlo a una template `menu.html`.

* Primero creamos un directorio **inc** dentro del directorio **templates** de nuestro proyecto
* Seguidamente creamos un `menu.html` con el siguiente contenido (vamos a ir adaptando el código del tema SOLID basado en bootstrap que hemos elegido el código de django-cms ):

~~~
{% load menu_tags %}

<!-- Fixed navbar -->
<div class="navbar navbar-default navbar-fixed-top" role="navigation">
  <div class="container">
    <div class="navbar-header">
      <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="/">PyConES 2017</a>
    </div>
    <div class="navbar-collapse collapse navbar-right">
      <ul class="nav navbar-nav">
          {% show_menu 0 100 0 0 "inc/menu_inc.html" %}
      </ul>
    </div><!--/.nav-collapse -->
  </div>
</div>
~~~

* Posteriormente creamos un `menu_inc.html` al que hacemos referencia en el anterior `menu.html` creado que será la template con el que irá renderizado los puntos de menú:

~~~
{% load menu_tags %}

{% for child in children %}
<li class="child{% if child.children %} dropdown{% endif %}{% if child.selected %} selected{% endif %}{% if child.ancestor %} ancestor{% endif %}{% if child.sibling %} sibling{% endif %}{% if child.descendant %} descendant{% endif %}">
	<a
    {% if child.children %}class="dropdown-toggle" data-toggle="dropdown"{% endif %}
    href="{{ child.attr.redirect_url|default:child.get_absolute_url }}">
    {{ child.get_menu_title }}
    {% if child.children %} <b class="caret"></b>{% endif %}
  </a>
	{% if child.children %}
	<ul class="dropdown-menu">
		{% show_menu from_level to_level extra_inactive extra_active template "" "" child %}
	</ul>
	{% endif %}
</li>
{% endfor %}
~~~

* Ahora ya tenemos nuestras plantillas de menú preparadas para sustituir en el bloque del `base.html`así que vamos a cambiar el menú que traía la plantilla por defecto por el nuestro:

~~~
<ul class="nav">
    {% show_menu 0 100 100 100 %}
</ul>
~~~

con el siguiente bloque:

~~~
{% include "inc/menu.html" %}
~~~


Para crear el **breadcrumbs** vamos a seguir la misma dinámica que con el menú.

* Creamos un fichero `breadcrumbs.html` con el siguiente contenido dentro del directorio **inc**

~~~
{% load menu_tags %}

<div id="blue">
    <div class="container">
    <div class="row">
      {% show_breadcrumb 1 "inc/breadcrumbs_inc.html" %}
    </div><!-- /row -->
    </div> <!-- /container -->
</div><!-- /blue -->
~~~

* Creamos otro fichero dentro del directorio **inc** llamado `breadcrumbs_inc.html` con el siguiente contenido:

~~~
{% for ance in ancestors %}
	{% if not forloop.last %}
	<a href="{{ ance.get_absolute_url }}"><h3 style="display: inline">{{ ance.get_menu_title }} &raquo; </h3></a> <span class="separator"></span>
	{% else %}
	<span class="active"><h3 style="display: inline">{{ ance.get_menu_title }}</h3></span>
	{% endif %}
{% endfor %}
~~~

* Por último vamos a crear una nueva plantilla dentro del directorio **templates** llamada `sobre_nosotros.html` que será la plantilla de la siguiente página en la que vamos a trabajar los plugins, esta página deberá incluir el breadcrumbs:

~~~
{% extends "base.html" %}
{% load cms_tags %}

{% block title %}{% page_attribute "page_title" %}{% endblock title %}

{% block content %}
	{% include "inc/breadcrumbs.html" %}
	{% placeholder "content" %}
{% endblock content %}
~~~

También tendremos que añadirla al `CMS_TEMPLATES` del `settings.py`:

~~~
CMS_TEMPLATES = (
    ('fullwidth.html', 'Fullwidth'),
    ('sidebar_left.html', 'Sidebar Left'),
    ('sidebar_right.html', 'Sidebar Right')
    ('home.html', 'Home'),
    ('sobre_nosotros.html', 'Sobre nosotros'),
)
~~~

## DEMO

Vamos a crear la página **sobre_nosotros** replicando la del tema SOLID.
