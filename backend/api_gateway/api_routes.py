from request_handlers import (
    HandleDataIngestion,
    HandleDataRetrieval,
    HandleDataProcessing,
)


def configure_routes(api):
    api.add_resource(HandleDataIngestion, "/ingest")
    api.add_resource(HandleDataProcessing, "/process")
    api.add_resource(HandleDataRetrieval, "/retrieve")
