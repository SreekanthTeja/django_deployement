
from pyfcm import FCMNotification
 
push_service = FCMNotification(api_key="AIzaSyD3JrrgmoLEaPjEL80E2nS6Jbtpvn_tePc")
 
# registration_id = "<device registration_id>"
# message_title = "Title"
# message_body = "Hello"
# result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
 
# print (result)
 
# # Send to multiple devices by passing a list of ids.
# # registration_ids = ["<device registration_id 1>", "<device registration_id 2>" ----]
# message_title = "Buidcron"
# message_body = "509601"
 
# print (result)
def send_otp(phone_number, otp):
    try:
        # result=push_service.notify_single_devices(registration_id="+918099961195", message_title="Buidcron", message_body="509601")
        # print(result)
        return {'status':'SENT'}
    except Exception as e:
        pass
