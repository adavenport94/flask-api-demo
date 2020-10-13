from flask_restplus import Api

from .policyholder_routes import policyholder_ns as policyholder_api
from .insured_event_routes import insured_event_ns as insured_event_api
from .metrics_routes import metrics_ns as metrics_api

api = Api(
    title='Health Insurance Policy API',
    version='1.0',
    description='A simple health insurance policy API',
    doc="/docs/"
)

api.add_namespace(policyholder_api)
api.add_namespace(insured_event_api)
api.add_namespace(metrics_api)
