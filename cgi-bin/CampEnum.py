#! python3
from enum import Enum

class Camp(Enum):
    MURA=1
    JINRO=2
    YOUKO=3

def returnCamp(string):
    if string=='「村\u3000人」の勝利です！':
        return Camp.MURA
    elif string=='「人\u3000狼」の勝利です！':
        return Camp.JINRO
    elif string=='「妖\u3000狐」の勝利です！':
        return Camp.YOUKO

def returnStringCamp(role):
    if role==Camp.MURA:
        return "村人"
    if role==Camp.JINRO:
        return "人狼"
    if role==Camp.YOUKO:
        return "妖狐"
