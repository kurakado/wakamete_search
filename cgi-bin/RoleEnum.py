#! python3
from enum import Enum

class Role(Enum):
    MURABITO=1
    KARYUDO=2
    KYOYU=3
    URANAI=4
    REINO=5
    KYOJIN=6
    JINRO=7
    YOUKO=8
    NEKOMATA=9
    TAIRO=10
    KOGITSUNE=11

def returnRole(string):
    if string=="[村　人]":
        return Role.MURABITO
    elif string=="[狩　人]":
        return Role.KARYUDO
    elif string=="[共有者]":
        return Role.KYOYU
    elif string=="[占い師]":
        return Role.URANAI
    elif string=="[霊能者]":
        return Role.REINO
    elif string=="[狂　人]":
        return Role.KYOJIN
    elif string=="[人　狼]":
        return Role.JINRO
    elif string=="[妖　狐]":
        return Role.YOUKO
    elif string=="[子　狐]":
        return Role.KOGITSUNE
    elif string=="[大　狼]":
        return Role.TAIRO
    elif string=="[猫　又]":
        return Role.NEKOMATA

def returnString(role):
    if role==Role.MURABITO:
        return "村人"
    if role==Role.KARYUDO:
        return "狩人"
    if role==Role.KYOYU:
        return "共有者"
    if role==Role.URANAI:
        return "占い師"
    if role==Role.REINO:
        return "霊能者"
    if role==Role.KYOJIN:
        return "狂人"
    if role==Role.JINRO:
        return "人狼"
    if role==Role.YOUKO:
        return "妖狐"
    if role==Role.KOGITSUNE:
        return "子狐"
    if role==Role.TAIRO:
        return "大狼"
    if role==Role.NEKOMATA:
        return "猫又"
