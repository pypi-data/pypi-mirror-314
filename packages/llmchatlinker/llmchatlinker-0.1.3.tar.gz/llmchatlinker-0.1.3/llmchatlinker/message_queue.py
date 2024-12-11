import os
import pika
import uuid
import logging
import time
from pika.exceptions import StreamLostError

logging.basicConfig(level=logging.INFO)

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5673))
# RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
# RABBITMQ_PASS = os.getenv('RABBITMQ_PASSWORD', 'guest')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'myuser')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASSWORD', 'mypassword')
INSTRUCTION_QUEUE = 'instruction_queue'
MAX_RETRIES = 5
RETRY_DELAY = 5

class MessageQueueClient:
    def __init__(self, queue_name=INSTRUCTION_QUEUE):
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
        self.response = None
        self.corr_id = None
        self.callback_queue = None
        self._initialize_connection()

    def _initialize_connection(self):
        """Initialize connection with retries."""
        self._retry_with_backoff(self._connect)

    def _connect(self):
        """Connect to RabbitMQ"""
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=credentials,
            heartbeat=600,
            blocked_connection_timeout=300
        ))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        self.callback_queue = self.channel.queue_declare(queue='', exclusive=True).method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )
        logging.info("Successfully connected to RabbitMQ")

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, instruction):
        """Send an instruction and wait for a response."""
        self._retry_with_backoff(self._publish_instruction, instruction)
        return self.response

    def _publish_instruction(self, instruction):
        """Publish an instruction to the queue."""
        if self.connection is None or self.connection.is_closed:
            self._initialize_connection()

        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
                delivery_mode=2  # Make message persistent
            ),
            body=instruction
        )
        while self.response is None:
            try:
                self.connection.process_data_events(time_limit=1)
            except StreamLostError:
                logging.error("Lost connection while waiting for response")
                self._initialize_connection()
                break

    @staticmethod
    def _retry_with_backoff(func, *args):
        """Retries a function with exponential backoff."""
        for attempt in range(MAX_RETRIES):
            try:
                func(*args)
                return
            except Exception as e:
                logging.error(f"Error (attempt {attempt + 1}/{MAX_RETRIES}): {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                else:
                    raise

def publish_message(message):
    client = MessageQueueClient()
    return client.call(message)

def publish_response(channel, message, correlation_id, reply_to):
    try:
        channel.basic_publish(
            exchange='',
            routing_key=reply_to,
            properties=pika.BasicProperties(
                correlation_id=correlation_id,
                delivery_mode=2
            ),
            body=message
        )
    except Exception as e:
        logging.error(f"Error publishing response: {e}")
        raise

def init_message_queue(queue_name):
    client = MessageQueueClient(queue_name)
    return client.channel, queue_name

def consume_messages(channel, queue_name, callback):
    def callback_wrapper(ch, method, properties, body):
        try:
            callback(body, properties)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logging.error(f"Error processing message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback_wrapper)

    while True:
        try:
            logging.info(f"Waiting for messages in {queue_name}")
            channel.start_consuming()
        except StreamLostError:
            logging.error("Connection lost. Attempting to reconnect...")
            time.sleep(RETRY_DELAY)
            channel, _ = init_message_queue(queue_name)
        except KeyboardInterrupt:
            channel.stop_consuming()
            break
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            time.sleep(RETRY_DELAY)