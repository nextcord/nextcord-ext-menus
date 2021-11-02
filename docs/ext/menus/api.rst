API Reference
=============

.. _ext_menus_api:

.. currentmodule:: nextcord.ext.menus

.. contents::

Reaction Menus
--------------

Menus
~~~~~

.. attributetable:: Menu

.. autoclass:: Menu
    :members:
    :exclude-members: should_add_reactions, should_add_buttons

.. autofunction:: button

Reordering Reactions
~~~~~~~~~~~~~~~~~~~~

.. autoclass:: Position
    :members:

.. autoclass:: First
    :members:

.. autoclass:: Last
    :members:

Pagination
~~~~~~~~~~

MenuPages
>>>>>>>>>

.. attributetable:: MenuPages

.. autoclass:: MenuPages
    :members:

Button
>>>>>>

.. attributetable:: Button

.. autoclass:: Button
    :members:

Button Menus
------------

Menus
~~~~~

.. attributetable:: ButtonMenu

.. autoclass:: ButtonMenu
    :members:
    :inherited-members:
    :exclude-members: add_button, buttons, clear_buttons, on_menu_button_error, reaction_check, remove_button, should_add_reactions, should_add_buttons, update

.. autofunction:: nextcord.ui.button

Pagination
~~~~~~~~~~

ButtonMenuPages
>>>>>>>>>>>>>>>

.. attributetable:: ButtonMenuPages

.. autoclass:: ButtonMenuPages
    :members:
    :inherited-members:

MenuPaginationButton
>>>>>>>>>>>>>>>>>>>>

.. attributetable:: MenuPaginationButton

.. autoclass:: MenuPaginationButton
    :members:
    :inherited-members:

Page Sources
------------

PageSource (Basic Interface)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. attributetable:: PageSource

.. autoclass:: PageSource
    :members:

ListPageSource
~~~~~~~~~~~~~~

.. attributetable:: ListPageSource

.. autoclass:: ListPageSource
    :members:
    :inherited-members:

GroupByPageSource
~~~~~~~~~~~~~~~~~

.. attributetable:: GroupByPageSource

.. autoclass:: GroupByPageSource
    :members:
    :inherited-members:

AsyncIteratorPageSource
~~~~~~~~~~~~~~~~~~~~~~~

.. attributetable:: AsyncIteratorPageSource

.. autoclass:: AsyncIteratorPageSource
    :members:
    :inherited-members: