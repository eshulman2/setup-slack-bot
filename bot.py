import os
from tinydb import TinyDB, Query
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

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


DB = db()

# Install the Slack app and get xoxb- token in advance
app = App(token=os.environ.get('BOT_TOKEN'))

# @app.event("app_mention")
# def event_test(say, body):
#     print(body['elements']['text'])
#     # say("Hi there!")

@app.command("/show-all-setups")
def hello_command(ack, command, respond):
    ack()
    respond(DB.get_all_servers())

@app.command("/use-server")
def hello_command(ack, command, respond):
    DB.update_server_user(command["text"], command["user"])
    ack("ack")
    
@app.command("/free-server")
def hello_command(ack, command, respond):
    DB.update_server_user(command["text"])
    ack("ack")

@app.command("/list-free")
def hello_command(ack, command, respond):
    ack(DB.list_free_servers())

if __name__ == "__main__":
    # 'xapp- (zap) App Token'
    SocketModeHandler(app, os.environ.get('APP_TOKEN')).start()
