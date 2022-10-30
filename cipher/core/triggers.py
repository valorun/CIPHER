from cipher.model import db, Trigger as DbTrigger
from cipher.core.sequence_reader import sequence_reader
from . import core

registered_triggers = ['intent_test']

def execute_trigger(trigger_name: str, **kwargs):
    """
    Execute sequences attached to a trigger.
    """
    if trigger_name not in registered_triggers:
        core.log.warning(f"Attempted to execute unregistered trigger '{trigger_name}'")
        return
    db_trigger = DbTrigger.query.filter_by(trigger_name=trigger_name, enabled=True).all()
    for t in db_trigger:
        sequence_reader.launch_sequence(t.sequence_id, **kwargs)