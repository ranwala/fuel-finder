from nicegui import ui
from backend import get_gas_stations

stations = get_gas_stations()

with ui.grid(columns=2):
    for station in stations:
        with ui.card():
            with ui.column().classes('gap-0'):
                ui.label(station['name']).tailwind.font_weight('bold')
                ui.label(f'{station["street"]} {station['houseNumber']}, {station['postCode']} {station['place']}')

            with ui.column().classes('gap-0'):
                ui.label(f'E5: {station["e5"]}')
                ui.label(f'E10: {station["e10"]}')
                ui.label(f'Diesel: {station["diesel"]}')


            ui.label(f'Open: ')


ui.run()