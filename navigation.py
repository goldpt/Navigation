from selenium import webdriver
from selenium.webdriver.common.keys import Keys

start = input('출발지를 입력하세요 : ')
destination = input('도착지를 입력하세요 : ')

def navigation(start, destination):
    import time
    url = 'https://map.naver.com/v5/directions/-/-/-/transit?c=14369089.5036386,4194531.2959524,15,0,0,0,dh'
    driver = webdriver.Chrome('D:\\anaconda3\\envs\\chatbot\\bin\\conversation_detect\\chromedriver.exe')
    driver.get(url)

    # 출발지 입력
    driver.find_element_by_xpath('//*[@id="directionStart0"]').click()
    driver.find_element_by_xpath('//*[@id="directionStart0"]').send_keys(start)
    driver.find_element_by_xpath('//*[@id="directionStart0"]').send_keys(Keys.ENTER)
    time.sleep(0.1)

    # 도착지 입력
    driver.find_element_by_xpath('//*[@id="directionGoal1"]').click()
    driver.find_element_by_xpath('//*[@id="directionGoal1"]').send_keys(destination)
    driver.find_element_by_xpath('//*[@id="directionGoal1"]').send_keys(Keys.ENTER)
    time.sleep(0.2)

    # 길찾기 버튼 누르기
    element = driver.find_element_by_xpath(
        '//*[@id="container"]/shrinkable-layout/div/directions-layout/directions-result/div[1]/div/directions-search/div[2]/button[2]')
    driver.execute_script("arguments[0].click();", element)

    time.sleep(0.6)

    # 최소 환승순
    element1 = driver.find_element_by_xpath(
        '//*[@id="container"]/shrinkable-layout/div/directions-layout/directions-result/div[1]/directions-summary-list/directions-summary-list-transit-option/div/div/div/button/span')
    driver.execute_script("arguments[0].click();", element1)
    driver.find_element_by_xpath('//*[@id="container"]/shrinkable-layout/div/directions-layout/directions-result/div[1]/directions-summary-list/directions-summary-list-transit-option/div/div/div/ul/li[3]/button').click()

    method_path = '//*[@id="container"]/shrinkable-layout/div/directions-layout/directions-result/div[1]/directions-summary-list/directions-hover-scroll/div/ul/li[1]/directions-summary-item-pubtransit/div[2]/ol/li[1]/div[1]/div[2]/em'
    time_path = '//*[@id="container"]/shrinkable-layout/div/directions-layout/directions-result/div[1]/directions-summary-list/directions-hover-scroll/div/ul/li[1]/directions-summary-item-pubtransit/div[1]/div/strong'
    start_path = '//*[@id="container"]/shrinkable-layout/div/directions-layout/directions-result/div[1]/directions-summary-list/directions-hover-scroll/div/ul/li[1]/directions-summary-item-pubtransit/div[2]/ol/li[1]/div[2]/div[1]/strong'
    destination_path = '//*[@id="container"]/shrinkable-layout/div/directions-layout/directions-result/div[1]/directions-summary-list/directions-hover-scroll/div/ul/li[1]/directions-summary-item-pubtransit/div[2]/ol/li[2]/div[3]/div/strong'

    method = driver.find_element_by_xpath(method_path).text
    time = driver.find_element_by_xpath(time_path).text
    startpoint = driver.find_element_by_xpath(start_path).text
    destinationpoint = driver.find_element_by_xpath(destination_path).text

    if (method.__contains__('선')):
        vehicle = '지하철'
        answer = f'{startpoint}에서 {vehicle} {method}을 타고 {destinationpoint}에서 하차하세요. 예상 소요 시간은 {time}입니다.'
        print(answer)
    elif (method.__contains__('동해')):
        answer = f'{startpoint}에서 동해선을 타고 {destinationpoint}에서 하차하세요. 예상 소요 시간은 {time}입니다.'
        print(answer)
    else:
        vehicle = '버스'
        answer = f'{method}번 {vehicle}를 타고 {startpoint} 정거장에서 승차 후 {destinationpoint} 정거장에서 하차하세요. 예상 소요 시간은 {time}입니다.'
        print(answer)

import time
start__ = time.time()
navigation(start, destination)
print('대답 생성 시간 : ', time.time()-start__, '초')