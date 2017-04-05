import mahjongSYK as mjsyk

# def isValid(group):
#     if (len(group.cards) == 3 and
#             (group.mjsyk.type_cal() == 'shunzi' or group.mjsyk.type_cal() == 'kezi')):
#         return True
#     elif(len(group.cards) == 2 and group.mjsyk.type_cal() == 'duizi'):
#         return True
#     else:
#         return False

def hand_check(hand):
    num_mianzi = 0
    num_quetou = 0
    num_cards = 0
    for group in hand.groups:
        num_cards += len(group.cards)
    max_num_mianzi = (int)(num_cards / 3)
    for group in hand.groups:
        type_of_group = group.get_type()
        if type_of_group in mjsyk.MIANZI:
            num_mianzi += 1
        elif type_of_group in mjsyk.QUETOU and num_quetou < 1:
            num_quetou += 1
    if num_mianzi == max_num_mianzi and num_quetou == 1:
        return True
    else:
        return False


