# Extender el menú de navegación

 Hay tres maneras diferentes de personalizar los menús de navegación de en django CMS.

## **Menús:**

Ampliar de manera estática las entradas de menú. Éste es el que vamos a llevar a cabo en nuestra página web de ejemplo. Vamos a añadir un nuevo punto a una web externa en nuestro menú.

* Primero creamos un fichero `menu.py` en nuestra app __my_web_cms__ que contendrá lo siguiente:

```
from menus.base import Menu, NavigationNode
from menus.menu_pool import menu_pool
from django.utils.translation import ugettext_lazy as _


class ExtendMenu(Menu):

    def get_nodes(self, request):
        nodes = []
        n = NavigationNode(_('PyConES 2017'), "https://2017.es.pycon.org", 1)
        nodes.append(n)
        return nodes


menu_pool.register_menu(ExtendMenu)
```
* Si actualizamos la página, ahora deberíamos ver la nueva entradas del menú.

La función `get_nodes` devuelve una lista de instancias de `NavigationNode`. `menus.base.NavigationNode` tiene siguientes argumentos:

1. `title`: Texto para el nodo de menú

2. `url` : URL para el nodo de menú

3. `id`: ID único apra el nodo de menú

4. `parent_id=None`: Si éste es un hijo de otro nodo, hay que pasarle aquí el identificador del padre.

5. `parent_namespace=None`: Si el nodo padre no está en este menú, puede darle el namespace padre. El espacio de nombres es el nombre de la clase. En el ejemplo anterior, que sería: ExtendMenu

6. `attr=None`: Un diccionario de atributos adicionales que puede utilizar en un modificador o en la plantilla

7. `visible=True`: Si este punto de menú debe ser visible o no


## **Adjuntar menús:**

Adjuntar su menú a una página.

Sirve para adaptar un menú según las condiciones de la solicitud (por ejemplo, usuarios anónimos/registrados), puede utilizar los Modificadores de Navegación o puede hacer uso de los ya existentes.

Por ejemplo, es posible añadir {'visible_for_anonymous': False}/{'visible_for_authenticated': False} atributos reconocidos por el modificador AuthVisibility de django CMS core.

[documentación oficial](http://docs.django-cms.org/en/release-3.4.x/how_to/menus.html#integration-attach-menus
).

## **Modificadores de Navegación:**

Modificar todo el árbol de menú

[documentación oficial](http://docs.django-cms.org/en/release-3.4.x/how_to/menus.html#navigation-modifiers
).
