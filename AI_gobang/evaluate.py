def judge_5(checklist):
    # 五连
    num = 0
    for i in range(5):
        if checklist[i] == checklist[i + 1] == checklist[i + 2] == checklist[i + 3] == checklist[i + 4] == checklist[4]:
            num += 1
    return num


def judge_live4(checklist):
    # 活四
    num = 0
    for i in range(1, 5):
        if checklist[i - 1] == checklist[i + 4] == 0 and \
                checklist[i] == checklist[i + 1] == checklist[i + 2] == checklist[i + 3] == checklist[4]:
            num += 1
    return num


def judge_chong4(checklist):
    pass


def judge_live3(checklist):
    pass
