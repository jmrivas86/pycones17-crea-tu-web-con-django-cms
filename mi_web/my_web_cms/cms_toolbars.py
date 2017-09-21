from cms.toolbar_pool import toolbar_pool
from cms.extensions.toolbar import ExtensionToolbar
from django.utils.translation import ugettext_lazy as _
from .models import IconExtension
from cms.toolbar_base import CMSToolbar
from django.core.urlresolvers import reverse
from cms.toolbar.items import Break, SubMenu
from cms.cms_toolbars import ADMIN_MENU_IDENTIFIER, ADMINISTRATION_BREAK


@toolbar_pool.register
class IconExtensionToolbar(ExtensionToolbar):
    # defines the model for the current toolbar
    model = IconExtension

    def populate(self):
        # setup the extension toolbar with permissions and sanity checks
        current_page_menu = self._setup_extension_toolbar()

        # if it's all ok
        if current_page_menu:
            # retrieves the instance of the current extension (if any) and the toolbar item URL
            page_extension, url = self.get_page_extension_admin()
            if url:
                # adds a toolbar item in position 0 (at the top of the menu)
                current_page_menu.add_modal_item(
                    _('Icono de página'), url=url,
                    disabled=not self.toolbar.edit_mode, position=0
                )


@toolbar_pool.register
class TaggitToolbar(CMSToolbar):

    def populate(self):
        #
        # 'Apps' is the spot on the existing djang-cms toolbar admin_menu
        # 'where we'll insert all of our applications' menus.
        #
        admin_menu = self.toolbar.get_or_create_menu(
            ADMIN_MENU_IDENTIFIER, _('PyConES')
        )

        #
        # Let's check to see where we would insert an 'Offices' menu in the
        # admin_menu.
        #
        position = admin_menu.get_alphabetical_insert_position(
            _('Tags'),
            SubMenu
        )

        #
        # If zero was returned, then we know we're the first of our
        # applications' menus to be inserted into the admin_menu, so, here
        # we'll compute that we need to go after the first
        # ADMINISTRATION_BREAK and, we'll insert our own break after our
        # section.
        #
        if not position:
            # OK, use the ADMINISTRATION_BREAK location + 1
            position = admin_menu.find_first(
                Break,
                identifier=ADMINISTRATION_BREAK
            ) + 1
            # Insert our own menu-break, at this new position. We'll insert
            # all subsequent menus before this, so it will ultimately come
            # after all of our applications' menus.
            admin_menu.add_break('custom-break', position=position)

        # OK, create our taggit menu here.
        taggit_menu = admin_menu.get_or_create_menu(
            'taggit-menu',
            _('Tags ...'),
            position=position
        )

        # Let's add some sub-menus to our tag menu that help our users

        # Take the user to the admin-listing for tags...
        url = reverse('admin:taggit_tag_changelist')
        taggit_menu.add_sideframe_item(_('Tag List'), url=url)

        # Display a modal dialogue for creating a new tag...
        url = reverse('admin:taggit_tag_add')
        taggit_menu.add_modal_item(_('Add New Tag'), url=url)

        # Add a break in the sub-menus
        taggit_menu.add_break()
