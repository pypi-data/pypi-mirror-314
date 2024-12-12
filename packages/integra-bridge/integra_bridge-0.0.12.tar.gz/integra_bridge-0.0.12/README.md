## Integra bridge

````bash
pip install integra-bridge
````
Allows you to move the business logic of complex services outside of Integra.
Under the hood, interaction with Integra is carried out using the HTTP protocol based on REST FastAPI.  

`Bridge` - base class responsible for assembling services.

Params:  
    - `title` string - input title of service;   
    - `address` string | None - address of service location;  
    - `description` string | None - address of service location;  
    - `manual_path` string | Pathlike - Path to manual file; 

To map external URLs to local ones when writing handlers,  
use the variable **URL_PATH_MAPPER**, which must be set via a variable in the environment of your service in the form of a serializable JSON string.

#### Minimal example of data handler implementation:

````python
from integra_bridge import Bridge
from integra_bridge.adapters import ProcessorAdapter
from integra_bridge.dto import SkeletonProcessor, ProcessorView


class SimpleProcessor(ProcessorAdapter):
    async def execute(self, body: dict, params: dict) -> dict:
        body['hello'] = 'world'
        return body

    async def get_view(self) -> ProcessorView:
        skeleton = SkeletonProcessor()
        return ProcessorView(
            title="Simple processor",
            description="",
            skeleton=skeleton
        )
        
bridge = Bridge(
    title='My service',
    address='Moscow',
    description='For demo',
    manual_path=Path(__file__).parent / 'manual.pdf'
)

bridge.register_handlers([SimpleProcessor])

application = bridge.build()

if __name__ == '__main__':
    uvicorn.run(app="__main__:application", host='localhost', port=8000)
````

#### You can construct forms for your handler inside Integra using parameter classes and skeletons: 

````python3
server_name = Parameter(
    name='server_name',
    label='Server name',
    description='',
    default_value='google.com',
    is_required=True,
    is_add_value=True,
    bottom_text='bottom_text'
)

skeleton = SkeletonProcessor(parameters=[server_name,])
````

#### Validation of form fields at Integra level:

````python3
class SimpleProcessor(ProcessorAdapter):
    async def execute(self, body: dict, params: dict) -> dict:
        body['hello'] = 'world'
        return body

    async def validate(self, processor: Processor) -> ValidationResponse:
        result = True
        params_description = {}
        if len(processor.params.get('field_to_check')) > 10:
            result = False
            params_description['field_to_check'] = ['Превышена максимальная длинна в 10 символов']
        return ValidationResponse(
            result=result,
            params_description=params_description,
        )
````

### Example of implementation of an incoming connector using the RabbitMQ broker:

````python
# Class for handling input broker message
class ConsumerManager:
    def __init__(self):
        self.consumers = {}

    async def create_consumer(self, queue_name: str, connection_params: dict):
        connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
        channel = await connection.channel()
        exchange = await channel.declare_exchange(name='integra', type="fanout")
        queue = await channel.declare_queue(queue_name, auto_delete=False, durable=True)
        await queue.bind(exchange=exchange, routing_key=queue_name)
        callback = partial(self.on_message, queue_name=queue_name, connection_params=connection_params)
        consumer_tag = await queue.consume(callback, no_ack=False)
        self.consumers[queue_name] = {"connection": connection, "channel": channel, "consumer_tag": consumer_tag}
        return consumer_tag

    async def delete_consumer(self, queue_name: str, connection_params: dict):
        if queue_name in self.consumers:
            consumer = self.consumers[queue_name]
            await consumer["channel"].close()
            await consumer["connection"].close()
            del self.consumers[queue_name]

    async def on_message(self, message: AbstractIncomingMessage, queue_name, connection_params: dict) -> None:
        data = json.loads(message.body.decode('utf-8'))
        send_status = await ConnectorAdapter.push_to_integra(
            input_body=data,
            connect_to_block_id=queue_name
        )
        if send_status in (200, 201):
            await message.ack()

#Connector form parametrs
server_name = Parameter(
    name='server_name',
    label='Server name',
    is_required=True,
    is_add_value=True,
)
url = Parameter(
    name='url',
    label='url',
    is_required=True,
    is_add_value=True,
)

class SimpleInputConnector(ConnectorAdapter):
    async def get_view(self) -> ConnectorView:
        skeleton_connector = SkeletonConnector(type_connect='input', parameters=[server_name, url, ])
        return ConnectorView(
            title="Simple input connector",
            input_description="description",
            skeleton_input_connect=skeleton_connector
        )

    async def on_after_deploy(self, connection_id: str, connector_params: dict):
        await consumer_manager.create_consumer(connection_id, connector_params)

    async def on_after_destroy(self, connection_id: str, connector_params: dict):
        await consumer_manager.delete_consumer(connection_id, connector_params)
````
