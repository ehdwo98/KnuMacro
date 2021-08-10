from selenium import webdriver
import time

driver = webdriver.Chrome('./chromedriver.exe')
driver.implicitly_wait(5)

url = 'https://sugang.knu.ac.kr/'

# 팝업창 처리
def closePopup():
    time.sleep(3)
    driver.switch_to_window(driver.window_handles[1])
    driver.close()
    driver.switch_to_window(driver.window_handles[0])

# 로그인
def login():
    driver.find_element_by_name('user.stu_nbr').send_keys('학번 입력')
    driver.find_element_by_name('user.usr_id').send_keys('아이디 입력')
    driver.find_element_by_name('user.passwd').send_keys('비번 입력')
    driver.find_element_by_xpath('//*[@id="loginForm"]/table/tbody/tr[4]/td/button[1]').click()
    driver.implicitly_wait(5)

# 재로그인
def init():
    driver.get(url)
    time.sleep(4)
    closePopup()
    time.sleep(1)
    login()
    time.sleep(2)

# 경고창 처리
def closeAlert():
    driver.implicitly_wait(10)
    alert = driver.switch_to_alert()
    alert.accept()

# 메인 로직
init()
login_time = time.time()

while(True):
    # 수강 신청 인원 비는지 확인
    max_people = int((driver.find_element_by_xpath('꽉찬 수꾸 강좌의 제한인원 xpath가져오기')).text)
    current_people = int((driver.find_element_by_xpath('꽉찬 수꾸 강좌의 현재인원 xpath가져오기')).text)
    
    # 현재 신청 인원이 비면
    if(max_people > current_people):
        # 강의 취소
        lecture = driver.find_element_by_xpath('수강목록에서 수취할 과목 교과목번호 xpath가져오기')
        if(lecture.text == 'CLTR003002'):
            driver.find_element_by_xpath('수강목록에서 수취할 과목 삭제선택 xpath가져오기').click()
            driver.find_element_by_xpath('수강신청 삭제버튼 xpaht가져오기').click()
            closeAlert()
            closeAlert()
        
            # 강의 신청
            driver.find_element_by_xpath('신청할 수꾸강좌 신청 xpath가져오기').click()
            closeAlert()
            print("강의 신청 확인")
            # 강의 신청되면 반복문 정지
            break

    # 로그인 만료 시간 임박하면 재로그인
    timelapse = int(time.time() - login_time)
    if(timelapse > 1150):
        print("재 로그인")
        driver.find_element_by_xpath('//*[@id="logout"]/button[1]').click()
        init()
        login_time = time.time()

    print("마지막 로그인 시간: {}초 전".format(str(timelapse)))
    time.sleep(1)
    driver.refresh()
