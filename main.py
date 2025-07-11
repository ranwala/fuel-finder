from click import style
from nicegui import ui
from backend import get_gas_stations

@ui.page('/', favicon='images/favicon.ico', title='Fuel Finder')
def main_page():
    with ui.header(elevated=True).classes(
            'py-2 bg-gradient-to-r from-blue-50 via-white to-blue-50 text-black shadow-md'
    ):
        with ui.row().classes('items-center justify-between w-full px-4 lg:px-20'):
            # Logo + Brand
            with ui.row().classes('items-center gap-3'):
                ui.image('images/logo.png').classes('w-10 lg:w-16')
                ui.label('Fuel Finder').classes('text-2xl md:text-4xl font-semibold text-blue-700')

    with ((ui.column().classes('w-full items-center gap-4 px-4 lg:px-20 my-4'))):
        address_input = ui.input(placeholder='Enter your address or postal code...') \
            .props('rounded outlined dense') \
            .classes('w-full max-w-md') \
            .style('font-size:16px;')

        with address_input as i:
            ui.button(color='primary', icon='search', on_click=lambda: show_stations()) \
                .props('flat dense').bind_visibility_from(i, 'value')

        # Dynamic container for results
        results_container = ui.column().classes('w-full items-center gap-4')

        def show_stations():
            if not address_input.value:
                ui.notify('Enter a valid address...')
                return

            stations = get_gas_stations(address_input.value)

            results_container.clear()

            if not stations:
                with results_container:
                    ui.label('No gas stations, please check the address!')
                return

            with results_container:
                with ui.row().classes('flex-wrap justify-center gap-4 px-4 lg:px-20 my-4'):
                    for station in stations:
                        with ui.card().classes('w-full max-w-sm p-4 shadow-md rounded-2xl'):
                            with ui.row().classes('items-center justify-between w-full'):
                                ui.label(station['name']) \
                                    .tooltip(station['name']) \
                                    .classes('text-lg font-bold truncate flex-1 mr-2')
                                ui.label('Open' if station['isOpen'] else 'Closed') \
                                    .classes(f'text-sm px-3 py-1 rounded-full shrink-0 '
                                             f'{"bg-green-100 text-green-800" if station["isOpen"] else "bg-red-100 text-red-800"}')

                            # Address
                            ui.label(f'{station["street"]} {station["houseNumber"]}, '
                                             f'{station["postCode"]} {station["place"]}') \
                                .tooltip(f'{station["street"]} {station["houseNumber"]}, '
                                             f'{station["postCode"]} {station["place"]}') \
                                .classes('text-sm text-gray-600 truncate w-full mt-1')

                            # Prices
                            with ui.row().classes('justify-start gap-2 mt-3 flex-wrap'):
                                ui.label(f'E5: {station["e5"]}') \
                                    .classes('text-sm px-3 py-1 bg-gray-100 rounded-md')
                                ui.label(f'E10: {station["e10"]}') \
                                    .classes('text-sm px-3 py-1 bg-gray-100 rounded-md')
                                ui.label(f'Diesel: {station["diesel"]}') \
                                    .classes('text-sm px-3 py-1 bg-gray-100 rounded-md')

    # Bind Enter key to trigger station search
    address_input.on('keydown.enter', lambda _:show_stations())
    address_input.on('blur', lambda _: show_stations())

ui.run()