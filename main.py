from nicegui import ui
from backend import get_gas_stations

@ui.page('/')
def main_page():
    with ui.header(elevated=True).classes('py-2 bg-white text-black'):
        with ui.row().classes('items-center gap-1 px-4 lg:px-20 py-0'):
            ui.image('images/logo.png').classes('w-10 lg:w-16')
            ui.label('Fuel Finder') \
                .classes('text-2xl md:text-4xl font-medium')

    with ui.column().classes('w-full items-center gap-4 px-4 lg:px-20 my-4'):
        address_input = ui.input(placeholder='Enter your address or postal code with the country') \
            .props('rounded outlined dense') \
            .classes('w-full max-w-md')
        with address_input as i:
            ui.button(color='red', on_click=lambda: i.set_value(None), icon='delete') \
                .props('flat dense').bind_visibility_from(i, 'value')

        # Dynamic container for results
        results_container = ui.column().classes('w-full items-center gap-4')

        def show_stations():
            if not address_input.value:
                ui.notify('Enter a valid address...')
                return

            stations = get_gas_stations(address_input.value)

            if not stations:
                ui.label('No gas stations, please check the address!')
                return

            results_container.clear()

            with results_container:
                with ui.row().classes('flex-wrap justify-center gap-4 px-4 lg:px-20 my-4'):
                    for station in stations:
                        with ui.card().classes('w-full max-w-sm gap-1'):
                            with ui.row().classes('items-center justify-between w-full'):
                                with ui.column().classes('gap-1'):
                                    ui.label(station['name']).classes('font-bold text-lg')
                                    ui.label(f'{station["street"]} {station["houseNumber"]}, '
                                             f'{station["postCode"]} {station["place"]}') \
                                        .classes('text-sm')

                                ui.icon('navigation').classes('text-white bg-blue-400 rounded-full p-1 rotate-12')

                            with ui.column().classes('gap-1 mt-2'):
                                ui.label(f'E5: {station["e5"]}')
                                ui.label(f'E10: {station["e10"]}')
                                ui.label(f'Diesel: {station["diesel"]}')

                            ui.separator().classes('mt-2 border-gray-500')

                            open_status = 'Yes' if station['isOpen'] else 'No'
                            ui.label(f'Open: {open_status}').classes('mt-2 text-xs')

    # Bind Enter key to trigger station search
    address_input.on('keydown.enter', lambda _:show_stations())

ui.run()