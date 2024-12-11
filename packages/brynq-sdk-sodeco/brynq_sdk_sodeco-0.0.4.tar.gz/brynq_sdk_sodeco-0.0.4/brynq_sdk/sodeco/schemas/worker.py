from pandera import DataFrameModel, Field, Column
from typing import Optional
from datetime import datetime
import re

class WorkerSchema(DataFrameModel):
    # Required fields
    Name: str = Field(nullable=False, str_length={'min_value': 0, 'max_value': 40})
    Firstname: str = Field(nullable=False, str_length={'min_value': 0, 'max_value': 25})
    
    # Optional fields with specific validations
    INSS: Optional[float] = Field(nullable=True, ge=0.0, le=99999999999.0)
    Sex: Optional[str] = Field(nullable=True, isin=['M', 'F'])
    Birthdate: Optional[str] = Field(nullable=True, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')
    BirthplaceZIPCode: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 12})
    Birthplace: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 30})
    BirthplaceCountry: Optional[str] = Field(nullable=True, str_length={'min_value': 5, 'max_value': 5}, regex=r'^[0-9]*$', default='00150')
    Nationality: Optional[str] = Field(nullable=True, str_length={'min_value': 5, 'max_value': 5}, regex=r'^[0-9]*$', default='00150')
    Language: Optional[str] = Field(nullable=True, isin=['N', 'F', 'D', 'E'])
    PayWay: Optional[str] = Field(nullable=True, isin=['Cash', 'Transfer', 'Electronic', 'AssignmentList'])
    BankAccount: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 45})
    BICCode: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 15})
    ID: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 15})
    IDType: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 3})
    IDValidUntil: Optional[str] = Field(nullable=True, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')
    DriverLicense: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 15})
    DriverCategory: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 2})
    NumberPlate: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 10})
    FuelCard: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 20})
    Education: Optional[str] = Field(nullable=True, isin=[
        'Basic', 'LowerSecondary', 'HigherSecondary', 'NotUniversity',
        'University', 'Secondary1Degree', 'Secondary2Degree', 'Secondary3Degree', 'Unknown'
    ])
    Profession: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 50})
    EHealthInsurance: Optional[int] = Field(nullable=True, ge=0, le=9999)
    EHealthInsuranceReference: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 20})
    AccidentInsurance: Optional[int] = Field(nullable=True, ge=0, le=9999)
    MedicalCenter: Optional[int] = Field(nullable=True, ge=0, le=9999)
    MedicalCenterReference: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 15})
    ExternalID: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 50})
    InterimFrom: Optional[str] = Field(nullable=True, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')
    InterimTo: Optional[str] = Field(nullable=True, str_length={'min_value': 8, 'max_value': 8}, regex=r'^[0-9]*$')
    TravelExpenses: Optional[str] = Field(nullable=True, isin=[
        'PublicTransportTrain', 'OwnTransport', 'PublicTransportOther', 'Bicycle', 'None'
    ])
    TypeOfTravelExpenses: Optional[str] = Field(nullable=True, isin=[
        'Other', 'PublicCommonTransport', 'OrganisedCommonTransport'
    ])
    SalaryCodeTravelExpenses: Optional[int] = Field(nullable=True, ge=1, le=9999)
    MainDivision: Optional[str] = Field(nullable=True, str_length={'min_value': 0, 'max_value': 10})

    class Config:
        strict = True
        coerce = True
