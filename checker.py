# -*- coding: utf-8 -*-
# Author: Frank-the-Obscure @ GitHub
# mahjong basic module

import re
import random

class Card:
    def __init__(self, card):
        super(Card, self).__init__()
        self.suit = re.search('[mpsz]', card).group()       #m:筒 p:索 s:万 z:字
        if self.suit is 'z':
            self.rank = int(re.search('[1-7]', card).group())
        else:
            self.rank = int(re.search('[1-9]', card).group())

    def __str__(self):
        return str(self.rank) + self.suit

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def set_flag(self, flag):
        self.flag = flag

MIANZI = ['shunzi', 'kezi']
QUETOU = ['duizi']
DAZI = ['duizi', 'bianzhang', 'kanzhang', 'liangmian']
GUZHANG = ['guzhang'] # init respones

CARD_LIST = [str(rank) + suit
             for suit in ['m', 'p', 's', 'z']
             for rank in range(1, 10)
             if rank in range(1, 8) or suit is not 'z']

CARD_LEFT = {card:4 for card in CARD_LIST}      #syk??

def init_paishan():
    """ 生成136张牌山
    i: nothing
    o: a list of 136 random card
    """
    paishan_list = CARD_LIST * 4
    random.shuffle(paishan_list)
    return paishan_list

def used_card(card):            #删去已使用的牌
    CARD_LEFT[str(card)] -= 1

VALID_LENGTH_OF_HAND = 14
MIANZI_MAX = 4
QUETOU_MAX = 1
XIANGTINGSHU_MAX = 8
finished_hand = []      #use this list for storing finished hand after iteration

class Mianzi(object):
    """docstring for Mianzi"""
    def __init__(self, card1, card2, card3):
        super(Mianzi, self).__init__()

        self.card1 = card1
        self.card2 = card2
        self.card3 = card3
        self.index = card1.rank

    def __str__(self):
        if self.isvalid():
            return str(self.card1) + str(self.card2) + str(self.card3)
        else:
            return 'not valid!'

    def isvalid(self):
        if(self.card1.suit == self.card2.suit == self.card3.suit):
            if(self.card1.rank == self.card2.rank - 1 and
               self.card2.rank == self.card3.rank - 1 and
               self.card1.suit is not 'z'):  # 顺子不能是字牌
                return True
            elif(self.card1.rank == self.card2.rank and
                  self.card1.rank == self.card3.rank):
                return True
        else:
            return False

class Quetou(object):
    """docstring for Quetou"""
    def __init__(self, card1, card2):
        super(Quetou, self).__init__()

        self.card1 = card1
        self.card2 = card2
        self.index = card1.rank

    def __str__(self):
        if self.isvalid():
            return str(self.card1) + str(self.card2)
        else:
            return 'not valid'

    def isvalid(self):
        if(self.card1.suit == self.card2.suit and
           self.card1.rank == self.card2.rank):
            return True
        else:
            return False

def hand_checker(hand, mianzi_needed = MIANZI_MAX, quetou_needed = QUETOU_MAX):
    """iterator for standard form"""
    global finished_hand
    finished_hand = []
    if mianzi_needed == 1 and len(hand) ==  3:
        if Mianzi(hand[0], hand[1], hand[2]).isvalid():
            finished_hand.append(Mianzi(hand[0], hand[1], hand[2]))
        return Mianzi(hand[0], hand[1], hand[2]).isvalid()
    if quetou_needed == 1 and len(hand) == 2:
        if Quetou(hand[0], hand[1]).isvalid():
            finished_hand.append(Quetou(hand[0], hand[1]))
        return Quetou(hand[0], hand[1]).isvalid()

    i = 0
    j = i + 1
    k = j + 1
    while j < len(hand):
        #先尝试雀头
        if quetou_needed and Quetou(hand[i], hand[j]).isvalid():
            iter_hand = hand[:]         #create a copy
            del iter_hand[j]
            del iter_hand[i]
            if hand_checker(iter_hand, mianzi_needed, quetou_needed - 1):       #递归迭代计算
                finished_hand.append(Quetou(hand[i], hand[j]))
                return hand
            else:
                pass
        while k < len(hand):
            if Mianzi(hand[i], hand[j], hand[k]).isvalid():
                iter_hand = hand[:]
                del iter_hand[k]
                del iter_hand[j]
                del iter_hand[i]
                if hand_checker(iter_hand, mianzi_needed - 1, quetou_needed):
                    finished_hand.append(Mianzi(hand[i], hand[j], hand[k]))
                    return hand
                else:
                    k += 1
            else:
                k += 1
        else:                       #syk??
            j += 1  # j变化时, 要重置k的值
            k = j + 1
    return None

def non_standard_form(hand, mianzi_needed = MIANZI_MAX, quetou_needed = QUETOU_MAX):
    global finished_hand
    finished_hand = []

    if mianzi_needed == MIANZI_MAX and quetou_needed == QUETOU_MAX:
        i = 0;
        flag = True
        while i < len(hand) - 1:
            if not Quetou(hand[i], hand[i + 1]).isvalid():
                flag = False
                break
            finished_hand.append(Quetou(hand[i], hand[i + 1]))
            i += 2
        if flag:
            return True
        yaojiu = hand_processer('19m19p19s1234567z')           ##syk??
        shisanyao = [sorted(yaojiu + [card], key = sort_hand)
                     for card in yaojiu]
        for shisanyao_hand in shisanyao:
            if issamehand(shisanyao_hand, hand):
                finished_hand = shisanyao_hand
                return True
    else:
        return

def print_hand(hand):
    for card in hand:
        print(card, end = '')
    print()

def issamehand(hand1, hand2):
    if len(hand1) != len(hand2):
        return False
    else:
        i = 0
        while i < len(hand1):
            if not is_samecard(hand1[i], hand2[i]):
                return False
            i += 1
        return True

def is_samecard(card1, card2):
    return str(card1) == str(card2)

def hand_processer(hand, raw_hand = True, length = VALID_LENGTH_OF_HAND, check_input = False):
    if not raw_hand:
        hand.sort(key = sort_hand)
        return hand
    processed_hand = []
    for split in re.findall('[1-9]+[mpsz]', hand):        ##将麻将牌形式标准化
        suit = re.search('[mpsz]', split).group()
        ranks = re.findall('[1-9]', split)
        for rank in ranks:
            processed_hand.append(rank + suit)
    if len(processed_hand) != length and check_input:       ##syk??check_input??
        return None
    hand_in_class = [Card(card) for card in processed_hand]
    hand_in_class.sort(key = sort_hand)
    return hand_in_class

def sort_hand(card):
    return card.get_suit(), card.get_rank()

def mahjong_checker(hand, output_notes = False, raw_hand = True):
    global finished_hand
    finished_hand = []

    if raw_hand:
        hand = hand_processer(hand, check_input = True)
    if hand:
        if non_standard_form(hand):
            if output_notes:
                print('Hand is mahjong. Wining hand is: ')
                for i in format_finished_hand(finished_hand, 'qiduizi'):
                    print(i, end = ' ')                     ##syk??
                print()
            return True
        else:
            finished_hand = []      #re init
        if hand_checker(hand):
            if output_notes:
                print('Hand is mahjong. Wining hand is: ')
                for i in format_finished_hand(finished_hand):
                    print(i, end=' ')
                print()
                # print_hand(hand)
            return True
        else:
            print('Hand is not valid.')
            return False

def format_finished_hand(finished_hand, kind = 'standard'):     ##面子在前，雀头在后
    if kind is not 'standard':
        return finished_hand
    else:
        finished_hand.reverse()
        for hand_set in finished_hand:
            if type(hand_set) == Quetou:
                quetou = hand_set
                finished_hand.remove(hand_set)
        finished_hand.append(quetou)
        return finished_hand

def main():
    from sys import argv
    try:
        script, input_hand = argv
    except ValueError:
        input_hand = input('input hand: ')
    mahjong_checker(input_hand, output_notes = True)

if __name__ == '__main__':              ##syk??
    main()
