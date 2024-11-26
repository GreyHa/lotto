from module.lotto import lotto
from module.common import json_dump, json_load

Lotto = lotto()
'''
데이터 베이스를 구성하여 데이터를 캐시

Lotto.__연금복권_보정_값__(data=보정데이터)
Lotto.__로또_보정_값__(data=보정데이터)

# {회차: 당첨번호 리스트}
Lotto.당첨_로또_번호_data = {}
Lotto.당첨_연금복권_번호_data = {}
'''



# 로또
Lotto.당첨_로또_번호_data = json_load('./당첨_로또_번호_data.json', none_data={})

내_로또_번호 = Lotto.랜덤_로또_번호()
로또_당첨회차, 로또_당첨번호 = Lotto.get_로또_당첨번호()

for 로또_번호 in 내_로또_번호:
    로또_당첨여부 = Lotto.내_로또_확인(회차=로또_당첨회차, 로또_번호=내_로또_번호)
    #print(로또_당첨여부)
    if 로또_당첨여부['당첨여부']:
        print(f"로또 {로또_당첨회차} 회차 {로또_당첨여부['등수']}등 당첨!\n내 번호: {로또_번호}")
    else:
        print(f'로또 {로또_당첨회차} 회차 꽝 입니다.\n내 번호: {로또_번호}')

json_dump('./당첨_로또_번호_data.json', Lotto.당첨_로또_번호_data)



# 연금복권
Lotto.당첨_연금복권_번호_data = json_load('./당첨_연금복권_번호_data.json', none_data={})

내_연금복권_번호 = Lotto.랜덤_연금복권_번호()
연금복권_당첨회차, 연금복권_당첨번호 = Lotto.get_연금복권_당첨번호()

for 연금복권_번호 in 내_연금복권_번호:
    연금복권_당첨여부 = Lotto.내_연금복권_확인(회차=연금복권_당첨회차, 연금복권_번호=내_연금복권_번호)
    #print(연금복권_당첨여부)
    if 연금복권_당첨여부['당첨여부']:
        print(f"연금복권 {연금복권_당첨회차} 회차 {연금복권_당첨여부['등수']}등 당첨!\n내 번호: {연금복권_번호}")
    else:
        print(f'연금복권 {연금복권_당첨회차} 회차 꽝 입니다.\n내 번호: {연금복권_번호}')

json_dump('./당첨_연금복권_번호_data.json', Lotto.당첨_연금복권_번호_data)


