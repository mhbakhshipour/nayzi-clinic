from kavenegar import *
import os
import logging

logger = logging.getLogger('app')


def send_otp(token, mobile, str_hash):
    try:
        api = KavenegarAPI(os.environ.get('KAVENEGAR_API_KEY'))
        params = {
            'sender': os.environ.get('KAVENEGAR_SENDER'),
            'receptor': mobile,
            'message': 'کلینیک نای ذی\nرمز احراز هویت شما: ' + str(token) + '\n\n' + str(
                str_hash) if str_hash is not None else '',
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
