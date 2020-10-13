from flask_restplus import Namespace, Resource
from flask import jsonify
from sqlalchemy import func

from schemas.models import InsuredEvent, Policyholder, AggregatedMetrics

metrics_ns = Namespace('aggregated_metrics', description='Routes for aggregated metrics')


@metrics_ns.route('/', doc={"description": "Returns aggregated metrics"})
class Metrics(Resource):
    """
    An endpoint to retrieve the following metrics:
        - total covered amount for all claims
        - total claims filed
        - average age of insured

    :return: AggregatedMetrics object containing the information above
    """
    @staticmethod
    def get():
        covered_amount = InsuredEvent.query.with_entities(func.sum(InsuredEvent.covered_amount).label('count')).first()
        average_age = Policyholder.query.with_entities(
            func.avg(func.age(Policyholder.date_of_birth)).label('average_age')).first()
        claims_count = InsuredEvent.query.count()

        return jsonify(
            aggregated_metrics=AggregatedMetrics(covered_amount[0], (average_age[0].days / 365), claims_count).__dict__
        )

