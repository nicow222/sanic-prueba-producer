from aio_pika import connect_robust, IncomingMessage
from config.database import get_database

async def process_message(message: IncomingMessage):
    async with message.process():
        message_data = message.body.decode()
        db = await get_database()
        
        if db is None:
            raise Exception("Failed to establish database connection")
        
        user_collection = db['users']
        note_collection = db['note']

        user_info = user_collection.find_one({'_id': message_data})

        # Crear una nueva nota para el usuario
        note_info = {
            'user_id': user_info['_id'],
            'user_email': user_info['email'],
            'title': 'RabbitMQ',
            'body': f'Nota para el usuario {user_info["name"]}'
        }

        # Insertar la nueva nota en la base de datos de MongoDB
        note_collection.insert_one(note_info).inserted_id

async def task_create_note():
    connection = await connect_robust(
        "amqp://guest:guest@127.0.0.1/",
    )

    queue_name = "users_queue"

    # Creating channel
    channel = await connection.channel()

    # Maximum message count which will be processing at the same time.
    await channel.set_qos(prefetch_count=100)

    # Declaring queue
    queue = await channel.declare_queue(queue_name)

    await queue.consume(process_message)