import os
from dotenv import load_dotenv
from nicegui import ui
from pyairtable import Api

load_dotenv()

def fetch_data():
    api = Api(os.environ['AIRTABLE_API_KEY'])
    table = api.table(os.environ['AIRTABLE_BASE_KEY'], os.environ['AIRTABLE_TABLE_NAME'])
    return table.all()

data = fetch_data()

columns = [
    {'field': 'Sorte', 'sortable': True},
    {'field': 'THC', 'sortable': True},
    {'field': 'CBD', 'sortable': True},
    {'field': 'Dominanz', 'sortable': True},
    {'field': 'Verfall', 'sortable': True},
    {'field': 'PZN', 'sortable': False},
    {'field': 'Charge', 'sortable': False, 'editable': True},
]


rows = []
for record in data:
    row = {'id': record['id']}
    for column in columns:
        field_name = column['field']
        row[field_name] = record['fields'].get(field_name, None)
    rows.append(row)

@ui.page('/')
def page():
    ui.add_sass('./styles.sass')

    def handle_cell_value_change(e, table):
        new_row = e.args['data']
        record_id = new_row['id']
        field_name = e.args['colId']
        new_value = e.args['newValue']
        
        ui.notify(f'Record ID: {record_id}, Field: {field_name}, New Value: {new_value}')
        
        # Update the row data locally
        rows[:] = [row | new_row if row['id'] == new_row['id'] else row for row in rows]
        
        # Update the record in Airtable
        table.update(record_id, {field_name: new_value})

    def test_function():
        ui.notify('test function')

    # style with external sass file
    with ui.element('div').classes('flex justify-between w-full'):
        # ui.input(placeholder='suche').props('outlined dense filled standout color=teal').classes('search-bar')
        # input with html
        # ui.html('<input type="text" class="search-bar" placeholder="suche">')
        search_input = ui.input(label='Search:', on_change=lambda e: search(e.value)).classes('search-bar').props('dense')
        with ui.element('div').classes('flex gap-5'):
            with ui.element('button').on('click', test_function).classes('button'):
                ui.label('print')
                ui.icon('print').classes('ml-2')
            with ui.element('button').on('click', test_function).classes('button'):
                # ui.label('refresh')
                ui.icon('refresh').classes('')

    # Create the Airtable API object and fetch data
    api = Api(os.environ['AIRTABLE_API_KEY'])
    table = api.table(os.environ['AIRTABLE_BASE_KEY'], os.environ['AIRTABLE_TABLE_NAME'])

    aggrid = ui.aggrid({
        'columnDefs': columns,
        'rowData': rows,
        'rowSelection': 'multiple',
        'stopEditingWhenCellsLoseFocus': True,
    }).on('cellValueChanged', lambda e: handle_cell_value_change(e, table)).style('width: 100%')

    def search(query):
        filtered_rows = [row for row in rows if query.lower() in row['Sorte'].lower()]
        aggrid.options['rowData'] = filtered_rows
        aggrid.update()
        # ui.notify('..Suche')

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