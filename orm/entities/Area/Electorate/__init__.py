from sqlalchemy.ext.associationproxy import association_proxy

from app import db
from sqlalchemy.orm import relationship, synonym
from orm.enums import ElectorateTypeEnum, AreaTypeEnum, AreaCategoryEnum
from orm.entities import Election, Area
from sqlalchemy.ext.hybrid import hybrid_property
from util import get_paginated_query


class ElectorateModel(Area.Model):
    electorateId = synonym("areaId")
    electorateName = synonym("areaName")
    electorateType = synonym("areaType")

    def __init__(self, electorateName, electorateType, electionId):
        super(ElectorateModel, self).__init__(
            areaName=electorateName,
            areaType=electorateType,
            electionId=electionId
        )

    __mapper_args__ = {
        'polymorphic_identity': AreaTypeEnum.Electorate,
        'polymorphic_on': "areaType"
    }


Model = ElectorateModel


def create(electorateName, electorateType, electionId):
    result = Model(
        electorateName=electorateName,
        electorateType=electorateType,
        electionId=electionId
    )

    return result


def get_all(electorateName=None, electionId=None, electorateType=None):
    query = Model.query

    if electorateName is not None:
        query = query.filter(Model.areaName.like(electorateName))

    if electionId is not None:
        query = query.filter(Model.electionId == electionId)

    if electorateType is not None:
        query = query.filter(Model.areaType == electorateType)

    result = query.all()

    return result