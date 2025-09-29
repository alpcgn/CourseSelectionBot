# CourseSelectionBot
- The Atılım University course selection bot checks the page every 10 seconds and adds each course to the cart at 0.2 seconds per course. If a course fails, it skips to the next one and retries the failed course in the next cycle until manually stopped.
- For now, it doesn’t work with elective courses.

## 📋 Prerequisites
- Python 3.8+ installed [Pyhton](https://www.python.org/downloads/)
- Google Chrome or another browser (e.g., Firefox)   
- The matching WebDriver for your browser (e.g., [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/))
- Selenium
### Install Selenium
```bash
pip3 install -U selenium
```
## 🚀 Quick Start

### For windows
Open run.bat
### For linux/macOS
```bash
cd path/CourseSelectionBot
python3 interface.py
```

## 📝 Usage
1. Make sure you've all prerequisites installed
2. Start the bot 
3. Enter your username & password  
4. Add your courses as shown in examples !!! ATTENTION Add them with the mandatory courses listed first, otherwise you won't able to select.
6. Press "Start bot" & relax
7. Do not close the bot tab while the bot is running. Click the “Stop Bot” button to stop it after you can close safely. 


## 🔧 Troubleshooting
Here are some common issues you might encounter when using this project with Selenium:

### 1. Selenium is not installed
- **Problem:** Python cannot find the Selenium module.  
- **Solution:** Make sure you have installed Selenium. Run:
```bash
pip install -U selenium
pip3 install -U selenium (for linux)
```
### 2. WebDriver version mismatch
- **Problem:** The browser does not open, or you get an error like “SessionNotCreatedException”.
- **Solution:** Ensure your WebDriver version matches your browser version. For example, if you use Chrome, download the matching ChromeDriver version.

### 3. WebDriver is not in PATH
- **Problem:** Python cannot find the WebDriver executable.
- **Solution:** Make sure the WebDriver executable is in your system PATH, or provide the full path in your script(main.py):
```bash
driver = webdriver.Chrome(executable_path="path/to/chromedriver")
```

### 4. ALSO
In addition, it is very likely that the bot may not work properly, as it has not yet been tested in a real scenario. The bot only opens once, sends a request to the page, and waits 10 seconds it is not a bot that continuously sends requests and tries to access the page. This way, we avoid any legal issues(i hope :D). Whether or not you can access the page still depends on your luck and your hardware performance.

Bunların yanında botun düzgün çalışmaması çok olası henüz gerçek senaryoda test edilme fırsatı bulunamamıştır. Bot sadece 10 saniyede bir kere  sayfaya istek atıp beklemektedir sürekli istek atıp girmeye çalışan bir bot değildir ki bu da yasal olarak sıkıntı yaratır. Girip girememeniz yine sizin şansınıza ve donanım gücünüze bağlıdır
