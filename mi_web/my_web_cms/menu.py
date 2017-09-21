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
