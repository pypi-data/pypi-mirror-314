#!/usr/bin/env python3

"""Used to configure the main menu."""


def fill_menu(menu, actions):
    """Add fields to the empty menu."""
    file_menu = menu.addMenu("File")
    file_menu.addAction(actions["open"])
    file_menu.addAction(actions["save"])
    file_menu.addAction(actions["save_as"])
    file_menu.addSeparator()
    file_menu.addAction(actions["import"])
    file_menu.addAction(actions["export"])

    edit_menu = menu.addMenu("Edit")
    edit_menu.addAction(actions["refresh"])
    edit_menu.addAction(actions["undo"])
    edit_menu.addAction(actions["redo"])
    edit_menu.addSeparator()
    edit_menu.addAction(actions["preferences"])
