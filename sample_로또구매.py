import config.conf as conf
from module.lotto import lotto
from automation_framework.Web import Web
from automation_framework.__chromedriver_autoinstall__ import chrome_driver_install_path
import element.element as el
import os

def 로또_구매(client:Web, 로또_번호:list):
    '''
        로또_번호: [[번호6개],[번호6개]...]
        로또_번호는 최대 5개 까지만 적용
        선택_번호 6개의 array를 5개 까지 포함
    '''

    # 구매 페이지로 변경
    url = 'https://el.dhlottery.co.kr/game/TotalGame.jsp?LottoId=LO40'
    client.Change_url(url)

    # 번호 선택 영역 프레임 변경
    client.Change_frame(0)

    # 회차 값 가져오기
    회차 = client(el.lp72_회차).FindValues().ElementValue
    
    # 번호 선택
    for 선택_번호 in 로또_번호[0:5]:
        
        '''
            # 해당 방식으로도 사용 가능하지만 속도 면에서 현재 코드가 효율적
            for 번호 in 선택_번호[0:6]:
                div(el.lotto_nums, Value=str(번호)).FindValues(not_find_error=True).Click()
        '''

        elements = client(el.lotto_nums).FindValues()
        for 번호 in 선택_번호[0:6]:
            elements.ElementHandle[elements.ElementValueList.index(str(번호))].click()

        client(el.lotto_ok1).Click()

    client(el.lotto_ok2).Click()
    client(el.lotto_ok3).Click()

    return 회차, 로또_번호

def 연금복권_구매(client:Web, 연금복권_번호:list, 모든조=True):
    '''
        연금복권_번호: [[번호7개],[번호7개]...]
        연금복권_번호는 최대 5개 까지만 적용
        선택_번호 7개의 array를 5개 까지 포함
    '''
    url = 'https://el.dhlottery.co.kr/game/TotalGame.jsp?LottoId=LP72'
    client.Change_url(url)

    # 번호 선택 영역 프레임 변경
    client.Change_frame(0)

    # 회차를 javascript 명령으로 조회
    회차 = client.driver.execute_script('return initround')

    result = []
        
    for 선택_번호 in 연금복권_번호[0:5]:
        # 조 선택
        
        if 모든조 == True:
            client(el.lp72_allgroup).Click()
        else:
            client(el.lp72_jogroup, Value=f'{선택_번호[0]}조').FindValues(not_find_error=True).Click()

        # 첫번째 번호 칸 선택
        client(el.lp72_select_num).Click()

        # 번호 선택
        elements = client(el.lp72_nums).FindValues()
        for 번호 in 선택_번호[1:7]:
            elements.ElementHandle[elements.ElementValueList.index(str(번호))].click()           

        client(el.lp72_ok1).Click()
        client.sleep(2)
        if client(el.lp72_not).DisplayElement().ElementDisplay:
            # 이미 판매된 번호
            # 이미 판매된 번호인 경우에 대한 처리를 함수에서 정해야 하는지 고민 필요
            # 현재는 이미 판매된 번호에 대해서 스킵 처리
            client(el.lp72_not_close).Click()
        else:
            if 모든조 == True:
                result = [[1] + 선택_번호[1:7], [2] + 선택_번호[1:7], [3] + 선택_번호[1:7], [4] + 선택_번호[1:7], [5] + 선택_번호[1:7]]
                break
            else:
                result.append(연금복권_번호)
    
    client(el.lp72_ok2).Click()
    try:
        client.alert_accept()
    except:
        pass
    client(el.lp72_ok3).Click()

    return 회차, result


if __name__ == '__main__':
    __script_path__ = f'{os.path.dirname(os.path.abspath(__file__))}'
    login_id = conf.login_id
    login_pw = conf.login_pw

    Lotto = lotto()
    client = Web()

    # 드라이버 접속
    client.Connection(executable_path=chrome_driver_install_path(base_path=__script_path__))

    #동행 복권 로그인
    login_url = 'https://dhlottery.co.kr/user.do?method=login'
    client.Change_url(login_url)

    client(el.login_id, Value=login_id).Send()
    client(el.login_pw, Value=login_pw).Send()
    client(el.login_bt).Click()
    client.sleep(5)


    #로또 번호 생성
    로또_번호 = Lotto.랜덤_로또_번호()
    print(로또_번호)

    #로또 구매
    로또_회차, 로또번호 = 로또_구매(client, 로또_번호=로또_번호)


    #연금복권 번호 생성
    연금복권_번호 = Lotto.랜덤_연금복권_번호()
    print(연금복권_번호)

    #연금복권 구매
    연금복권_회차, 연금복권_번호 = 연금복권_구매(client, 연금복권_번호=연금복권_번호)

    #드라이버 종료
    client.driver.quit()
