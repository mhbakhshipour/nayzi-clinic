from kavenegar import *
import os
import logging

logger = logging.getLogger('app')


def send_otp(token, mobile):
    try:
        api = KavenegarAPI(os.environ.get('KAVENEGAR_API_KEY'))
        params = {
            'sender': os.environ.get('KAVENEGAR_SENDER'),
            'receptor': mobile,
            'message': 'کد فعال سازی :' + str(token),
        }
        response = api.sms_send(params)
        logging.info(
            str({
                'action': 'SEND_SMS',
                'api_key': os.environ.get('KAVENEGAR_API_KEY'),
                'token': token,
                'mobile': mobile,
                'gateway_response': str(response)

            })
        )
        return response[0]['status']
    except APIException as e:
        return e
    except HTTPException as e:
        return e
