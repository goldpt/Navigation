from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from konlpy.tag import Komoran
mecab = Komoran()

def navigation(query):
    bow1 = mecab.pos(query)

    n_list = []
    for i in range(len(bow1)):
        if bow1[i][1] == 'NNP' or bow1[i][1] == 'NNG':
            n_list.append(bow1[i][0])

    destination = ''
    for j in range(len(n_list)):
        destination += n_list[j]

    start = "용두산공원"
    import time
    url = 'https://map.naver.com/v5/directions/-/-/-/walk?c=14363488.1740287,4177437.6448353,16,0,0,0,dh'

    driver = webdriver.Chrome(ChromeDriverManager().install())
    #driver = webdriver.Chrome('chromedriver.exe')
    driver.get(url)

    # 출발지 입력
    driver.find_element_by_xpath('//*[@id="directionStart0"]').click()
    driver.find_element_by_xpath('//*[@id="directionStart0"]').send_keys(start)
    driver.find_element_by_xpath('//*[@id="directionStart0"]').send_keys(Keys.ENTER)
    time.sleep(0.2)

    # 도착지 입력
    driver.find_element_by_xpath('//*[@id="directionGoal1"]').click()
    driver.find_element_by_xpath('//*[@id="directionGoal1"]').send_keys(destination)
    driver.find_element_by_xpath('//*[@id="directionGoal1"]').send_keys(Keys.ENTER)
    time.sleep(0.2)

    # 길찾기 버튼 누르기
    element = driver.find_element_by_xpath(
        '//*[@id="container"]/shrinkable-layout/div/directions-layout/directions-result/div[1]/div[1]/directions-search/div[2]/button[3]')
    driver.execute_script("arguments[0].click();", element)

    time.sleep(0.5)

    # 도보 거리 확인
    distance = driver.find_element_by_xpath('//*[@id="container"]/shrinkable-layout/div/directions-layout/directions-result/div[1]/directions-summary-list/directions-hover-scroll/div/ul/li[1]/directions-summary-item-walking/div[1]/span[2]/readable-distance').text

    if distance.__contains__('km'):
        driver.find_element_by_xpath('//*[@id="container"]/shrinkable-layout/div/directions-layout/directions-result/div[1]/div/ul/li[1]/a').click()
        time.sleep(1)

        optimaltime = driver.find_element_by_xpath(
            '//*[@id="container"]/shrinkable-layout/div/directions-layout/directions-result/div[1]/directions-summary-list/directions-hover-scroll/div/ul/li[1]/directions-summary-item-pubtransit/div[1]/div/strong').text
        optimal1 = driver.find_element_by_xpath(
            '//*[@id="container"]/shrinkable-layout/div/directions-layout/directions-result/div[1]/directions-summary-list/directions-hover-scroll/div/ul/li[1]/directions-summary-item-pubtransit/div[2]/ol')
        optimalmethod = optimal1.find_elements_by_tag_name('em')
        optimalstation = optimal1.find_elements_by_tag_name('strong')

        for j in range(len(optimalstation)):
            optimalstation[j] = optimalstation[j].text
            # print(j, ' : ', optimalstation[j])

        for i in range(len(optimalmethod)):
            if optimalmethod[i].text.__contains__('선'):
                optimalmethod[i] = '지하철 ' + optimalmethod[i].text
            elif optimalmethod[i].text.__contains__('동해'):
                optimalmethod[i] = '동해선'
            else:
                optimalmethod[i] = optimalmethod[i].text + '번 버스'

        # 환승 X
        if (len(optimalmethod) == 4) & (optimalmethod[2].__contains__('분')):
            # print('환승 X')
            method_path = '//*[@id="container"]/shrinkable-layout/div/directions-layout/directions-result/div[1]/directions-summary-list/directions-hover-scroll/div/ul/li[1]/directions-summary-item-pubtransit/div[2]/ol/li[1]/div[1]/div[2]/em'
            time_path = '//*[@id="container"]/shrinkable-layout/div/directions-layout/directions-result/div[1]/directions-summary-list/directions-hover-scroll/div/ul/li[1]/directions-summary-item-pubtransit/div[1]/div/strong'
            start_path = '//*[@id="container"]/shrinkable-layout/div/directions-layout/directions-result/div[1]/directions-summary-list/directions-hover-scroll/div/ul/li[1]/directions-summary-item-pubtransit/div[2]/ol/li[1]/div[2]/div[1]/strong'
            destination_path = '//*[@id="container"]/shrinkable-layout/div/directions-layout/directions-result/div[1]/directions-summary-list/directions-hover-scroll/div/ul/li[1]/directions-summary-item-pubtransit/div[2]/ol/li[2]/div[3]/div/strong'

            method = driver.find_element_by_xpath(method_path).text
            time1 = driver.find_element_by_xpath(time_path).text
            startpoint = driver.find_element_by_xpath(start_path).text
            destinationpoint = driver.find_element_by_xpath(destination_path).text

            if (method.__contains__('선')):
                vehicle = '지하철'
                answer = f'{startpoint}에서 {vehicle} {method}을 타고 {destinationpoint}에서 하차하세요. 예상 소요 시간은 {time1}입니다.'

            elif (method.__contains__('동해')):
                answer = f'{startpoint}에서 동해선을 타고 {destinationpoint}에서 하차하세요. 예상 소요 시간은 {time1}입니다.'

            else:
                vehicle = '버스'
                answer = f'{startpoint} 정거장에서 {method}번 {vehicle}를 타고 {destinationpoint} 정거장에서 하차하세요. 예상 소요 시간은 {time1}입니다.'

        # 1번 환승
        elif len(optimalmethod) == 4:
            method = []
            method.append(optimalmethod[0])
            method.append(optimalmethod[2])
            answer = f'{optimalstation[0]}에서 {method[0]}를 타고 {optimalstation[1]}에서 {method[1]}으로 환승하고 {optimalstation[2]}에서 내리면 도착합니다. 예상 소요 시간은 {optimaltime}입니다.'

            # 가끔 1번 환승인데 len=4인 경우 버스 번호는 optimalmethod0,2
            # 진짜 len=4인 경우는 버스번호 0

        # 1번 환승
        elif len(optimalmethod) == 5:
            method = []
            method.append(optimalmethod[0])
            method.append(optimalmethod[3])
            answer = f'{optimalstation[0]}에서 {method[0]}를 타고 {optimalstation[1]}에서 {method[1]}로 환승하고 {optimalstation[2]}에서 내리면 도착합니다. 예상 소요 시간은 {optimaltime}입니다.'

        # 2번 환승
        elif len(optimalmethod) == 6:
            method = []
            method.append(optimalmethod[0])
            method.append(optimalmethod[3])
            method.append(optimalmethod[4])
            answer = f'{optimalstation[0]}에서 {method[0]}를 타고 {optimalstation[1]}에서 {method[1]}로 환승하고 ' \
                     f'{optimalstation[2]}에서 {method[2]}로 환승하고 {optimalstation[3]}에서 내리면 도착합니다. 예상 소요 시간은 {optimaltime}입니다.'

    else:
        answer = f'큰 길을 따라 {distance} 걸어가면 도착합니다.'

    current_url = driver.current_url

    url1 = 'https://vivoldi.com/url/'
    driver.get(url1)

    driver.find_element_by_xpath('//*[@id="url"]').click()
    driver.find_element_by_xpath('//*[@id="url"]').send_keys(current_url)
    driver.find_element_by_xpath('//*[@id="btnUrl"]').click()

    time.sleep(0.3)

    shorten_url = driver.find_element_by_xpath('//*[@id="linkUrl"]').text

    answer = "r" + answer + shorten_url
    return answer
