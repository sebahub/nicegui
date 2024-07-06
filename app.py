#!/usr/bin/env python3
from nicegui import ui, Tailwind

columns = [
    {'field': 'name', 'editable': True, 'sortable': True},
    {'field': 'age', 'editable': True},
    {'field': 'id'},
]
rows = [
    {'id': 0, 'name': 'Alice', 'age': 18},
    {'id': 1, 'name': 'Bob', 'age': 21},
    {'id': 2, 'name': 'Carol', 'age': 20},
]


@ui.page('/')
def page():
    ui.add_sass('./styles.sass')
    def add_row():
        new_id = max((dx['id'] for dx in rows), default=-1) + 1
        rows.append({'id': new_id, 'name': 'New name', 'age': None})
        ui.notify(f'Added row with ID {new_id}')
        aggrid.update()

    def handle_cell_value_change(e):
        new_row = e.args['data']
        ui.notify(f'Updated row to: {e.args["data"]}')
        rows[:] = [row | new_row if row['id'] == new_row['id'] else row for row in rows]

    async def delete_selected():
        selected_id = [row['id'] for row in await aggrid.get_selected_rows()]
        rows[:] = [row for row in rows if row['id'] not in selected_id]
        ui.notify(f'Deleted row with ID {selected_id}')
        aggrid.update()

    def test_function():
        ui.notify('test function')

    # style with external sass file
    with ui.element('div').classes('flex justify-between w-full'):
        # ui.input(placeholder='suche').props('outlined dense filled standout color=teal').classes('search-bar')
        # input with html
        # ui.html('<input type="text" class="search-bar" placeholder="suche">')
        search_input = ui.input(label='Search:', on_change=lambda e: search(e.value))
        with ui.element('div').classes('flex gap-5'):
            with ui.element('button').on('click', test_function).classes('button'):
                ui.label('print')
                ui.icon('print').classes('ml-2')
            with ui.element('button').on('click', test_function).classes('button'):
                # ui.label('refresh')
                ui.icon('refresh').classes('')

    aggrid = ui.aggrid({
        'columnDefs': columns,
        'rowData': rows,
        'rowSelection': 'multiple',
        'stopEditingWhenCellsLoseFocus': True,
    }, theme='balham').on('cellValueChanged', handle_cell_value_change)

    def search(query):
        filtered_rows = [row for row in rows if query.lower() in row['name'].lower()]
        aggrid.options['rowData'] = filtered_rows
        aggrid.update()
        ui.notify('..Suche')

    # # Works both
    # with ui.element('div').classes('p-2 bg-blue-100').on('click', test_function):
    #     ui.label('testinger').on('click', test_function)


    # # ui.button.default_props('rounded outline')
    # # Style with Qasar props
    # ui.button('Print', icon='print').props('color=green')
    # # style with tailwind classes
    # ui.button('Button B').classes('text-purple-700 hover:text-white border border-purple-700 hover:bg-purple-800 focus:ring-4 focus:outline-none focus:ring-purple-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2 dark:border-purple-400 dark:text-purple-400 dark:hover:text-white dark:hover:bg-purple-500 dark:focus:ring-purple-900')

        

    # ui.button('Delete selected', on_click=delete_selected)
    # ui.button('New row', on_click=add_row)



ui.run()