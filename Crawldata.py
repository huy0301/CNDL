import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time

# Đường dẫn tới ChromeDriver
chrome_driver_path = 'C:/Users/MSI/Downloads/chromedriver-win64/chromedriver.exe'  # Thay đổi đường dẫn tới ChromeDriver

# Khởi tạo Service
service = Service(chrome_driver_path)

# Khởi tạo WebDriver cho Chrome
driver = webdriver.Chrome(service=service)

# URL của trang web cần crawl
url = "https://www.nhatot.com/mua-ban-bat-dong-san"

# Mở trang web
driver.get(url)

# Đợi một chút để trang web tải xong
time.sleep(5)

# Danh sách để lưu dữ liệu
data = []

# Bộ đếm số trang và giới hạn số trang
page_count = 1
max_pages = 10  # Số trang tối đa bạn muốn thu thập dữ liệu

while page_count <= max_pages:
    # Tìm tất cả các thẻ chứa thông tin bất động sản
    listings = driver.find_elements(By.CLASS_NAME, 'a13uzdlb')

    for listing in listings:
        title = listing.find_element(By.CLASS_NAME, 'a15fd2pn').text.strip() if listing.find_elements(By.CLASS_NAME, 'a15fd2pn') else 'Không có'
        price = listing.find_element(By.CSS_SELECTOR, 'span[style="color: rgb(229, 25, 59); cursor: inherit; font-size: 16px;"]').text.strip() if listing.find_elements(By.CSS_SELECTOR, 'span[style="color: rgb(229, 25, 59); cursor: inherit; font-size: 16px;"]') else 'Không có'
        
        # Lấy kiểu bất động sản
        details = listing.find_element(By.CLASS_NAME, 'bwq0cbs.tle2ik0').text.strip() if listing.find_elements(By.CLASS_NAME, 'bwq0cbs.tle2ik0') else 'Không có'
        
        # Phân loại kiểu bất động sản
        if "chung cư" in details.lower() or "căn hộ" in details.lower():
            real_estate_type = "Nhà thương mại"
        elif "nhà" in details.lower():
            real_estate_type = "Nhà ở"
        elif "đất" in details.lower():
            real_estate_type = "Công nghiệp"
        else:
            real_estate_type = "Không xác định"

        # Lấy tất cả các thẻ span có class 'bfe6oav'
        area_spans = listing.find_elements(By.CLASS_NAME, 'bfe6oav')
        
        # Lấy giá trên 1 mét vuông và tổng diện tích
        price_per_m2 = area_spans[1].text.strip() if len(area_spans) > 1 else 'Không có'
        total_area = area_spans[2].text.strip() if len(area_spans) > 2 else 'Không có'
        
        # Lấy địa chỉ và chỉ lấy tên thành phố
        address_info = listing.find_element(By.CLASS_NAME, 'c1u6gyxh').text.strip().split('•')[0] if listing.find_elements(By.CLASS_NAME, 'c1u6gyxh') else 'Không có'

        # Thêm thông tin vào danh sách dữ liệu
        data.append({
            'Tiêu đề': title,
            'Giá': price,
            'Giá trên 1 mét vuông': price_per_m2,
            'Tổng diện tích': total_area,
            'Địa chỉ (Tên thành phố)': address_info,
            'Kiểu bất động sản': details,
            'Phân loại': real_estate_type
        })

    print(f"Đã thu thập dữ liệu từ trang {page_count}.")

    # Thử tìm nút "Trang tiếp theo" nếu số trang chưa đạt tới giới hạn
    if page_count < max_pages:
        try:
            # Tìm nút "Trang tiếp theo" và nhấp vào
            next_button = driver.find_element(By.CLASS_NAME, 'Paging_pagingItem__Y3r2u')
            next_button.click()
            
            # Đợi trang tải xong trước khi tiếp tục
            time.sleep(5)
        except NoSuchElementException:
            print("Đã đến trang cuối cùng.")
            break  # Thoát vòng lặp khi không còn nút "Trang tiếp theo"
    else:
        print("Đã đạt tới giới hạn trang.")
        break  # Thoát vòng lặp khi đạt tới trang giới hạn

    # Tăng số trang đã thu thập
    page_count += 1

# Chuyển đổi danh sách dữ liệu thành DataFrame của pandas
df = pd.DataFrame(data)

# Lưu DataFrame vào file CSV
df.to_csv('bat_dong_san_Mua_ban.csv', index=False, encoding='utf-8-sig')
# Hoặc lưu vào file Excel
df.to_excel('bat_dong_san_Mua_ban.xlsx', index=False, engine='openpyxl')

print("Dữ liệu đã được lưu vào file bat_dong_san.csv và bat_dong_san.xlsx")

# Đóng trình duyệt
driver.quit()
