PRIMARY_COLOR = "#0000FF"      # Синий фон кнопок
PRIMARY_TEXT = "#FFFFFF"       # Белый текст
ERROR_COLOR = "#FF0000"        # Красный для кнопок удаления
BACKGROUND_COLOR = "#F0F0F0"   # Цвет фона (если нужен)
MENU_HIGHLIGHT = "#0000AA"     # Цвет выделения пунктов меню


def button_style(bg=PRIMARY_COLOR, fg=PRIMARY_TEXT):
    return f"background-color: {bg}; color: {fg};"

def remove_button_style():
    return f"color: {ERROR_COLOR}; font-weight: bold;"