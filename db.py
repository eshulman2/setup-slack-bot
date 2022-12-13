
from tinydb import TinyDB, Query

class db():
    def __init__(self, db_file='./db.json'):
        self.db = TinyDB(db_file)
        self.set_up_table = self.db.table('set_up')
        self.query = Query()
    
    def get_all_servers(self):
        return '\n'.join([str(server) for server in self.set_up_table.all()])

    def update_server_user(self, set_up, user_name):
        self.set_up_table.upsert(
                {'setup': set_up, 'user': user_name, 'in_use': True},
                self.quary.setup == set_up)

    def free_up_server(self, set_up):
        self.set_up_table.upsert({'setup': set_up, 'user': None,
                'in_use': False},
                self.quary.setup == set_up)

    def list_free_servers(self):
        '\n'.join([str(server) for server in 
                    self.set_up_table.search(self.quary.in_use == 'False')])

