def setup_airtable(self):
    self.api = Api(os.environ['AIRTABLE_API_KEY'])
    self.table = self.api.table(os.getenv('AIRTABLE_BASE_KEY'), os.getenv('AIRTABLE_TABLE_NAME'))
    self.data = self.table.all(view="Grid view")