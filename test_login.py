import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # รันแบบไม่มีหน้าต่าง UI สำหรับ CI/CD
    driver = webdriver.Chrome(options=chrome_options)
    
    # ชี้ path 
    html_file_path = f"file://{os.path.abspath('Simple login.html')}"
    driver.get(html_file_path)
    
    yield driver
    driver.quit()

def test_successful_login(driver):
    # ใส่ข้อมูลถูกต้อง
    driver.find_element(By.ID, "user").send_keys("admin")
    driver.find_element(By.ID, "pass").send_keys("1234")
    driver.find_element(By.ID, "btn").click()
    
    welcome_box = driver.find_element(By.ID, "welcomeBox")
    assert welcome_box.get_attribute("hidden") is None

def test_wrong_password(driver):
    # ใส่รหัสผ่านผิด
    driver.find_element(By.ID, "user").send_keys("admin")
    driver.find_element(By.ID, "pass").send_keys("wrongpass")
    driver.find_element(By.ID, "btn").click()
    
    # ตรวจสอบข้อความ Error
    error_msg = driver.find_element(By.ID, "msg").text
    assert error_msg == "Wrong password. Try again."