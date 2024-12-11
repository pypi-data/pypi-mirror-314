from wedeliver_core_plus.helpers.topics import Topics
from wedeliver_core_plus.helpers import kafka_producers
def send_sms(message, mobile):
    if not isinstance(mobile, list):
        mobile = [mobile]
    kafka_producers.send_topic(topic=Topics().SEND_SMS, datajson=dict(
        function_name='app.business_logic.bulk_sms.send_v2.send_bulk_v2',
        function_params=dict(
            sms_message=message, mobile_numbers=mobile
        )
    ))
