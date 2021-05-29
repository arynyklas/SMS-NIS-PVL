# -*- coding: utf-8 -*-


def get_actual_year(reponse: list) -> dict:
    for item in reponse:
        if item['Data']['IsActual']:
            return item

def score_to_mark(score: float) -> int:
    temp = round(score)

    if temp >= 85 and temp <= 100:
        return 5
    elif temp >= 65 and temp <= 84:
        return 4
    elif temp >= 40 and temp <= 64:
        return 3
    else:
        return 2
