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
    driver.find_element_by_name('user.stu_nbr').send_keys('2018112801')
    driver.find_element_by_name('user.usr_id').send_keys('ehdwo98')
    driver.find_element_by_name('user.passwd').send_keys('wlsdk2991!')
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
    max_people = int((driver.find_element_by_xpath('/html/body/div/div[3]/div[11]/div/div[2]/table/tbody/tr[3]/td[8]')).text)
    current_people = int((driver.find_element_by_xpath('//*[@id="lectPackReqGrid_1"]/td[9]')).text)
    
    # 현재 신청 인원이 비면
    if(max_people > current_people):
        # 강의 취소
        lecture = driver.find_element_by_xpath('//*[@id="onlineLectReqGrid_5"]/td[2]')
        if(lecture.text == 'CLTR003002'):
            driver.find_element_by_xpath('//*[@id="onlineLectReqGrid_5"]/td[1]/input').click()
            driver.find_element_by_xpath('//*[@id="btn_delete"]').click()
            closeAlert()
            closeAlert()
        
            # 강의 신청
            driver.find_element_by_xpath('//*[@id="lectPackReqGrid_1"]/td[11]').click()
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