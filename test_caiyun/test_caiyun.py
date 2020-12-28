import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
# from lxml import etree
from nose.tools import assert_equal
from selenium import webdriver
import requests
import re
import json
from selenium.webdriver.common.action_chains import ActionChains


driver = webdriver.Chrome(ChromeDriverManager().install())


def setup():
    print("=======test_case set up=======")


def teardown():
    # driver.quit()
    print("=======test_case tear down=======")


# 语言描述显示
def test_case1():
    print("================test_case1============")
    driver.get('http://www.caiyunapp.com/map')
    ActionChains(driver).move_by_offset(645, 537).click().perform()
    current_url = driver.current_url
    num = re.findall("#(.*)", current_url)[0]
    # num = re.search("#(.*)", current_url)
    # print(num)
    longitude = num.split(",")[0]
    latitude = num.split(",")[1]
    # 这种写法不用导入By
    web_tip = driver.find_elements_by_xpath("//div[@class='desc']")[1].text
    # web_tip = driver.find_elements(By.XPATH, "//div[@class='desc']")[1].text
    # web_tem = driver.find_elements(By.XPATH, "//div[@class='temp']/span")[0].text
    # print(web_tip)
    # print(longitude)
    # print(latitude)
    url = "https://api.caiyunapp.com/v2.5/96Ly7wgKGq6FhllM/{longitude},{latitude}/weather.json"\
        .format(longitude=longitude, latitude=latitude)
    print(url)
    response = requests.get(url=url)
    res_dict = json.loads(response.content)
    tip = res_dict['result']['forecast_keypoint']
    # tip = res_dict['result']['minutely']['description']
    # print(tip)
    assert_equal(web_tip, tip)
    case2(res_dict)
    case3(longitude, latitude)
    # assert_equal(web_tem, tem)
    case4(res_dict)
    case5(res_dict)


# 温度显示
def case2(res_dict):
    print("================test_case2============")
    tem = res_dict['result']['realtime']['temperature']
    tem = str(round(tem)) + "°"
    # print(tem)
    web_tem = driver.find_elements(By.XPATH, "//div[@class='temp']/span")[0].text
    assert_equal(web_tem, tem)


# 空气雷达图显示
def case3(longitude, latitude):
    print("================test_case3============")
    time.sleep(5)
    driver.find_elements_by_id("a-air")[0].click()
    aqi_url = "https://caiyunapp.com/fcgi-bin/v1/img.py?token=96Ly7wgKGq6FhllM&lonlat={longitude},{latitude}&type=pm25"\
        .format(longitude=longitude, latitude=latitude)
    aqi_response = requests.get(url=aqi_url)
    res_dict = json.loads(aqi_response.content)
    pics = res_dict['radar_img']
    # x = 0
    # 接口图片数据
    radar = []
    for pic in pics:
        # print(pic[0])
        pic1 = re.findall("(.*)\?", pic[0])[0]
        # print(pic)
        radar.append(pic1)
        # x += 1
    # print(radar)
    # print(x)
    # print(res_dict['status'])
    # print("=========================================")
    driver.find_elements_by_id("switch")[0].click()
    web_pics = driver.find_elements_by_xpath("//div[@class='amap-layers']/div/img")
    # print(web_pics)
    web_radar = []
    for web_pic in web_pics:
        # print(web_pic)
        # print(web_pic.get_attribute("src"))
        pic2 = web_pic.get_attribute("src")
        pic3 = re.findall("(.*)\?", pic2)[0]
        web_radar.append(pic3)
    # print(web_radar)
    driver.find_elements_by_id("switch")[0].click()
    assert_equal(web_radar, radar)


# 空气质量指数和状态
def case4(res_dict):
    # print(res_dict)
    print("================test_case4============")
    quality_num = res_dict['result']['realtime']['air_quality']['aqi']['chn']
    # print(round(quality_num))
    quality_num = str(round(quality_num))
    quality_status = res_dict['result']['realtime']['air_quality']['description']['chn']
    # print(quality_status)
    web_quality_num = driver.find_elements_by_xpath("//div[@class='temp']/span")[0].text
    # print(web_quality_num)
    web_quality_status = driver.find_elements_by_xpath("//div[@class='temp']/small")[0].text
    # print(web_quality_status)
    assert_equal(web_quality_num, quality_num)
    assert_equal(web_quality_status, quality_status)


# 空气语言描述显示
def case5(res_dict):
    print("================test_case5============")
    aqi_tip = res_dict['result']['hourly']['description']
    web_aqi_tip = driver.find_elements_by_xpath("//div[@class='desc']")[1].text
    assert_equal(web_aqi_tip, aqi_tip)