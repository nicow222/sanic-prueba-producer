from sanic import Sanic
from services.service_note import task_create_note
from services.service_grpc import server


app = Sanic(__name__)

@app.listener('before_server_start')
async def setup_server(app, loop):
    app.add_task(task_create_note)
    app.add_task(server)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)