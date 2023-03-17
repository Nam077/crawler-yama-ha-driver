from selenium import webdriver
from selenium.webdriver.common.by import By

# Khởi tạo trình duyệt
driver = webdriver.Edge()

# Mở trang web Google
driver.get("https://www.google.com")

# Tìm phần tử ô tìm kiếm bằng ID và gửi từ khóa tìm kiếm
search_box = driver.find_elements(By.NAME, "q")[0]
search_box.send_keys('Bác hồ sinh ngày bao nhiêu')
# Nhấn nút tìm kiếm
search_box.submit()

# Chờ đến khi trang được tải hoàn tất
driver.implicitly_wait(10)

# Tìm kết quả đầu tiên và nhấp vào liên kết
result = driver.find_elements(By.CLASS_NAME, 'g')
for r in result:
    print(r.text)
