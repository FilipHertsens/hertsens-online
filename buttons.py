
def navbuttons(user):
    buttons = {}
    if user.is_active:
        for role_buttons in user.roles:
            for button in role_buttons.navbarbutton:
                if button.navbarcat.name not in buttons:
                    buttons[button.navbarcat.name] = []
                bn = {'name':button.name,'type':button.type,'href':button.href,}
                buttons[button.navbarcat.name].append(bn)

    return buttons