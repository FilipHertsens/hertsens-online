import ast
from flask_login import current_user

def navbuttons():
    buttons = []
    if current_user.is_active:
        buttons = ast.literal_eval(current_user.roles[0].list_navButtons)
    return buttons