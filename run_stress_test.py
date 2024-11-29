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
  pass_cnt = 0
  fail_cnt = 0
  avg_rgb_cnt = {}

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
      result += f'test cycle #{i+1} completed successfully:\n{completed}\n'
      pass_cnt += 1
    else:
      result += f'tset cycle #{i+1} failed:\n{completed}\n'
      fail_cnt += 1

    print(f'INFO: test cycle #{i+1} catching camera info')
    info_table = driver.find_element(By.XPATH, '//*[@id="webcam-props"]/table').text
    avg_rgb = driver.find_element(By.XPATH, '//*[@id="webcam-prop_image_rgb_color"]/div').value_of_css_property('background')
    avg_rgb = avg_rgb.split(' n')[0]
    result += f'Webcam Information:\n{info_table}\nAverage RGB Color: {avg_rgb}\n============================'

    if avg_rgb in avg_rgb_cnt.keys():
      avg_rgb_cnt[avg_rgb] += 1
    else:
      avg_rgb_cnt[avg_rgb] = 1

  driver.quit()
  print(f'INFO: complete camera sress test for {cycles} cycles.')

  report = f'\n========== Report ==========\nPass: {pass_cnt}/{cycles}\nFail: {fail_cnt}/{cycles}\nAverage RGB Color: {avg_rgb_cnt}\n========== Details ==========\n'
  result = report + result

  file_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
  f = open(f'./log/camera_stress_log_{file_datetime}.log', 'a')
  f.write(result)
  f.close()
  print(f'INFO: please refer to the file ./log/camera_stress_log_{file_datetime}.log to see the details.')

  sys.exit()
