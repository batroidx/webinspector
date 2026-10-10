import ttkbootstrap as ttk


def create_menu(app, menu_items, background=None, foreground=None, activebackground=None, activeforeground=None):
    menubar = ttk.Menu(
        app,
        tearoff=False,
        **({"background": background} if background else {}),
        **({"foreground": foreground} if foreground else {}),
        **({"activebackground": activebackground} if activebackground else {}),
        **({"activeforeground": activeforeground} if activeforeground else {})
    )

    for menu_item in menu_items:
        submenu = ttk.Menu(
            menubar,
            tearoff=False,
            **({"background": background} if background else {}),
            **({"foreground": foreground} if foreground else {}),
            **({"activebackground": activebackground} if activebackground else {}),
            **({"activeforeground": activeforeground} if activeforeground else {})
        )

        for item in menu_item["items"]:
            if item == "separator":
                submenu.add_separator()
            else:
                submenu.add_command(
                    label=item["label"],
                    command=item["command"]
                )

        menubar.add_cascade(
            label=menu_item["label"],
            menu=submenu
        )

    app.configure(menu=menubar)

    return menubar