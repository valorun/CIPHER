from cipher.core.actions import speech

def main(**kwargs):
    if 'slots' not in kwargs or len(kwargs['slots']) < 1:
        return

    result = 0
    last_operator = None
    for slot in kwargs['slots']:
        if slot['entity'] == 'snips/number':
            if last_operator is None:
                result = slot['value']['value']
            else:
                if last_operator == '+':
                    result += slot['value']['value']
                elif last_operator == '-':
                    result -= slot['value']['value']
                elif last_operator == '*':
                    result *= slot['value']['value']
                elif last_operator == '/':
                    result /= slot['value']['value']
        elif slot['entity'] == 'operator':
            last_operator = slot['value']['value']

    speech(str(int(result)))