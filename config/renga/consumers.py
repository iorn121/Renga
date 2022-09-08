import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebSocketConsumer


class RengaConsumer(WebSocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.group_name = 'renga_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name,
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {'type': 'renga_message',
                                  'message': message}
        )

    def renga_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({'message': message}))
