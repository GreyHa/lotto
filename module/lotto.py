import random, time, requests
from bs4 import BeautifulSoup

class lotto():

    def __init__(self):
        self.당첨_로또_번호_data = {}
        self.당첨_연금복권_번호_data = {}

        self.로또_선택_번호 = list(range(1,46))
        self.연금복권_선택_번호 = {
            '0':list(range(1,6)),
            '1':list(range(0,10)),
            '2':list(range(0,10)),
            '3':list(range(0,10)),
            '4':list(range(0,10)),
            '5':list(range(0,10)),
            '6':list(range(0,10))
        }
        
        
    def __연금복권_보정_값__(self, data:dict):
        '''
            data: {
                '1': [],
                '2': [],
                '3': [],
                '4': [],
                '5': [],
                '6': [],
            }
            
            각 array에 들어 갈 숫자 범위는 1~9
            숫자가 많을 수록 그 숫자가 뽑히는 확률 증가
        '''
        for key in data:
            self.연금복권_선택_번호[key] += data[key]

    def __로또_보정_값__(self, data:list):
        '''
            data: []
            
            array에 들어 갈 숫자 범위는 1~45
            숫자가 많을 수록 그 숫자가 뽑히는 확률 증가
        '''
        self.로또_선택_번호 += data

    def 랜덤_연금복권_번호(self, 고정_번호={}, delay=0):
        '''
            고정_번호 = {
                '1': 0~9,
                .
                ..
                ...
                '6': 0~9
            }
            key 값 1~6
            특정 자리수를 고정
        '''
        result = []
        선택_번호 = []
        for key in range(1,7):
            if key in 고정_번호:
                선택_번호.append(고정_번호[str(key)])
            else:
                선택_번호.append(random.choice(self.연금복권_선택_번호[str(key)]))
            time.sleep(delay)

        for 조 in range(1,6):
            result.append([조]+선택_번호)
            
        #print(f'연금 복권 번호: {result}')
        return result

    def 랜덤_로또_번호(self, 고정_번호:list=[], 개수=5, delay=0):
        '''
            고정_번호 = []
            
            특정 숫자 고정 최대 6개
        '''
        result = []
        
        for _ in range(개수):
            선택_번호 = [] + 고정_번호
            __로또_선택_번호__ = list(self.로또_선택_번호)
            while len(선택_번호) < 6:
                번호 = random.choice(__로또_선택_번호__)
                if 번호 not in result:
                    선택_번호.append(번호)
                    __로또_선택_번호__ = list(filter(lambda x: x != 번호, __로또_선택_번호__))
                    time.sleep(delay)

            선택_번호.sort()
            result.append(선택_번호)

        #print(f'로또 번호: {result}')
        return result

    def get_연금복권_당첨번호(self, Round:int=-1):
        result = []

        url = 'https://m.dhlottery.co.kr/gameResult.do?method=win720'
        if Round >= 1:
            url += f'&Round={Round}'

        html = requests.get(url).text
        bsobj = BeautifulSoup(html, 'html.parser')
        
        el0 = 'select option[selected]'
        el1 = 'div.prizeresult div.prize:nth-child(1) h4 strong, div.prizeresult div.prize:nth-child(1) ul li'

        select = bsobj.select(el0)
        회차 = select[0].get('value')
        select = bsobj.select(el1)
        for el in select:
            result.append(int(el.text))

        #print(f'{회차} 회차: {result}')
        self.당첨_연금복권_번호_data[str(회차)] = result
        return int(회차), result

    def get_로또_당첨번호(self, Round:int=-1):
        result = []

        url = 'https://m.dhlottery.co.kr/gameResult.do?method=byWin'
        if Round >= 1:
            data = {'drwNo':Round}
            el0 = 'select.numberSelect option[selected]'
        else:
            el0 = 'select.numberSelect option:nth-child(1)'
            data = {}

        response = requests.post(url, data=data)
        html = response.text
        
        bsobj = BeautifulSoup(html, 'html.parser')

        el1 = 'div.bx_lotto_winnum span.ball'

        select = bsobj.select(el0)
        회차 = select[0].get('value')

        select = bsobj.select(el1)
        for el in select:
            result.append(int(el.text))
        
        #print(f'{회차} 회차: {result}')
        self.당첨_로또_번호_data[str(회차)] = result
        return int(회차), result

    def 내_로또_확인(self, 회차, 로또_번호):
        if str(회차) not in self.당첨_로또_번호_data:
            self.get_로또_당첨번호(Round=int(회차))
            time.sleep(3)

        회차_당첨_번호 = self.당첨_로또_번호_data[str(회차)]

        당첨 = []

        for 내_번호 in 로또_번호:
            if 내_번호 in 회차_당첨_번호[0:6]:
                당첨.append(내_번호)

        if len(당첨) == 3:
            등수 = 5

        elif len(당첨) == 4:
            등수 = 4
        
        elif len(당첨) == 5:
            if 회차_당첨_번호[6] in 로또_번호:
                등수 = 2
            else:
                등수 = 3

        elif len(당첨) == 6:
            등수 = 1

        else:
            등수 = -1

        if 등수 > 0:
            당첨여부 = True
        else:
            당첨여부 = False

        result = {
            '당첨여부': 당첨여부,
            '등수': 등수,
            '회차': 회차,
            '당첨 번호': 회차_당첨_번호,
            '내 번호': 로또_번호,
            '맞은 번호': 당첨
        }

        #print(result)
        return result

    def 내_연금복권_확인(self, 회차, 연금복권_번호):

        if str(회차) not in self.당첨_연금복권_번호_data:
            self.get_연금복권_당첨번호(Round=int(회차))
            time.sleep(3)

        회차_당첨_번호 = self.당첨_연금복권_번호_data[str(회차)]

        당첨 = []

        for number_index in range(-1, -len(회차_당첨_번호), -1):
            당첨_번호 = 회차_당첨_번호[number_index]
            if 당첨_번호 == 연금복권_번호[number_index]:
                당첨.insert(0,당첨_번호)
            else:
                break

        if len(당첨) == 1:
            등수 = 7

        elif len(당첨) == 2:
            등수 = 6
        
        elif len(당첨) == 3:
            등수 = 5

        elif len(당첨) == 4:
            등수 = 4
        
        elif len(당첨) == 5:
            등수 = 3

        elif len(당첨) == 6:
            등수 = 2

        elif len(당첨) == 7:
            등수 = 1

        else:
            등수 = -1
        
        if 등수 > 0:
            당첨여부 = True
        else:
            당첨여부 = False

        result = {
            '당첨여부': 당첨여부,
            '등수': 등수,
            '회차': 회차,
            '당첨 번호': 회차_당첨_번호,
            '내 번호': 연금복권_번호,
            '맞은 번호': 당첨
        }

        #print(result)
        return result