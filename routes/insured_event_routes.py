import datetime
from flask_restplus import Namespace, Resource, fields
from flask import jsonify, request
from schemas.models import db, InsuredEvent

insured_event_ns = Namespace('insured_event', description='Insured event related operations')

insured_event_model = insured_event_ns.model('insured_event', {'date_of_incidence': fields.String(description='Date of incidence', required=True, example="10/10/2020"),
                                                                'billed_amount': fields.Float(description='Amount billed', required=True, example=250.00),
                                                                'covered_amount': fields.Float(description='Amount covered', required=False, example=150.50),
                                                                'type_of_issue': fields.String(description='Medical Issue', required=False, example="Broken Wrist"),
                                                                'policyholder_id': fields.Integer(description='Policy holder ID', required=False, example=1)})


# Insured Event Namespace Routes #
@insured_event_ns.route('/create_insured_event', doc={"description": "Create a new insured event"})
class CreateInsuredEvent(Resource):
    """
    An endpoint to create an insured event.

    :return: Unique ID of the new insured event.
    """
    @insured_event_ns.expect(insured_event_model)
    def post(self):
        date_of_incidence = datetime.datetime.strptime(insured_event_ns.payload.get('date_of_incidence'), '%m/%d/%Y')
        billed_amount = insured_event_ns.payload.get('billed_amount')
        covered_amount = insured_event_ns.payload.get('covered_amount')
        type_of_issue = insured_event_ns.payload.get('type_of_issue')
        policyholder_id = insured_event_ns.payload.get('policyholder_id')

        insured_event = InsuredEvent(date_of_incidence=date_of_incidence, billed_amount=billed_amount,
                                     covered_amount=covered_amount,
                                     type_of_issue=type_of_issue, policyholder_id=policyholder_id)
        db.session.add(insured_event)
        db.session.commit()
        return jsonify(
            id=insured_event.id
        )


@insured_event_ns.route('/', doc={"description": "Returns all insured events"})
class InsuredEvents(Resource):
    """
    An endpoint to retrieve all Insured events.

    :return: List of all insured events.
    """
    @staticmethod
    def get():
        insured_events = InsuredEvent.query.all()
        return jsonify(
            insured_events=insured_events
        )
