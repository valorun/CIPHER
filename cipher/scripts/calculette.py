from cipher.core.actions import SpeechAction


def main(**kwargs):
    if 'slots' not in kwargs or len(kwargs['slots']) < 1:
        return

    result = None
    last_operator = None
    for slot in kwargs['slots']:
        if slot['entity'] == 'snips/number':
            if last_operator is None:
                if result is None:
                    result = slot['value']['value']
                else:
                    SpeechAction("Il semble que l'opération demandée n'est pas valide").execute()
                    return False  # calcul invalide, deux opérandes successifs
            else:
                if last_operator == '+':
                    result += slot['value']['value']
                elif last_operator == '-':
                    result -= slot['value']['value']
                elif last_operator == '*':
                    result *= slot['value']['value']
                elif last_operator == '/':
                    result /= slot['value']['value']
                last_operator = None
        elif slot['entity'] == 'operator':
            if last_operator is None:
                if result is None:
                    SpeechAction("Il semble que l'opération demandée n'est pas valide").execute()
                    return False  # calcul invalide, commence par un opérateur
                last_operator = slot['value']['value']
            else:
                SpeechAction("Il semble que l'opération demandée n'est pas valide").execute()
                return False  # calcul invalide, deux opérateurs successifs
        else:
            SpeechAction("Il semble que l'opération demandée n'est pas valide").execute()
            return False

    SpeechAction(str(int(result))).execute()
    return True
