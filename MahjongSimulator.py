import MahjongSYK as mjsyk

input_hand = []
mahjongflag = 0     ##胡牌标识
OPERATION = ['mahjong', 'peng', 'gang', 'skip']

def openGame():
    global input_hand
    mjsyk.init_paishan()
    # myfile = open("input.txt")
    # input_hand = myfile.read()
    input_hand = []
    for i in range(0, 13):      #先抽13张牌
        input_hand.append(mjsyk.getCard_paishan())
    mjsyk.hand_processer(input_hand, raw_hand=False)
    print('Game begin, the hand cards are: ', end = '')
    mjsyk.print_hand(input_hand)

def ProGame_my_round():
    global input_hand, mahjongflag
    checkcard = mjsyk.getCard_paishan()
    print('the card I get is: ', str(checkcard))
    input_hand.append(checkcard)
    flag = mjsyk.mahjong_check(input_hand, raw_hand=False)

    """检测是否有暗刻并进行相应操作"""
    numcount = 0
    max_numcount = 0
    max_numcount_index = 0
    for i in range(1, len(input_hand)):
        if mjsyk.is_samecard(input_hand[i - 1], input_hand[i]):
            numcount += 1
        else:
            if max_numcount < numcount:
                max_numcount = numcount
                max_numcount_index = i
            numcount = 0
    if max_numcount < numcount:
        max_numcount = numcount
        max_numcount_index = len(input_hand) - 1

    if max_numcount == 4:
        print('Can make anke. Anke:1   Skip:Press and other key')
        print('Your choice:')
        flag = input()
        if flag == 1:
            card0 = input_hand[max_numcount_index]
            for i in range(0, len(input_hand)):
                if mjsyk.is_samecard(card0, input_hand[i]):
                    del input_hand[i + 3]
                    del input_hand[i + 2]
                    del input_hand[i + 1]
                    del input_hand[i]
                    break
            return 'anke'
            # for card in input_hand:
            #     if mjsyk.is_samecard(card, card0):
            #         input_hand.remove(card)
            #         numcount += 1
            #         if numcount == 4:
            #             ProGame_my_round()
    # print('Is mahjong?', flag)

    if not flag:
        mjsyk.xiangtingshu_output(input_hand, raw_hand=False)
        card0 = input('打哪一张: ')
        for i in range(0, len(input_hand)):
            if card0 == str(input_hand[i]):
                del input_hand[i]
                break
        # for card in input_hand:
        #     if card0 == str(card):
        #         input_hand.remove(card)
        mjsyk.hand_processer(input_hand, raw_hand=False)
        print('手牌: ', end = '')
        mjsyk.print_hand(input_hand)
        return 'skip'
    else:
        mahjongflag = 1
        return 'mahjong'

def ProGame_other_round():
    global input_hand
    checkcard = mjsyk.getCard_paishan()
    print('the card other player puts is: ', str(checkcard))
    num_samecount = mjsyk.operation_check(input_hand, checkcard = checkcard)
    if num_samecount == 2:      ##可碰
        print('Peng:1   Skip:Press and other key')
    elif num_samecount == 3:    ##可杠
        print('Peng:1   Gang:2   Skip:Press and other key')
    else:
        print('Skip')
        return 'skip'
    flag = int(input('Your choice:'))
    """碰牌与杠牌操作"""
    if (num_samecount == 2 or num_samecount == 3) and flag == 1:
        mjsyk.peng_handingroup(input_hand, checkcard)
        card0 = input('打哪一张: ')
        for i in range(0, len(input_hand)):
            if card0 == str(input_hand[i]):
                del input_hand[i]
                return 'peng'
        # for card in input_hand:
        #     if card0 == str(card):
        #         input_hand.remove(card)
    elif num_samecount == 3 and flag == 2:
        mjsyk.gang_handingroup(input_hand, checkcard)
        return 'gang'
    else:
        return 'skip'
    # return True         ##表示进入我的回合ProGame_my_round()或已经胡牌
        # ProGame_my_round()



def main():
    openGame()
    flag = ''
    while mahjongflag == 0:
        flag = ProGame_my_round()
        if flag == 'mahjong':
            break
        elif flag == 'anke':
            continue
        i = 0
        while i < 3:
            flag = ProGame_other_round()
            print('sykdebug i = ', i)
            print('sykdebug flag = ', flag)
            if flag == 'peng':
                i = 0
                continue
            elif flag == 'gang':
                break
            i += 1

        # for i in range(0, 3):       #for循环使用了迭代器，不能直接修改循环变量
        #     flag = ProGame_other_round()
        #     print('sykdebug i = ', i)
        #     print('sykdebug flag = ', flag)
        #     if flag == 'peng':
        #         i = -1
        #     elif flag == 'gang':
        #         break

    print('mahjong!! Game is over.')
if __name__ == '__main__':
    main()