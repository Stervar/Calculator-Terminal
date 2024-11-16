import dearpygui.dearpygui as dpg

def button_callback(sender, app_data):
    dpg.set_value("text", "Кнопка нажата!")

dpg.create_context()
dpg.create_viewport(title='Dear PyGui Калькулятор', width=400, height=200)

with dpg.window(label="Главное окно"):
    dpg.add_text("Нажмите кнопку:")
    dpg.add_button(label="Нажми меня", callback=button_callback)
    dpg.add_text("", tag="text")

dpg.create_viewport()
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()