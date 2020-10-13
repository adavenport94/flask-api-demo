import datetime
from flask_restplus import Namespace, Resource, fields
from flask import jsonify
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from schemas.models import Policyholder, db

policyholder_ns = Namespace('policyholder', description='Policyholder related operations')

policyholder_model = policyholder_ns.model('policyholder', {'gender': fields.String(description='Gender', required=True, example='Female'),
                                                            'date_of_birth': fields.String(description='Birth date', required=True, example='6/20/1994'),
                                                            'ssn': fields.Integer(description='Social security number', required=True, example=11122333),
                                                            'smoking_status': fields.Boolean(description='Smoking status', required=False, example=True),
                                                            'allergies': fields.String(description='Allergies', required=False, example='Nuts, Pollen'),
                                                            'medical_conditions': fields.String(description='Existing medical conditions', required=False, example='Asthma, Hypertension')})

validate_ssn_model = policyholder_ns.model('validate_ssn_model', {'policyholder_id': fields.Integer(description='Unique polciy holder ID', required=True, example=1),
                                                                  'ssn': fields.Integer(description='Social security number', required=True, example=11122333)})


# Policyholder Namespace Routes #
@policyholder_ns.route('/create_insured', doc={"description": "Create a new policy holder"})
class CreateInsured(Resource):
    """
    An endpoint to create a policy holder.

    :return: Unique ID of the new policy holder.
    """
    @policyholder_ns.expect(policyholder_model)
    def post(self):
        gender = policyholder_ns.payload.get('gender')
        date_of_birth = datetime.datetime.strptime(policyholder_ns.payload.get('date_of_birth'), '%m/%d/%Y')
        ssn = str(policyholder_ns.payload.get('ssn'))
        smoking_status = policyholder_ns.payload.get('smoking_status')
        allergies = policyholder_ns.payload.get('allergies')
        medical_conditions = policyholder_ns.payload.get('medical_conditions')

        ssn_hash = pbkdf2_sha256.hash(ssn)

        policyholder = Policyholder(gender=gender, date_of_birth=date_of_birth, ssn_hash=ssn_hash,
                                    smoking_status=smoking_status,
                                    allergies=allergies, medical_conditions=medical_conditions)
        db.session.add(policyholder)
        db.session.commit()
        return jsonify(
            id=policyholder.id
        )


@policyholder_ns.route('/', doc={"description": "Returns all policy holders"})
class Policyholders(Resource):
    """
    An endpoint to retrieve all policy holders.

    :return: List of all policy holders including all metadata.
    """
    @staticmethod
    def get():
        policyholders = Policyholder.query.all()
        return jsonify(
            policyholders=policyholders
        )


@policyholder_ns.route('/<policyholder_id>', doc={"description": "Fetch policy holder by ID"})
@policyholder_ns.doc(params={'policyholder_id': 'Unique policy holder ID'})
class PolicyholderByID(Resource):
    """
    An endpoint to find a policy holder by unique ID.

    :return: policy holder with the associated ID.
    """
    @staticmethod
    def get(policyholder_id):
        policyholder = Policyholder.query.filter_by(id=policyholder_id).one()
        return jsonify(
            policyholder=policyholder
        )


@policyholder_ns.route('/validate_ssn', doc={"description": "Fetch policy holder by ID"})
class ValidatePolicyHolderSSN(Resource):
    """
    An endpoint to validate the policy holder's SSN. Verifies the passed input with the stored hash.

    :return: valid key with either 'true' or 'false'.
    """
    @policyholder_ns.expect(validate_ssn_model)
    def post(self):
        policyholder_id = policyholder_ns.payload.get('policyholder_id')
        ssn = str(policyholder_ns.payload.get('ssn'))

        policyholder = Policyholder.query.filter_by(id=policyholder_id).one()
        if not pbkdf2_sha256.verify(ssn, policyholder.ssn_hash):
            return jsonify(
                valid=False
            )
        return jsonify(
            valid=True
        )

