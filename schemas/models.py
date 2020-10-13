import datetime

from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()


# Database Models
@dataclass
class Policyholder(db.Model):
    """Policyholder model"""
    __tablename__ = 'policyholder'

    id: int
    gender: str
    date_of_birth: datetime
    # Omit ssn_hash from response object
    # ssn_hash: str
    smoking_status: bool
    allergies: str
    medical_conditions: str
    insured_events: "InsuredEvent"

    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String, unique=False, nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    ssn_hash = db.Column(db.String, unique=False, nullable=False)
    smoking_status = db.Column(db.Boolean)
    allergies = db.Column(db.String)
    medical_conditions = db.Column(db.String)
    insured_events = relationship("InsuredEvent")

    def __repr__(self):
        return '<Policyholder ID %r>' % self.id


@dataclass
class InsuredEvent(db.Model):
    """InsuredEvent model"""
    __tablename__ = 'insured_event'

    id: int
    date_of_incidence: datetime
    billed_amount: float
    covered_amount: float
    type_of_issue: str
    policyholder_id: int

    id = db.Column(db.Integer, primary_key=True)
    date_of_incidence = db.Column(db.DateTime, nullable=False)
    billed_amount = db.Column(db.Float, nullable=False)
    covered_amount = db.Column(db.Float, nullable=False)
    type_of_issue = db.Column(db.String)
    policyholder_id = Column(Integer, ForeignKey('policyholder.id'))

    def __repr__(self):
        return '<InsuredEvent ID %r>' % self.id


# Other data structures
class AggregatedMetrics(object):
    def __init__(self, covered_amount: float, average_age: float, claims: int):
        self.covered_amount = covered_amount
        self.average_age = average_age
        self.claims = claims
