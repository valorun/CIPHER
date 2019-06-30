#from cipher.core.actions import speech

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

    print(str(int(result)))

args = {}
s1 = {}
s1['entity'] = 'snips/number'
s1['value'] = {}
s1['value']['value'] = 2.0

s2 = {}
s2['entity'] = 'operator'
s2['value'] = {}
s2['value']['value'] = '+'

s3 = {}
s3['entity'] = 'snips/number'
s3['value'] = {}
s3['value']['value'] = 3.0

s4 = {}
s4['entity'] = 'operator'
s4['value'] = {}
s4['value']['value'] = '*'

s5 = {}
s5['entity'] = 'snips/number'
s5['value'] = {}
s5['value']['value'] = 2.0

args['slots'] = [s1, s2, s3, s4, s5]
main(**args)