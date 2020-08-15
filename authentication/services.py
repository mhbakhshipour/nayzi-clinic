from kavenegar import *
import os
import logging

from requests import HTTPError

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


def get_token_crm():
    try:
        b = {'username': 'mhbp', 'password': '`tDj7*o*ZQ'}
        response = requests.post(url='https://45.149.77.48/api/login', json=b)
        logging.info(
            str({
                'action': 'crm_get_token',
                'gateway_response': str(response)
            })
        )
        return response.json()['token']
    except HTTPError as e:
        return e


def check_user_crm_history(mobile):
    try:
        token = get_token_crm()
        h = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
        response = requests.get(url='https://45.149.77.48/api/TelephonesData/' + mobile, headers=h)
        logging.info(
            str({
                'action': 'check_user_crm_history',
                'mobile': mobile,
                'gateway_response': str(response)
            })
        )
        return response
    except HTTPError as e:
        return e


def update_crm(mobile, body):
    try:
        token = get_token_crm()
        h = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}

        response = requests.put(url='https://45.149.77.48/api/TelephonesData/' + mobile, json=body, headers=h)
        logging.info(
            str({
                'action': 'update_crm',
                'gateway_response': str(response)
            })
        )
        return response
    except HTTPError as e:
        return e
