import asyncio
import datetime
import json
import uuid
import websockets
from websockets import ConnectionClosed


FN_CALL = 'notify-infraction-call'
RDM_URL = 'ws://www.radop.ml:8765/'
RDM_OPERATION = 'insert'
RDM_DATABASE = 'NOTIFY'
RDM_TABLE = 'infraction'
RDM_AUDIT_DATABASE = 'AUDIT'
RDM_AUDIT_TABLE = 'fn_notify_infraction'
PENALTY_IDENTIFIER = {
    0: {
        'level': 'Média',
        'value': 130.16,
        'points': 4
    },
    1: {
        'level': 'Grave',
        'value': 195.23,
        'points': 5
    },
    2: {
        'level': 'Gravíssima',
        'value': 880.41,
        'points': 7
    }
}


def generate_rfc_time():
    time = datetime.datetime.utcnow()
    time = str(time.isoformat('T'))
    time = time.rsplit('.')[0] + 'Z'
    return time


def generate_uuid():
    return str(uuid.uuid4())


def success_message(message):
    status_code = 200
    response = {
        'status_code': status_code,
        'message': message
    }
    return response


def failure_message(message, status_code=500):
    response = {
        'status_code': status_code,
        'message': message
    }
    return response


async def send_audit_data(data):
    async with websockets.connect(
        f'{RDM_URL}{RDM_OPERATION}'
    ) as websocket:
        identifier = generate_uuid()
        time = generate_rfc_time()
        call = 'rethink-manager-call'
        payload = {
            'database': RDM_AUDIT_DATABASE,
            'table': RDM_AUDIT_TABLE,
            'data': data
        }

        package = {
            'id': identifier,
            'type': call,
            'payload': payload,
            'time': time
        }

        await websocket.send(json.dumps(package))

        try:
            message = await asyncio.wait_for(websocket.recv(), timeout=20)
            if message is None:
                raise Exception('No message was received from WS.')
            else:
                return message
        except (ConnectionRefusedError) as err:
            return err
        except ConnectionClosed as err:
            return err
        except RuntimeError as err:
            return err
        except Exception as err:
            return err


async def send_notify_data(data):
    async with websockets.connect(
        f'{RDM_URL}{RDM_OPERATION}'
    ) as websocket:
        identifier = generate_uuid()
        time = generate_rfc_time()
        call = 'rethink-manager-call'
        payload = {
            'database': RDM_DATABASE,
            'table': RDM_TABLE,
            'data': data
        }

        package = {
            'id': identifier,
            'type': call,
            'payload': payload,
            'time': time
        }

        await websocket.send(json.dumps(package))

        try:
            message = await asyncio.wait_for(websocket.recv(), timeout=20)
            if message is None:
                raise Exception('No message was received from WS.')
            else:
                return message
        except (ConnectionRefusedError) as err:
            return err
        except ConnectionClosed as err:
            return err
        except RuntimeError as err:
            return err
        except Exception as err:
            return err


def create_notification(identifier, vehicle, infraction):
    allowed_speed = infraction['max_allowed_speed']
    read_speed = infraction['vehicle_speed']
    considered_speed = infraction['considered_speed']
    penalty = infraction['infraction']
    brand, model = vehicle['brand'].rsplit('/')
    chassis = vehicle['chassis']
    city = vehicle['city']
    color = vehicle['color']
    date, time = vehicle['date'].rsplit(' às ')
    model_year = vehicle['year']
    plate = vehicle['plate']
    state = vehicle['state']
    status = vehicle['status_message']

    notification = {
        'infraction_identifier': identifier,
        'allowed_track_speed': allowed_speed,
        'read_speed': read_speed,
        'considered_speed': considered_speed,
        'penalty': PENALTY_IDENTIFIER[penalty],
        'date': date,
        'time': time,
        'vehicle_brand': brand,
        'vehicle_model': model,
        'vehicle_year': model_year,
        'vehicle_chassi': chassis,
        'vehicle_color': color,
        'vehicle_plate': plate,
        'vehicle_city': city,
        'vehicle_state': state,
        'vehicle_status': status
    }

    return notification


def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    try:
        package = json.loads(req)
        package_type = package['type']
        package_payload = package['payload']
        package_id = package['id']
        infraction_id = package_payload['infraction_id']
        infraction_data = package_payload['infraction_data']
        vehicle_data = package_payload['vehicle_data']

        infraction = create_notification(
            infraction_id,
            vehicle_data,
            infraction_data
        )

        if package_type != FN_CALL:
            error_msg = (f'Error!! The message header indicates other '
                         f'function call. Verify if the correct service '
                         f'was called.')
            response = failure_message(error_msg)
            return response

        loop = asyncio.get_event_loop()
        loop.run_until_complete(send_audit_data(package))
        notification = loop.run_until_complete(send_notify_data(infraction))
        notification = json.loads(notification)
        notification_id = notification['response_message']['generated_keys'][0]

        response = success_message(
            f'A  infração {package_id} (ID) será notificada. O identificador '
            f'da notificação é {notification_id}'
        )

        response.update({'notification': infraction})

    except (TimeoutError, ConnectionRefusedError) as err:
        response = failure_message(str(err))
        return response
    except ConnectionClosed as err:
        response = failure_message(str(err))
        return response
    except RuntimeError as err:
        response = failure_message(str(err))
        return response
    except Exception as err:
        response = failure_message(str(err))
        return response
    else:
        return response
