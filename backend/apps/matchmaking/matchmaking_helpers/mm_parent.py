import logging
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from apps.authentication.models import User

class MatchMakingParent:
    channel_layer = get_channel_layer()
    logger = logging.getLogger(__name__)
    _is_valid = False
    def __init__(self, data_json: dict, user: User):
        self.user = user
        self.data_json = data_json

    @database_sync_to_async
    def _log_info(self, to_log, message):
        self.logger.info(f'{message}:{to_log}')

    async def validate_data(self):
        pass