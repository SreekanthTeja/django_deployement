import boto3
client = boto3.client(
    "sns",
    aws_access_key_id="AKIA47CQ27URZ2VQOTYN",
    aws_secret_access_key="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",
    region_name="us-east-1"
)

def send_otp(phone_number, otp):
    try:
        print("helooo")
        otp_request = client.publish(PhoneNumber=phone_number,Message="Your OTP to login %s"%(otp), MessageAttributes={'AWS.SNS.SMS.SMSType': {'DataType': 'String','StringValue': 'Transactional'}})
        print("otp", otp_request)
        return True
    except Exception as e:
        pass
