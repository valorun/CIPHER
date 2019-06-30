from cipher.core.sequence_reader import sequence_reader

def getSequenceName(slots):
    sequence_name = ''
    member = None
    movement = None
    direction = None
    chosen_duplicated_member = None
    for slot in slots:
        if slot['slotName'] == 'member':
            member = slot['value']['value']
        elif slot['slotName'] == 'movement':
            movement = slot['value']['value']
        elif slot['slotName'] == 'direction':
            direction = slot['value']['value']
        elif slot['slotName'] == 'chosen_duplicated_member':
            chosen_duplicated_member = slot['value']['value']
    if movement is None:
       return None
    else:
        sequence_name += movement
    if member is not None:
        sequence_name += '_' + member
    if chosen_duplicated_member is not None:
        sequence_name += '_' + chosen_duplicated_member
    if direction is not None:
        sequence_name += '_' + direction
    return sequence_name

def main(**kwargs):
    if 'slots' not in kwargs or len(kwargs['slots']) < 1:
        return

    sequence_name = getSequenceName(kwargs['slots'])
    if sequence_name is not None:
        sequence_reader.launchSequence(sequence_name)