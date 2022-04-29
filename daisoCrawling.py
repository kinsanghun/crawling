from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import Select
import pandas as pd
import time


class daiso:
  def __init__(self):
    self.url = "https://www.daiso.co.kr/cs/shop"
    self.arealist = ["동대문구", "강남구", "은평구", "중랑구", "성동구", "성북구", "종로구", "영등포구", "강동구", "화곡동", "광진구", "마포구", "구로구", "양천구",
                     "중구", "용산구", "노원구", "관악구", "서대문구", "서초구", "동작구", "송파구", "강서구", "도봉구", "강북구", "금천구"]

  def run(self):
    datas = list()
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options
    driver.implicitly_wait(1)

    driver.get(self.url)
    driver.implicitly_wait(1)
    
    driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/section/div/form/div/div[2]/div[1]/ul/li[3]/a").click()
    select_main = Select(driver.find_element(By.XPATH, "//*[@id='searchRegion']/span[1]/select"))
    select_main.select_by_value("서울")
    driver.implicitly_wait(3)

    select = Select(driver.find_element(By.XPATH, "//*[@id='searchRegion']/span[2]/select"))
    searchButtonPath = "/html/body/div[1]/div[3]/section/div/form/div/div[2]/div[4]/button"

    for area in self.arealist:
      div_count = 1
      arealist = dict()
      d_title = list()
      d_addr = list()

      select.select_by_value(area)
      driver.implicitly_wait(1)
      driver.find_element(By.XPATH, searchButtonPath).click()
      driver.implicitly_wait(1)
      time.sleep(1)
    
      while True:
        try:
          title = driver.find_element(By.XPATH, f"/html/body/div[1]/div[3]/section/div/form/div/div[4]/div/div/div[{div_count}]/a/h4").text
          driver.implicitly_wait(1)
          addr = driver.find_element(By.XPATH, f"/html/body/div[1]/div[3]/section/div/form/div/div[4]/div/div/div[{div_count}]/a/p").text
          driver.implicitly_wait(1)

          s = addr.find("(")+1
          e = addr.rfind(")")
          if s == 0:
            city = ""
          else:
            city = addr[s:e]
            city = city[:city.rfind("동")+1]

          datas.append([area, city, title, addr])
          div_count += 1

        except:
          print("Count : ", div_count-1)
          break

    driver.close()
    result = pd.DataFrame(datas, columns=["class","city", "name", "Address"])
    return result
      

if __name__ == "__main__":
  daios = daiso()
  datas = daios.run()
  print(datas)
  datas.to_csv("result.csv")
