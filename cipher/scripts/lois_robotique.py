from cipher.core.actions import speech

lois = [
    "un robot ne peut porter atteinte à un être humain, ni, en restant passif, permettre qu'un être humain soit exposé au danger",
    "un robot doit obéir aux ordres qui lui sont donnés par un être humain, sauf si de tels ordres entrent en conflit avec la première loi ",
    "un robot doit protéger son existence tant que cette protection n'entre pas en conflit avec la première ou la deuxième loi"
]
def main(**kwargs):
    if 'slots' not in kwargs or len(kwargs['slots']) < 1:
        for loi in lois:
            speech(loi)
        return True


    selected_lois = []
    for slot in kwargs['slots']:
        number = slot['value']['value']
        if number > 0 and number < 4:
            if number not in selected_lois:
                selected_lois.append(number)
        else:
            speech("Cette loi n'existe pas")
            return False

    for number in selected_lois:
        speech(lois[number-1])

    return True
