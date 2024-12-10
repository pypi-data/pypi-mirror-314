from sqlalchemy import String, Column, DateTime, Float, Integer
from sqlalchemy.orm import relationship
from .sap_model import SapBonanzaBase as SBB


class Activity(SBB):
    __tablename__ = 'sap_activity'

    ActivityCode = Column('ActivityCode', Integer, primary_key=True)
    CardCode = Column('CardCode', String)
    Notes = Column('Notes', String, nullable=True)
    ActivityDate = Column('ActivityDate', DateTime)
    ActivityTime = Column('ActivityTime', String)
    StartDate = Column('StartDate', DateTime)
    Closed = Column('Closed', String)
    CloseDate = Column('CloseDate', DateTime, nullable=True)
    Phone = Column('Phone', String)
    Fax = Column('Fax', String, nullable=True)
    Subject = Column('Subject', Integer)
    DocType = Column('DocType', String)
    DocNum = Column('DocNum', String, nullable=True)
    DocEntry = Column('DocEntry', String, nullable=True)
    Priority = Column('Priority', String)
    Details = Column('Details', String, nullable=True)
    Activity = Column('Activity', String)
    ActivityType = Column('ActivityType', Integer)
    Location = Column('Location', Integer)
    StartTime = Column('StartTime', String)
    EndTime = Column('EndTime', String)
    Duration = Column('Duration', Float)
    DurationType = Column('DurationType', String)
    SalesEmployee = Column('SalesEmployee', Integer)
    ContactPersonCode = Column('ContactPersonCode', Integer)
    HandledBy = Column('HandledBy', Integer)
    Reminder = Column('Reminder', String)
    ReminderPeriod = Column('ReminderPeriod', Float)
    ReminderType = Column('ReminderType', String)
    City = Column('City', String, nullable=True)
    PersonalFlag = Column('PersonalFlag', String)
    Street = Column('Street', String, nullable=True)
    ParentObjectId = Column('ParentObjectId', String, nullable=True)
    ParentObjectType = Column('ParentObjectType', String, nullable=True)
    Room = Column('Room', String, nullable=True)
    InactiveFlag = Column('InactiveFlag', String)
    State = Column('State', String, nullable=True)
    PreviousActivity = Column('PreviousActivity', String, nullable=True)
    Country = Column('Country', String, nullable=True)
    Status = Column('Status', String, nullable=True)
    TentativeFlag = Column('TentativeFlag', String)
    EndDueDate = Column('EndDueDate', DateTime)
    DocTypeEx = Column('DocTypeEx', String)
    AttachmentEntry = Column('AttachmentEntry', String, nullable=True)
    RecurrencePattern = Column('RecurrencePattern', String)
    EndType = Column('EndType', String)
    SeriesStartDate = Column('SeriesStartDate', DateTime)
    SeriesEndDate = Column('SeriesEndDate', DateTime, nullable=True)
    MaxOccurrence = Column('MaxOccurrence', Integer)
    Interval = Column('Interval', Integer)
    Sunday = Column('Sunday', String)
    Monday = Column('Monday', String)
    Tuesday = Column('Tuesday', String)
    Wednesday = Column('Wednesday', String)
    Thursday = Column('Thursday', String)
    Friday = Column('Friday', String)
    Saturday = Column('Saturday', String)
    RepeatOption = Column('RepeatOption', String)
    BelongedSeriesNum = Column('BelongedSeriesNum', String, nullable=True)
    IsRemoved = Column('IsRemoved', String)
    AddressName = Column('AddressName', String, nullable=True)
    AddressType = Column('AddressType', String)
    HandledByEmployee = Column('HandledByEmployee', String, nullable=True)
    RecurrenceSequenceSpecifier = Column('RecurrenceSequenceSpecifier', String, nullable=True)
    RecurrenceDayInMonth = Column('RecurrenceDayInMonth', Integer, nullable=True)
    RecurrenceMonth = Column('RecurrenceMonth', Integer, nullable=True)
    RecurrenceDayOfWeek = Column('RecurrenceDayOfWeek', String, nullable=True)
    SalesOpportunityId = Column('SalesOpportunityId', Integer, nullable=True)
    SalesOpportunityLine = Column('SalesOpportunityLine', Integer, nullable=True)
    HandledByRecipientList = Column('HandledByRecipientList', String, nullable=True)
    Office365EventId = Column('Office365EventId', String, nullable=True)
    DataVersion = Column('DataVersion', Integer)

    def __repr__(self):
        return f"<Activity(activity_code='{self.ActivityCode}', card_code='{self.CardCode}')>"


class ActivityType(SBB):
    __tablename__ = 'sap_activity_type'

    Code = Column('Code', Integer,primary_key=True)
    Name = Column('Name' , String)

    def __repr__(self):
        return f"<ActivityType(activity_type='{self.Code}', activity_name='{self.Name}')>"




