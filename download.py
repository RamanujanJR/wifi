import os
import sys
from selenium import webdriver

def download_chrome_driver():
    print("--- ĐANG TẢI DRIVER CHO GOOGLE CHROME ---")
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=options)
        driver.quit()
        print(">> [OK] Đã tải và cài đặt thành công Driver cho Google Chrome!\n")
        return True
    except Exception as e:
        print(f">> [LỖI] Không thể tải driver cho Chrome. Chi tiết:\n{e}\n")
        return False

def download_edge_driver():
    print("--- ĐANG TẢI DRIVER CHO MICROSOFT EDGE ---")
    try:
        options = webdriver.EdgeOptions()
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')
        driver = webdriver.Edge(options=options)
        driver.quit()
        print(">> [OK] Đã tải và cài đặt thành công Driver cho Microsoft Edge!\n")
        return True
    except Exception as e:
        print(f">> [LỖI] Không thể tải driver cho Edge. Chi tiết:\n{e}\n")
        return False

if __name__ == "__main__":
    print("==================================================")
    print("  CÔNG CỤ TẢI DRIVER OFFLINE CHO SELENIUM (AWING) ")
    print("==================================================")
    print("\nLƯU Ý: Bạn bắt buộc phải ĐANG CÓ MẠNG (qua 4G, hoặc tự đăng nhập WiFi bằng tay)")
    print("để chạy script này. Sau khi tải xong, bạn có thể chạy ngầm offline vĩnh viễn.\n")
    
    input("Hãy chắc chắn đã có mạng ổn định, bấm ENTER để bắt đầu tải...")
    print()
    
    chrome_success = download_chrome_driver()
    edge_success = download_edge_driver()
    
    print("==================================================")
    if chrome_success or edge_success:
        # Đường dẫn thư mục cache mặc định của Selenium trên Windows/macOS/Linux
        cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "selenium")
        print("HOÀN THÀNH!")
        print(f"Các file driver đã được lưu trữ an toàn tại thư mục hệ thống:")
        print(f" -> {cache_dir}")
        print("\nBây giờ bạn có thể ngắt mạng, mở file 'autowifi.py' (bản Selenium V6) để chạy ngầm vĩnh viễn!")
    else:
        print("THẤT BẠI!")
        print("Không tải được driver nào. Hãy chắc chắn bạn đang có kết nối internet thực sự và chạy lại.")
    print("==================================================")
    input("\nBấm ENTER để thoát...")