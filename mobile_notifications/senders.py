import logging
from django.conf import settings
from gcm import GCM

from .apns import APNs, Payload
from .models import IOSDevice, AndroidDevice


INVALID_TOKEN = 8
ANDROID_PUSH_LIMIT = 1000

cert_pem = getattr(settings, 'APNS_CERT_PEM', None)
key_pem = getattr(settings, 'APNS_KEY_PEM', None)
api_key = getattr(settings, 'GCM_API_KEY', None)
use_sandbox = getattr(settings, 'APNS_USE_SANDBOX', True)

logger = logging.getLogger(__name__)


class APNSNotification(object):

    def __init__(self, device, alert, custom={}, badge=0, sound='default',
                 content_available=True):
        self.payload = Payload(
            alert=alert,
            sound=sound,
            badge=badge,
            custom=custom,
            content_available=content_available
        )
        self.uid = device.id
        self.reg_id = device.reg_id


def apns_send(notifications, use_sandbox=use_sandbox, enhanced=True):
    if cert_pem and key_pem:
        for notification in notifications:
            apns = APNs(
                use_sandbox=use_sandbox,
                cert_file=cert_pem,
                key_file=key_pem,
                enhanced=enhanced
            )
            apns.gateway_server.register_response_listener(response_listener)

            apns.gateway_server.send_notification(
                notification.reg_id,
                notification.payload,
                identifier=notification.uid
            )
    else:
        logger.warning('APNS_CERT_PEM and APNS_KEY_PEM do not set.')


def response_listener(error_response):
    status = error_response['status']
    identifier = error_response['identifier']
    if status == INVALID_TOKEN:
        IOSDevice.objects.filter(id=identifier).delete()


def apns_send_testing(use_sandbox=use_sandbox, enhanced=True):
    notifications = []
    for device in IOSDevice.objects.filter(testing=True):
        notification = APNSNotification(
            device=device,
            alert='test',
            badge=1
        )
        notifications.append(notification)
    apns_send(notifications, use_sandbox, enhanced)


class GCMNotification(object):

    def __init__(self, reg_ids, data, collapse_key=None):
        """
        reg_ids: an array contains all to be pushed registration ids
        """
        self.reg_ids = reg_ids
        self.data = data
        self.collapse_key = collapse_key

    def device_count(self):
        return len(self.reg_ids)


def gcm_send(notification):
    if api_key:
        start_index = 0
        device_count = notification.device_count()

        while(start_index < device_count):
            push_ids = notification.reg_ids[
                start_index:(start_index + ANDROID_PUSH_LIMIT)
            ]
            gcm = GCM(api_key=api_key)
            response = gcm.json_request(
                registration_ids=push_ids,
                data=notification.data,
                collapse_key=notification.collapse_key
            )

            # Handling errors
            if 'errors' in response:
                for error, fail_reg_ids in response['errors'].items():
                    # Check for errors and act accordingly
                    if error is 'NotRegistered':
                        # Remove reg_ids from database
                        for reg_id in fail_reg_ids:
                            AndroidDevice.objects.filter(reg_id=reg_id).delete()
            if 'canonical' in response:
                for reg_id, canonical_id in response['canonical'].items():
                    # Repace reg_id with canonical_id in your database
                    try:
                        entry = AndroidDevice.objects.get(reg_id=reg_id)
                        if entry.reg_id is not canonical_id:
                            entry.delete()
                    except AndroidDevice.DoesNotExist:
                        pass
            start_index += ANDROID_PUSH_LIMIT
    else:
        logger.warning('GCM_API_KEY does not be set.')
