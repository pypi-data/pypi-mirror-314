from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class AlertSignalPresence(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ALERT_SIGNAL_PRESENCE_ON: _ClassVar[AlertSignalPresence]
    ALERT_SIGNAL_PRESENCE_OFF: _ClassVar[AlertSignalPresence]
    ALERT_SIGNAL_PRESENCE_LATCH: _ClassVar[AlertSignalPresence]
    ALERT_SIGNAL_PRESENCE_ACK: _ClassVar[AlertSignalPresence]

class AlertConditionEscalationProcess(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ALERT_CONDITION_ESCALATION_PROCESS_START_ESCALATION: _ClassVar[AlertConditionEscalationProcess]
    ALERT_CONDITION_ESCALATION_PROCESS_STOP_ESCALATION: _ClassVar[AlertConditionEscalationProcess]
    ALERT_CONDITION_ESCALATION_PROCESS_START_DEESCALATION: _ClassVar[AlertConditionEscalationProcess]
    ALERT_CONDITION_ESCALATION_PROCESS_STOP_DEESCALATION: _ClassVar[AlertConditionEscalationProcess]
ALERT_SIGNAL_PRESENCE_ON: AlertSignalPresence
ALERT_SIGNAL_PRESENCE_OFF: AlertSignalPresence
ALERT_SIGNAL_PRESENCE_LATCH: AlertSignalPresence
ALERT_SIGNAL_PRESENCE_ACK: AlertSignalPresence
ALERT_CONDITION_ESCALATION_PROCESS_START_ESCALATION: AlertConditionEscalationProcess
ALERT_CONDITION_ESCALATION_PROCESS_STOP_ESCALATION: AlertConditionEscalationProcess
ALERT_CONDITION_ESCALATION_PROCESS_START_DEESCALATION: AlertConditionEscalationProcess
ALERT_CONDITION_ESCALATION_PROCESS_STOP_DEESCALATION: AlertConditionEscalationProcess
