from kavenegar import *
import os
import logging

logger = logging.getLogger('app')


def send_otp(token, mobile, str_hash):
    try:
        api = KavenegarAPI(os.environ.get('KAVENEGAR_API_KEY'))
        params = {
            'receptor': mobile,
            'template': 'otp-nayzi',
            'token': str(token),
            'token2': str(str_hash),
        }
        response = api.verify_lookup(params)
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
