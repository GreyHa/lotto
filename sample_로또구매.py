import config.conf as conf
from module.lotto import lotto
from automation_framework.Web import Web
from automation_framework.__chromedriver_autoinstall__ import chrome_driver_install_path
import element.element as el
import os

__script_path__ = f'{os.path.dirname(os.path.abspath(__file__))}'
login_id = conf.login_id
login_pw = conf.login_pw

def 로또_구매(로또_번호:list):
    '''
        로또_번호: [[번호6개],[번호6개]...]
        로또_번호는 최대 5개 까지만 적용
        선택_번호 6개의 array를 5개 까지 포함
    '''
    page3 = 'https://el.dhlottery.co.kr/game/TotalGame.jsp?LottoId=LO40'
    div.driver.get(page3)
    div.driver.switch_to.frame(0)
    회차 = div(el.lp72_회차).FindValues().ElementValue
    for 선택_번호 in 로또_번호[0:5]:
        elements = div(el.lotto_nums).FindValues()
        for 번호 in 선택_번호[0:6]:
            elements.ElementHandle[elements.ElementValueList.index(str(번호))].click()

        div(el.lotto_ok1).Click()
    div(el.lotto_ok2).Click()
    div(el.lotto_ok3).Click()

    return 회차, 로또_번호 

def 연금복권_구매(연금복권_번호:list):
    '''
        연금복권_번호: [[번호7개],[번호7개]...]
        연금복권_번호는 최대 5개 까지만 적용
        선택_번호 7개의 array를 5개 까지 포함
    '''
    page2 = 'https://el.dhlottery.co.kr/game/TotalGame.jsp?LottoId=LP72'
    div.driver.get(page2)
    div.driver.switch_to.frame(0)
    회차 = div.driver.execute_script('return initround')

    result = []
    
    div(el.lp72_select_num).Click()

    for 선택_번호 in 연금복권_번호[0:5]:
        div(el.lp72_jogrou, Value=f'{선택_번호[0]}조').FindValues(not_find_error=True).Click()
        
        elements = div(el.lp72_nums).FindValues()
        for 번호 in 선택_번호[1:7]:
            elements.ElementHandle[elements.ElementValueList.index(str(번호))].click()           

        div(el.lp72_ok1).Click()
        div.sleep(2)
        if div(el.lp72_not).DisplayElement().ElementDisplay:
            #이미 판매된 번호
            div(el.lp72_not_close).Click()
        else:
             result.append(연금복권_번호)

    div(el.lp72_ok2).Click()
    div(el.lp72_ok3).Click()
    return 회차, result



Lotto = lotto()
div = Web()

# 드라이버 접속
div.Connection(executable_path=chrome_driver_install_path(base_path=__script_path__))

#동행 복권 로그인
login_url = 'https://dhlottery.co.kr/user.do?method=login'
div.Change_url(login_url)

div(el.login_id, Value=login_id).Send()
div(el.login_pw, Value=login_pw).Send()
div(el.login_bt).Click()
div.sleep(5)


#로또 번호 생성
로또_번호 = Lotto.랜덤_로또_번호()
print(로또_번호)

#로또 구매
로또_회차, 로또번호 = 로또_구매(로또_번호=로또_번호)


#연금복권 번호 생성
연금복권_번호 = Lotto.랜덤_연금복권_번호()
print(연금복권_번호)

#연금복권 구매
연금복권_회차, 연금복권_번호 = 연금복권_구매(연금복권_번호=연금복권_번호)

#드라이버 종료
div.driver.quit()
