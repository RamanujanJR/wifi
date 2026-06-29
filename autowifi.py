import time
import datetime
import shutil
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

TEST_URL = "https://clients3.google.com/generate_204"
ROUTER_URL = "http://192.168.200.1/login"

def check_internet():
    try:
        return requests.get(TEST_URL, timeout=3).status_code == 204
    except:
        return False

def reconnect_wifi():
    print(f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] Rớt mạng! Đang kết nối lại ngầm...")
    
    options = webdriver.ChromeOptions()
    
    # 1. Định vị trình duyệt (Dùng shutil như đã fix ở bản trước)
    chromium_path = shutil.which("chromium-browser") or shutil.which("chromium")
    options.binary_location = chromium_path
    
    options.add_argument('--headless=new')
    
    # ==============================================================
    # VŨ KHÍ TỐI THƯỢNG CHỐNG LẠI ANDROID PHANTOM PROCESS KILLER
    # ==============================================================
    options.add_argument('--single-process') # Ép chạy 1 tiến trình duy nhất (Cứu tinh của Termux)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer') # Tắt bộ giả lập đồ họa 
    options.add_argument('--disable-features=VizDisplayCompositor') # Tắt bộ dựng hình
    # ==============================================================
    
    # Tắt bảo mật chặn mạng PNA
    options.add_argument('--disable-web-security') 
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--disable-features=IsolateOrigins,site-per-process,BlockInsecurePrivateNetworkRequests')
    
    # Xóa dấu vết Bot
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    chromedriver_path = shutil.which("chromedriver")
    
    # FIX LỖI TIMEOUT DO LOCALHOST CỦA TERMUX
    service = Service(chromedriver_path, service_args=["--port=0", "--host=127.0.0.1"])
    
    driver = webdriver.Chrome(service=service, options=options)
    try:
        # Tiêm mã xóa cờ Webdriver
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        })
        
        driver.get(ROUTER_URL)
        print("-> Đang chờ trang tải và đếm ngược quảng cáo (Sẽ mất khoảng 5-10s)...")
        
        # Vòng lặp soi nút (Giống Tampermonkey)
        clicked = False
        for _ in range(30):
            time.sleep(1)
            try:
                btn = driver.find_element(By.ID, "connectToInternet")
                btn_class = btn.get_attribute("class")
                if btn_class and "disabled" not in btn_class:
                    # Bấm nút và kích hoạt hàm JS song song để đảm bảo ăn 100%
                    driver.execute_script("""
                        arguments[0].click();
                        try { slideBannerFunctions.connectToWifi(); } catch(e) {}
                    """, btn)
                    print("-> Đã Click nút! Đang chờ Router mở mạng...")
                    clicked = True
                    break
            except:
                pass
                
        if not clicked:
            print("-> [Lỗi] Quá 30s không tìm thấy nút kết nối.")
            return

        # Kiên nhẫn đợi mạng thông (Vì PNA đã tắt, lệnh gửi đi sẽ thông suốt)
        for _ in range(15):
            time.sleep(1)
            if check_internet():
                print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] KẾT NỐI THÀNH CÔNG! Đã chạy ngầm hoàn toàn.")
                return
        
        print("-> [Lỗi] Đã click nhưng mạng vẫn chưa thông.")
        
    except Exception as e:
        print(f"-> [Lỗi]: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    print("=========================================")
    print("  AWING AUTO-CONNECT FOR TERMUX (ANDROID)")
    print("=========================================")
    print("Mã nguồn đã tối ưu hóa cho Mobile. Đang giám sát mạng...")
    
    if check_internet():
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Đang có mạng. Tool sẽ trực chờ...")
        
    while True:
        if not check_internet():
            reconnect_wifi()
        time.sleep(5)
