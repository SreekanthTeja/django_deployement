import boto3
client = boto3.client(
    "sns",
    aws_access_key_id="AKIA47CQ27UR7RTO4KOF",
    aws_secret_access_key="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",
    region_name="ap-south-1"
)
smsattrs = {
    'AWS.SNS.SMS.SenderID': { 'DataType': 'String', 'StringValue': 'TestSender' },
    'AWS.SNS.SMS.SMSType': { 'DataType': 'String', 'StringValue': 'Transactional'}
}
def send_otp(phone_number, otp):
    try:
        client.publish(Message=otp, PhoneNumber=phone_number, MessageAttributes=smsattrs)
        print(client)
        return {'status':'SENT'}
    except Exception as e:
        pass
