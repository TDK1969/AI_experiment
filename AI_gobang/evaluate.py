def judge_5(checklist, player):
    # 五连
    num = 0
    for i in range(5):
        if checklist[i] == checklist[i + 1] == checklist[i + 2] == checklist[i + 3] == checklist[i + 4] == player:
            num += 1
    return num


def judge_live4(checklist, player):
    # 活四
    num = 0
    for i in range(1, 5):
        if checklist[i - 1] == checklist[i + 4] == 0 and \
                checklist[i] == checklist[i + 1] == checklist[i + 2] == checklist[i + 3] == player:
            num += 1
    return num


def judge_chong4(checklist, player):
    """
    冲四
    :param checklist: 棋子列表
    :return: 冲四的数量
    """
    num = 0
    for i in range(5):
        flag = True
        empty = 0
        for j in range(i, i + 5):
            if checklist[j] == 0:
                empty += 1
            elif checklist[j] != player:
                flag = False
                break
        if empty == 1 and flag:
            num += 1
    return num


def judge_live3(checklist, player):
    """
    活三
    :param checklist: 长度为9的棋子列表
    :return: 活三的数量
    """
    num = 0
    for i in range(5):
        cnt = 0
        for j in range(i, i + 5):
            if checklist[j] == 0:
                cnt += 1
            elif checklist[j] != player:
                break
        if cnt == 2 and checklist[i + 1] == checklist[i + 3] and \
                (checklist[i + 1] == player or checklist[i + 3] == player):
            num += 1
    return num


def judge_sleep3(checklist, player, enemy):
    """
    眠三
    :param checklist:
    :param player:
    :param enemy:
    :return:
    """
    num = 0
    for k in range(2):
        checklist.reverse()
        for i in range(1, 5):
            cnt = 0
            if checklist[i - 1] == enemy or checklist[i - 1] == -1:
                for j in range(i, i + 5):
                    if checklist[j] == 0:
                        cnt += 1
                    elif checklist[j] != player:
                        break
                if cnt == 2 and checklist[i + 1] == checklist[i + 3] and \
                        (checklist[i + 1] == player or checklist[i + 3] == player):
                    num += 1
    return num


def judge_lian2(checklist, player):
    """
    连二
    :param checklist:
    :param player:
    :return:
    """
    num = 0
    if checklist[1] == checklist[2] == checklist[5] == checklist[6] == 0 and checklist[3] == checklist[4] == player:
        num += 1
    if checklist[2] == checklist[3] == checklist[6] == checklist[7] == 0 and checklist[4] == checklist[5] == player:
        num += 1
    return num


def judge_jump2(checklist, player):
    """
    跳二
    :param checklist:
    :param player:
    :return:
    """
    num = 0
    if checklist[1] == checklist[3] == checklist[5] == 0 and checklist[2] == checklist[4] == player:
        num += 1
    if checklist[3] == checklist[5] == checklist[7] == 0 and checklist[4] == checklist[6] == player:
        num += 1
    return num


def judge_bigjump2(checklist, player):
    """
    大跳二
    :param checklist:
    :param player:
    :return:
    """
    num = 0
    if checklist[0] == checklist[2] == checklist[3] == checklist[5] == 0 and checklist[1] == checklist[4] == player:
        num += 1
    if checklist[3] == checklist[5] == checklist[6] == checklist[8] == 0 and checklist[4] == checklist[7] == player:
        num += 1
    return num


def judge_sleep2(checklist, player, enemy):
    num = 0
    for i in range(2):
        checklist.reverse()
        if (checklist[2] == enemy or checklist[2] == -1) and checklist[3] == checklist[4] == player and \
                checklist[5] == checklist[6] == 0:
            num += 1
        if (checklist[3] == enemy or checklist[3] == -1) and checklist[4] == checklist[5] == player and \
                checklist[6] == checklist[7] == 0:
            num += 1
        if (checklist[1] == enemy or checklist[1] == -1) and checklist[2] == checklist[4] == player and \
                checklist[3] == checklist[5] == 0:
            num += 1
        if (checklist[3] == enemy or checklist[3] == -1) and checklist[6] == checklist[4] == player and \
                checklist[5] == checklist[7] == 0:
            num += 1
        if (checklist[3] == enemy or checklist[3] == -1) and checklist[4] == checklist[7] == player and \
                checklist[5] == checklist[6] == 0:
            num += 1
        if (checklist[0] == enemy or checklist[0] == -1) and checklist[1] == checklist[4] == player and \
                checklist[2] == checklist[3] == 0:
            num += 1
    return num


def TDK_value(player, enemy, list1, list2, list3, list4):
    # 敌之要点乃我之要点
    value = 0
    for i in range(2):
        tempValue = 0
        player, enemy = enemy, player
        list1[4] = list2[4] = list3[4] = list4[4] = player
        five_num = judge_5(list1, player) + judge_5(list2, player) + judge_5(list3, player) + judge_5(list4, player)
        five_value = 10000000 * five_num

        live4_num = judge_live4(list1, player) + judge_live4(list2, player) + judge_live4(list3, player) + \
                    judge_live4(list4, player)
        live4_value = 1000000 * live4_num

        chong4_num = judge_chong4(list1, player) + judge_chong4(list2, player) + judge_chong4(list3, player) + \
                     judge_chong4(list4, player)
        chong4_value = 100000 * chong4_num

        live3_num = judge_live3(list1, player) + judge_live3(list2, player) + judge_live3(list3, player) + \
                    judge_live3(list4, player)
        live3_value = 80000 * live3_num

        sleep3_num = judge_sleep3(list1, player, enemy) + judge_sleep3(list2, player, enemy) + \
                     judge_sleep3(list3, player, enemy) + judge_sleep3(list4, player, enemy)
        sleep3_value = 10000 * sleep3_num

        lian2_num = judge_lian2(list1, player) + judge_lian2(list2, player) + judge_lian2(list3, player) + \
                    judge_lian2(list4, player)
        lian2_value = 3000 * lian2_num

        jump2_num = judge_jump2(list1, player) + judge_jump2(list2, player) + judge_jump2(list3, player) + \
                    judge_jump2(list4, player)
        jump2_value = 1500 * jump2_num

        bigjump2_num = judge_bigjump2(list1, player) + judge_bigjump2(list2, player) + \
                       judge_bigjump2(list3, player) + judge_bigjump2(list4, player)
        bigjump2_value = 1000 * bigjump2_num

        sleep2_num = judge_sleep2(list1, player, enemy) + judge_sleep2(list2, player, enemy) + \
                     judge_sleep2(list3, player, enemy) + judge_sleep2(list4, player, enemy)
        sleep2_value = 500 * sleep2_num

        tempValue = five_value + live4_value + chong4_value + live3_value + sleep3_value + \
                    lian2_value + jump2_value + bigjump2_value + sleep2_value

        if chong4_num and live3_num or live3_num >= 2:
            tempValue += 1000000

        value += tempValue

    return value