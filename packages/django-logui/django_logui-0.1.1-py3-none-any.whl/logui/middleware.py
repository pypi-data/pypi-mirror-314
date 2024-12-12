import logging

from django.utils.deprecation import MiddlewareMixin

from logui.conf import LOGUI_URL_PREFIX


class RequestResponseLoggerMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.get_response = get_response
        from logui.conf import LOGUI_REQUEST_RESPONSE_LOGGER_NAME
        if not LOGUI_REQUEST_RESPONSE_LOGGER_NAME:
            raise ValueError(
                f'For use RequestResponseLoggerMiddleware you need to add the LOGUI_REQUEST_RESPONSE_LOGGER_NAME variable to your django settings.')
        self.log = logging.getLogger(
            LOGUI_REQUEST_RESPONSE_LOGGER_NAME
        ) if LOGUI_REQUEST_RESPONSE_LOGGER_NAME else None

    def process_request(self, request):
        if self.log and LOGUI_URL_PREFIX not in request.path:
            self.log.info(f'⏴ {request.ip} {request.method} {request.path}')
        return None

    def process_response(self, request, response):
        if self.log and LOGUI_URL_PREFIX not in request.path:
            self.log.info(f'⏵ {request.ip} {request.method} {request.path} {response.status_code}')
        return response
