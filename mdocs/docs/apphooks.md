# Apphooks: Integración de aplicaciones Django en Django-CMS

La integración de otras aplicaciones en django CMS, que es de donde proviene una gran parte de su poder.

Integrar aplicaciones no sólo significa instalarlas junto a django CMS, para que coexistan pacíficamente. Significa utilizar las características de django CMS para construir un único proyecto web coherente que acelere el trabajo de gestión del sitio y haga posible una publicación más automatizada y enriquecida.

Es clave para que la integración de django CMS funcione, no requiere que modifiquemos otras aplicaciones a menos que lo deseemos. Esto es particularmente importante cuando estamos utilizando aplicaciones de terceros y no queremos tener que mantener nuestras propios forks. (La única excepción a esto es si decidimos construir características de django CMS directamente en las propias aplicaciones, por ejemplo cuando se utiliza marcadores de posición en otras aplicaciones).

Veamos el [ejemplo](http://docs.django-cms.org/en/release-3.4.x/introduction/integrating_applications.html
). de la documentación oficial de django CMS:



# Integración de third-party application

Ya sabemos crear nuestros propios plugins y aplicaciones CMS django, pero otro punto importante es extender nuestro CMS con una aplicación de terceros. Para ello vamos a integrar la aplicación **Aldryn News & Blog**.

* Instalamos la dependencia con pip

`pip install aldryn-newsblog`

* Añadimos a `INSTALLED_APPS` en el fichero `settings.py` debería quedar algo así:

```
INSTALLED_APPS = (
    'djangocms_admin_style',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'cms',
    'menus',
    'sekizai',
    'treebeard',
    'djangocms_text_ckeditor',
    'filer',
    'easy_thumbnails',
    'djangocms_column',
    'djangocms_link',
    'cmsplugin_filer_file',
    'cmsplugin_filer_folder',
    'cmsplugin_filer_image',
    'cmsplugin_filer_utils',
    'djangocms_style',
    'djangocms_snippet',
    'djangocms_googlemap',
    'djangocms_video',
    'mi_web',
    'my_web_cms',
    'aldryn_apphooks_config',
    'aldryn_categories',
    'aldryn_common',
    'aldryn_newsblog',
    'aldryn_people',
    'aldryn_reversion',
    'aldryn_translation_tools',
    'parler',
    'sortedm2m',
    'taggit',
    'reversion',
    'aldryn_boilerplates',
)
```

* Ahora hacemos la migración en base de datos:

`python manage.py migrate`

* El siguiente punto es crear una página con el hook a la aplicación:
    - Crear una página CMS django y la llamamos "Blog".
    - En Configuración avanzada... > Configuración de aplicaciones, seleccione NewsBlog.

Como podemos ver en la imagen inferior ahora en la página de blog tenemos un nuevo punto de menú en el toolbar.

![Apphook](images/blog.png)

Añadimos un par de artículos y podemos comprobar que ya está totalmente integrada nuestro blog pero... ¡Qué feo se ve!. Vamos a adaptar las plantillas con las del tema SOLID:

* Lo primero es descargarnos el directorio `aldryn_newsblog` que está dentro del directorio templates de la aplicación. Podemos hacerlo con un `cp` desde el entorno virtual o descargando del repositorio la app.

* Ahora ponemos ese directorio dentro del directorio templates de nuestro proyecto, deberíamos tener algo así:

![aldryn_newsblog](images/aldryn_blog.png)

Ahora vamos a sobreescribir las templates que necesitamos:

* **base.html**

```
{% extends CMS_TEMPLATE %}
{% load cms_tags %}

{% block content %}
  <div class="container mtb">
       <div class="row">
         <! -- BLOG POSTS LIST -->
         <div class="col-lg-8">
          {% block newsblog_content %}
              {# article_list.html and article_detail.html extend this template #}
          {% endblock %}
        </div><! --/col-lg-8 -->
        <! -- SIDEBAR -->
        <div class="col-lg-4">
          {% placeholder "sidebar" %}
        </div>
      </div><! --/row -->
     </div><! --/container -->
{% endblock content %}
```

* **article_detail.html**

```
{% extends "aldryn_newsblog/base.html" %}
{% load i18n cms_tags apphooks_config_tags %}

{% block title %}
    {{ article.title }} - {{ block.super }}
{% endblock %}

{% block newsblog_content %}
    {% include "aldryn_newsblog/includes/article.html" with detail_view="true" %}
    {% static_placeholder "newsblog_social" %}
{% endblock %}
```

* **includes/article.html**

```
{% load i18n staticfiles thumbnail cms_tags apphooks_config_tags %}

{% if article.featured_image_id %}
  <img class="img-responsive" src="{% thumbnail article.featured_image 800x450 crop subject_location=article.featured_image.subject_location %}" alt="{{ article.featured_image.alt }}">
{% endif %}

{% if detail_view %}
    <h3 class="ctitle">{% render_model article "title" %}</h3>
{% else %}
    <a href="{% namespace_url 'article-detail' article.slug namespace=namespace default='' %}"><h3 class="ctitle">{% render_model article "title" %}</h3></a>
{% endif %}

<p><csmall>Posted: {{ article.publishing_date|date }}</csmall> | <csmall2>By: {% include "aldryn_newsblog/includes/author.html" with author=article.author %}</csmall2></p>
{% render_model article "lead_in" %}

{% if detail_view %}
    {% render_placeholder article.content language placeholder_language %}
{% else %}
  <p><a href="{% namespace_url 'article-detail' article.slug namespace=namespace default='' %}">[Read More]</a></p>
  <div class="hline"></div>
  <div class="spacing"></div>
{% endif %}
```

* **includes/author.html**

```
{% load i18n staticfiles thumbnail apphooks_config_tags %}

{% if author %}
        <a href="{% namespace_url "article-list-by-author" author.slug namespace=namespace default='' %}">
            {% if author.visual %}
                {% thumbnail author.visual "50x50" crop upscale subject_location=author.visual.subject_location as author_image %}
                <img src="{{ author_image.url }}" width="50" height="50" alt="{{ author.name }}">
            {% endif %}
            {{ author.name }}
        </a>
    {% if author.function %}<p>{{ author.function }}</p>{% endif %}
    {% if author.article_count %}<p>{{ author.article_count }}</p>{% endif %}
{% endif %}
```

* **plugins/tags.html**

```
{% load i18n apphooks_config_tags %}

<h4>Popular Tags</h4>
<div class="hline"></div>
<p>
  {% for tag in tags %}
    <a class="btn btn-theme" href="{% namespace_url "article-list-by-tag" tag.slug namespace=instance.app_config.namespace default='' %}" role="button">{{ tag.name }}</a>
  {% endfor %}
</p>

```

* **plugins/latest_articles.html**

```
{% load i18n staticfiles thumbnail cms_tags apphooks_config_tags %}


<h4>Recent Posts</h4>
<div class="hline"></div>
  <ul class="popular-posts">

{% for article in article_list %}
    <li>
      {% if article.featured_image_id %}
        <a href="{% namespace_url 'article-detail' article.slug namespace=namespace default='' %}">
          <img class="img-responsive" src="{% thumbnail article.featured_image 70x70 crop subject_location=article.featured_image.subject_location %}"
          alt="{{ article.featured_image.alt }}">
        </a>
      {% endif %}
        <h4><a href="{% namespace_url 'article-detail' article.slug namespace=namespace default='' %}">{{ article.title }}</a></h4>
        <em>Posted: {{ article.publishing_date|date }}</em>
    </li>
{% empty %}
    <p>{% trans "No items available" %}</p>
{% endfor %}

<div class="spacing"></div>
```

* **plugins/categories.html**

```
{% load i18n apphooks_config_tags %}


<h4>Categories</h4>
<div class="hline"></div>
{% for category in categories %}
    <p {% if newsblog_category.id == category.id %} class="active"{% endif %}>
      <a href="{% namespace_url "article-list-by-category" category.slug namespace=instance.app_config.namespace default='' %}">
        <i class="fa fa-angle-right"></i>
        {{ category.name }}
      </a>
      <span class="badge badge-theme pull-right">{{ category.article_count }}</span>
    </p>
{% endfor %}
<div class="spacing"></div>
```
