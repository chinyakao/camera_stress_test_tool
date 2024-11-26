import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from time import sleep
from datetime import datetime

if __name__ == '__main__':
  if len(sys.argv) == 3:
    if sys.argv[1] == '-c':
      cycles = int(sys.argv[2])
  else:
    print('WARN: Arguments is insufficient. Please try "python3 run_stress_test.py -c 100"')
    sys.exit()
  
  baseurl = 'https://webcamtests.com/'
  result = ''
  
  # Configure content settings to disable notifications/geolocation, allow mic/camera
  chrome_opt = ChromeOptions()  
  content_settings = {'notifications': 2, 'geolocation': 2, 'media_stream': 1}
  profile = {'managed_default_content_settings': content_settings}
  prefs = {'profile': profile}
  chrome_opt.add_experimental_option('prefs', prefs)

  driver = webdriver.Chrome(options=chrome_opt)

  for i in range(cycles):
    # Navigate to the https://webcamtests.com/
    print(f'INFO: test cycle #{i+1} getting in webcamtests')
    driver.get(baseurl)
    driver.implicitly_wait(10)

    # Wait for detecting camera device
    sleep(10)
    
    launch = driver.find_element(By.ID, 'webcam-launcher')
    launch.click()
    driver.implicitly_wait(10)
    
    print(f'INFO: test cycle #{i+1} testing camera')
    sleep(60)
    
    print(f'INFO: test cycle #{i+1} checking test result')
    completed = driver.find_element(By.XPATH, '//*[@id="webcam-notices"]').text
    if 'Testing was completed successfully.' in completed:
      result += f"test cycle #{i+1} completed successfully:\n{completed}\n"
    else:
      result += f"tset cycle #{i+1} failed:\n{completed}\n"

    print(f'INFO: test cycle #{i+1} catching camera info')
    info_table = driver.find_element(By.XPATH, '//*[@id="webcam-props"]/table').text
    result+= f"Webcam Information:\n{info_table}\n====================\n"

  driver.quit()
  print(f'INFO: complete camera sress test for {cycles} cycles.')  

  file_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
  f = open(f"./log/camera_stress_log_{file_datetime}.log", "a")
  f.write(result)
  f.close()
  print(f'INFO: please refer to the file ./log/camera_stress_log_{file_datetime}.log to see the details.')

  sys.exit()
