import os
import db
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

DB = db.db()
# Install the Slack app and get xoxb- token in advance
app = App(token=os.environ.get('BOT_TOKEN'))

@app.command("/show-all-setups")
def hello_command(ack, command, respond):
    ack()
    respond(DB.get_all_servers())

@app.command("/use-server")
def hello_command(ack, command, respond):
    DB.update_server_user(command["text"], command["user_name"])
    ack(f"server {command['text']} is now used by {command['user_name']}")
    
@app.command("/free-server")
def hello_command(ack, command, respond):
    DB.free_up_server(command["text"])
    ack("ack")

@app.command("/list-free")
def hello_command(ack, command, respond):
    ack()
    respond(DB.list_free_servers())

if __name__ == "__main__":
    # 'xapp- (zap) App Token'
    SocketModeHandler(app, os.environ.get('APP_TOKEN')).start()
