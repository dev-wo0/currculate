#실시간 Daum 환율을 이용한 환율계산기

import requests
from bs4 import BeautifulSoup

#환율들이 들어갈 리스트
#달러, 엔화, 유로, 위안, 호주달러
exchanges = [] 

class Calc :
    def __init__(self, result = 0) :
        self.__result = result
        
    #a= 현재돈, b = 환율
    def ToKorean(self, a, b) :  
        result = round(a * b, 2)    #소수점 2째자리 반올림
        return result
    
    def ToExchange(self, a, b) :
        result = round(a / b, 2)
        return result
    

def web_search(value) :             # 어떤 환율을 사용 할지 value 값 전달.
    req = requests.get('https://search.daum.net/search?w=tot&DA=YZR&t__nil_searchbox=btn&sug=&sugo=&q=%ED%99%98%EC%9C%A8')  # 웹 페이지 URL
    html = req.text                             # URL의 html파일 
    soup = BeautifulSoup(html, 'html.parser')   # html 파일 파싱 준비

    # my_titles는 list 객체
    exchange_list = soup.select(
        '#exBoxTab > a > span > em.txt_num'     # 환율 부분을 나타내는 Tag들 목록
    )
    
    for title in exchange_list :
        # Tag안의 텍스트
        exchanges.append(title.text)            # 환율들을 리스트에 추가
    
    exchanges[1] = float(exchanges[1]) / 100    # 엔화 = 100엔 기준이므로 게산의 편의를 위해 1엔 기준으로 나눠줌.

    return float(exchanges[value-1])
        

def main() :
    print("**************************")
    print("실시간 환율 계산기 입니다.")
    print("원하는 환율을 골라주세요.")
    print("1.달러\t2.엔화\t3.유로\t4.위안\t5.호주달러\n")
    while(1) :
        value = int(input("원하는 환율을 골라주세요."))
        if(value < 1 or value > 5) :
            print("1 ~ 5까지의 숫자를 입력해주세요.\n**************************\n")
        else :
            break
    
    Exc_rate = web_search(value) #환율
    if(value==1) :
        money_K = "달러"
    elif(value==2) :
        money_K = "엔화"
    elif(value==3) :
        money_K = "유로"
    elif(value==4) :
        money_K = "위안"
    else :
        money_K = "호주달러"
        
    print(money_K,"를 선택하셨습니다.\n현재 Daum 웹페이지 기준",money_K,"의 환율은 1원당",Exc_rate,money_K,"입니다.\n\n")
    
    #외국돈을 원화로 바꿀지, 원화에서 외국돈으로 바꿀지
    print("1.",money_K,"-> 원화\t\t2.원화 ->",money_K)
    while(1) :
        Exc = input()
        if(Exc == "1" or Exc == "2") :
            break
        else :
            print("숫자를 다시 입력해주세요.\n**************************\n\n1.",money_K,"-> 원화\t\t2.원화 ->",money_K)

    if(Exc=="1") :      #외국돈 -> 원화
        print(money_K,"-> 원화를 선택하셨습니다.")
        print("\n현재 가지고 있는",money_K,"를 입력하세요.")
        get_Money = float(input())

    elif(Exc=="2") :
        print("원화 ->",money_K,"를 선택하셨습니다.")
        print("\n현재 가지고 있는 원화를 입력하세요.")
        get_Money = float(input())
    
    calc = Calc()
    if(Exc=="1") :      #외국돈 -> 원화
        Result = calc.ToKorean(get_Money, Exc_rate)
        print("환전 결과는 =",Result,"원")
        
    elif(Exc=="2") :    #원화 -> 외국돈
        Result = calc.ToExchange(get_Money, Exc_rate)
        print("환전 결과는 =",Result, money_K)
    
main()
