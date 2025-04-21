# # consumers.py (Django Channels)
# from channels.generic.websocket import WebsocketConsumer
# import json
# from .models import Notification

# class NotificationConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         notification = Notification.objects.create(
#             user=self.scope['user'],
#             message=text_data_json['message'],
#             icon=text_data_json['icon']
#         )
#         self.send(text_data=json.dumps({
#             'id': notification.id,
#             'message': notification.message,
#             'icon': notification.icon,
#             'created_at': notification.created_at.strftime('%Y-%m-%d %H:%M:%S')
#         }))