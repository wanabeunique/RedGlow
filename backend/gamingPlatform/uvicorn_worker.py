from uvicorn.workers import UvicornWorker


class CustomUvicornWorker(UvicornWorker):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config.lifespan = 'off'
        self.config.ws = 'websockets'
        self.config.log_level = 'debug'
