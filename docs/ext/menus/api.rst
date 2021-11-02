API Reference
=============

.. _ext_menus_api:

.. currentmodule:: nextcord.ext.menus

.. contents::

Reaction Menus
--------------

Menu
~~~~

.. attributetable:: Menu

.. autoclass:: Menu
    :members:
    :exclude-members: should_add_reactions, should_add_buttons

Button decorator
~~~~~~~~~~~~~~~~

.. autofunction:: button

Reordering Reactions
~~~~~~~~~~~~~~~~~~~~

Position
>>>>>>>>

.. autoclass:: Position
    :members:

First
>>>>>

.. autoclass:: First
    :members:

Last
>>>>

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

ButtonMenu
~~~~~~~~~~

.. attributetable:: ButtonMenu

.. autoclass:: ButtonMenu
    :members:
    :inherited-members:
    :exclude-members: add_button, buttons, clear_buttons, on_menu_button_error, reaction_check, remove_button, should_add_reactions, should_add_buttons, update, from_message

Button decorator
~~~~~~~~~~~~~~~~

.. autofunction:: nextcord.ui.button

Pagination
~~~~~~~~~~

ButtonMenuPages
>>>>>>>>>>>>>>>

.. attributetable:: ButtonMenuPages

.. autoclass:: ButtonMenuPages
    :members:
    :inherited-members:
    :exclude-members: add_button, buttons, clear_buttons, on_menu_button_error, reaction_check, remove_button, should_add_reactions, should_add_buttons, update, from_message


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

Exceptions
----------

.. autoclass:: MenuError
    :members:

.. autoclass:: CannotEmbedLinks
    :members:

.. autoclass:: CannotSendMessages
    :members:

.. autoclass:: CannotAddReactions
    :members:

.. autoclass:: CannotReadMessageHistory
    :members: