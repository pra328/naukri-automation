from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver # Import WebDriver for type hinting
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By # Keep By import if used in functions
import time
import os
from datetime import datetime

try:
    import undetected_chromedriver as uc
except Exception:
    uc = None


def _find_chrome_binary() -> str | None:
    """Return the installed Chrome/Chromium binary path, if present."""
    candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
    ]
    for path in candidates:
        if path and os.path.exists(path):
            return path
    return None


def switch_to_new_window(driver: WebDriver, timeout: int = 10) -> None:
    """
    Switches to a new window/tab that opens after clicking a link.
    
    Args:
        driver: The webdriver instance.
        timeout: Maximum time to wait for new window.
    """
    original_window = driver.current_window_handle
    wait = WebDriverWait(driver, timeout)
    
    # Wait for new window to open
    wait.until(lambda driver: len(driver.window_handles) > 1)
    
    # Switch to the new window
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break


def setup_driver() -> WebDriver:
    """
    Sets up and returns a configured Chrome webdriver instance.

    Returns:
        A configured Chrome webdriver instance.
    """
    import os
    import platform
    import tempfile
    
    try:
        # Detect if we're running in CI/GitHub Actions
        is_ci = os.getenv('CI') == 'true' or os.getenv('GITHUB_ACTIONS') == 'true'
        
        # Chrome options for better compatibility
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--no-default-browser-check")
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--disable-extensions")
        
        # Advanced stealth Chrome options to avoid detection
        # GitHub Actions should use a virtual display instead of headless mode to reduce anti-bot detection.
        if is_ci:
            print("🤖 Detected CI environment - using virtual display mode")
            chrome_options.add_argument("--disable-software-rasterizer")
            chrome_options.add_argument("--disable-setuid-sandbox")
            chrome_options.add_argument("--remote-debugging-port=0")
        else:
            print("💻 Running in local environment - using normal Chrome mode")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        # chrome_options.add_argument("--remote-debugging-port=9222")  # Commented out to avoid port conflicts
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        
        # Enhanced anti-detection measures
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions-file-access-check")
        chrome_options.add_argument("--disable-extensions-http-throttling")
        chrome_options.add_argument("--disable-extensions-except")
        chrome_options.add_argument("--disable-component-extensions-with-background-pages")
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--disable-sync")
        chrome_options.add_argument("--disable-translate")
        chrome_options.add_argument("--hide-scrollbars")
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-permissions-api")
        chrome_options.add_argument("--disable-presentation-api")
        chrome_options.add_argument("--disable-print-preview")
        chrome_options.add_argument("--disable-speech-api")
        chrome_options.add_argument("--disable-file-system")
        chrome_options.add_argument("--disable-client-side-phishing-detection")
        chrome_options.add_argument("--disable-component-update")
        chrome_options.add_argument("--disable-domain-reliability")
        chrome_options.add_argument("--disable-features=TranslateUI,BlinkGenPropertyTrees")
        chrome_options.add_argument("--disable-ipc-flooding-protection")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-background-networking")
        chrome_options.add_argument("--disable-breakpad")
        chrome_options.add_argument("--disable-client-side-phishing-detection")
        chrome_options.add_argument("--disable-component-extensions-with-background-pages")
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-features=TranslateUI")
        chrome_options.add_argument("--disable-hang-monitor")
        chrome_options.add_argument("--disable-ipc-flooding-protection")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-prompt-on-repost")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-sync")
        chrome_options.add_argument("--disable-translate")
        chrome_options.add_argument("--disable-windows10-custom-titlebar")
        chrome_options.add_argument("--metrics-recording-only")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--safebrowsing-disable-auto-update")
        chrome_options.add_argument("--password-store=basic")
        chrome_options.add_argument("--use-mock-keychain")

        chrome_binary = _find_chrome_binary()
        if chrome_binary:
            chrome_options.binary_location = chrome_binary
            print(f"📍 Using Chrome binary: {chrome_binary}")
        
        # Randomize user agent from a pool of real browsers
        import random
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0"
        ]
        selected_user_agent = random.choice(user_agents)
        chrome_options.add_argument(f"--user-agent={selected_user_agent}")
        
        # Randomize language and locale
        languages = ["en-US,en;q=0.9", "en-GB,en;q=0.9", "en-CA,en;q=0.9", "en-AU,en;q=0.9"]
        selected_language = random.choice(languages)
        chrome_options.add_argument(f"--accept-language={selected_language}")
        
        # Additional headers
        chrome_options.add_argument("--accept-encoding=gzip, deflate, br")
        chrome_options.add_argument("--accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7")
        chrome_options.add_argument("--sec-ch-ua=\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"")
        chrome_options.add_argument("--sec-ch-ua-mobile=?0")
        chrome_options.add_argument("--sec-ch-ua-platform=\"Windows\"")
        chrome_options.add_argument("--sec-fetch-dest=document")
        chrome_options.add_argument("--sec-fetch-mode=navigate")
        chrome_options.add_argument("--sec-fetch-site=none")
        chrome_options.add_argument("--sec-fetch-user=?1")
        chrome_options.add_argument("--upgrade-insecure-requests=1")
        
        print("🌐 Using cloud-optimized Chrome configuration")
        
        # Start Chrome with robust error handling
        driver = None
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                print(f"🔍 Attempting to start Chrome (attempt {attempt + 1}/{max_retries})...")
                
                if is_ci and uc is not None:
                    print("🔐 Using undetected-chromedriver in CI environment")
                    driver = uc.Chrome(options=chrome_options)
                else:
                    # Create service with better configuration
                    service = Service(ChromeDriverManager().install())
                    
                    # Create driver with explicit service (don't start service manually)
                    driver = webdriver.Chrome(service=service, options=chrome_options)
                
                # Set timeouts for better stability
                driver.set_page_load_timeout(30)
                driver.implicitly_wait(10)
                
                # Test the session by getting the current URL
                driver.get("about:blank")
                print("✅ Chrome started successfully and session is valid")
                break
                
            except Exception as e:
                print(f"⚠️ Chrome startup attempt {attempt + 1} failed: {e}")
                if driver:
                    try:
                        driver.quit()
                    except:
                        pass
                    driver = None
                if 'service' in locals():
                    try:
                        service.stop()
                    except:
                        pass
                
                if attempt < max_retries - 1:
                    print("🔄 Retrying with different configuration...")
                    time.sleep(2)
                else:
                    print("❌ All Chrome startup attempts failed")
                    raise Exception(f"Failed to start Chrome after {max_retries} attempts: {e}")
        
        if not driver:
            raise Exception("Failed to create Chrome driver instance")
        
        # Execute advanced stealth scripts to avoid detection
        try:
            print("🕵️ Applying advanced stealth measures...")
            
            # Comprehensive stealth script
            stealth_script = """
            // Override automation indicators (fixed to avoid redefinition error)
            try {
                Object.defineProperty(navigator, 'webdriver', {get: () => false, configurable: true});
            } catch(e) {
                // Property already defined, skip
            }
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
            Object.defineProperty(navigator, 'permissions', {get: () => ({query: () => Promise.resolve({state: 'granted'})})});
            
            // Override Chrome runtime
            if (window.chrome && window.chrome.runtime) {
                Object.defineProperty(window.chrome.runtime, 'onConnect', {get: () => undefined});
                Object.defineProperty(window.chrome.runtime, 'onMessage', {get: () => undefined});
            }
            
            // Override automation flags
            try {
                Object.defineProperty(navigator, 'automation', {get: () => false, configurable: true});
            } catch(e) {
                // Property already defined, skip
            }
            
            // Mock realistic plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => ({
                    length: 3,
                    0: {name: 'Chrome PDF Plugin', description: 'Portable Document Format'},
                    1: {name: 'Chrome PDF Viewer', description: 'Portable Document Format'},
                    2: {name: 'Native Client', description: 'Native Client Executable'}
                })
            });
            
            // Mock realistic screen properties
            Object.defineProperty(screen, 'availHeight', {get: () => 1040});
            Object.defineProperty(screen, 'availWidth', {get: () => 1920});
            Object.defineProperty(screen, 'colorDepth', {get: () => 24});
            Object.defineProperty(screen, 'height', {get: () => 1080});
            Object.defineProperty(screen, 'width', {get: () => 1920});
            
            // Mock realistic timezone
            Object.defineProperty(Intl.DateTimeFormat.prototype, 'resolvedOptions', {
                value: function() { return {timeZone: 'America/New_York'}; }
            });
            
            // Override getParameter to hide automation
            const originalGetParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) {
                    return 'Intel Inc.';
                }
                if (parameter === 37446) {
                    return 'Intel(R) Iris(TM) Graphics 6100';
                }
                return originalGetParameter.call(this, parameter);
            };
            
            // Mock realistic connection
            Object.defineProperty(navigator, 'connection', {
                get: () => ({
                    effectiveType: '4g',
                    rtt: 50,
                    downlink: 10
                })
            });
            
            // Override Date to appear more human
            const originalDate = Date;
            Date = class extends originalDate {
                constructor(...args) {
                    if (args.length === 0) {
                        super(originalDate.now() + Math.random() * 1000);
                    } else {
                        super(...args);
                    }
                }
            };
            
            // Mock realistic battery API
            if (navigator.getBattery) {
                navigator.getBattery = () => Promise.resolve({
                    charging: true,
                    chargingTime: 0,
                    dischargingTime: Infinity,
                    level: 0.8
                });
            }
            
            // Override canvas fingerprinting
            const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
            HTMLCanvasElement.prototype.toDataURL = function() {
                const context = this.getContext('2d');
                if (context) {
                    context.fillStyle = 'rgba(255, 255, 255, 0.01)';
                    context.fillRect(0, 0, 1, 1);
                }
                return originalToDataURL.apply(this, arguments);
            };
            
            // Mock realistic hardware concurrency
            Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8});
            
            // Override notification permission
            Object.defineProperty(Notification, 'permission', {get: () => 'default'});
            
            // Mock realistic memory
            Object.defineProperty(navigator, 'deviceMemory', {get: () => 8});
            
            // Override speech synthesis
            if (window.speechSynthesis) {
                Object.defineProperty(window.speechSynthesis, 'getVoices', {
                    value: () => [
                        {name: 'Google US English', lang: 'en-US', default: true},
                        {name: 'Microsoft David Desktop', lang: 'en-US'},
                        {name: 'Microsoft Zira Desktop', lang: 'en-US'}
                    ]
                });
            }
            
            // Remove automation indicators from window
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            
            // Mock realistic touch support
            Object.defineProperty(navigator, 'maxTouchPoints', {get: () => 0});
            
            // Override geolocation
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition = () => {};
                navigator.geolocation.watchPosition = () => {};
            }
            
            console.log('Stealth measures applied successfully');
            """
            
            driver.execute_script(stealth_script)
            print("✅ Advanced stealth measures applied successfully")
            
        except Exception as e:
            print(f"⚠️ Some stealth measures failed: {e}")
            pass  # Continue even if stealth measures fail
        
        # Navigate to Naukri with session validation and retry logic
        max_nav_retries = 3
        for nav_attempt in range(max_nav_retries):
            try:
                print(f"🌐 Navigating to Naukri.com (attempt {nav_attempt + 1}/{max_nav_retries})...")
                
                # Add human-like random delay to avoid rate limiting
                import random
                delay = random.uniform(3, 8)  # Longer, more human-like delays
                print(f"⏱️ Waiting {delay:.1f} seconds (human-like delay)...")
                time.sleep(delay)
                
                # Simulate human-like mouse movement before navigation
                try:
                    from selenium.webdriver.common.action_chains import ActionChains
                    actions = ActionChains(driver)
                    # Random mouse movements
                    for _ in range(random.randint(2, 5)):
                        x_offset = random.randint(-100, 100)
                        y_offset = random.randint(-100, 100)
                        actions.move_by_offset(x_offset, y_offset)
                        actions.perform()
                        time.sleep(random.uniform(0.1, 0.3))
                except:
                    pass  # Continue if mouse simulation fails
                
                driver.get("https://www.naukri.com/")
                
                # Simulate human-like scrolling behavior
                try:
                    import random
                    scroll_pause_time = random.uniform(0.5, 2.0)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
                    time.sleep(scroll_pause_time)
                    driver.execute_script("window.scrollTo(0, 0);")
                    time.sleep(scroll_pause_time)
                except:
                    pass
                
                # Validate session is still active
                current_url = driver.current_url
                page_title = driver.title
                print(f"📍 Current URL: {current_url}")
                print(f"📄 Page Title: {page_title}")
                
                # Check if we got blocked
                if "Access Denied" in page_title or "blocked" in page_title.lower():
                    print(f"⚠️ Access denied on attempt {nav_attempt + 1}")
                    if nav_attempt < max_nav_retries - 1:
                        print("🔄 Retrying with different approach...")
                        # Longer wait with exponential backoff
                        wait_time = 15 + (nav_attempt * 10)
                        print(f"⏱️ Waiting {wait_time} seconds before retry...")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise Exception("Access denied - website is blocking automated requests")
                
                # Wait for page to load with human-like timing
                load_time = random.uniform(3, 7)
                print(f"⏱️ Waiting {load_time:.1f} seconds for page to load...")
                time.sleep(load_time)
                break
                
            except Exception as nav_error:
                print(f"⚠️ Navigation attempt {nav_attempt + 1} failed: {nav_error}")
                if nav_attempt < max_nav_retries - 1:
                    print("🔄 Retrying navigation...")
                    retry_delay = random.uniform(5, 10)
                    print(f"⏱️ Waiting {retry_delay:.1f} seconds before retry...")
                    time.sleep(retry_delay)
                else:
                    raise nav_error
        
        # Try to find and click login button with multiple selectors
        print("🔍 Looking for login button...")
        
        # Wait for page to fully load
        time.sleep(5)
        
        # Try multiple selectors for login button
        login_selectors = [
            (By.LINK_TEXT, "Login"),
            (By.PARTIAL_LINK_TEXT, "Login"),
            (By.XPATH, "//a[contains(text(), 'Login')]"),
            (By.XPATH, "//a[contains(text(), 'login')]"),
            (By.XPATH, "//button[contains(text(), 'Login')]"),
            (By.XPATH, "//button[contains(text(), 'login')]"),
            (By.XPATH, "//a[@href*='login']"),
            (By.XPATH, "//button[@class*='login']"),
            (By.CSS_SELECTOR, "a[href*='login']"),
            (By.CSS_SELECTOR, "button[class*='login']")
        ]
        
        login_button = None
        for selector_type, selector_value in login_selectors:
            try:
                print(f"🔍 Trying selector: {selector_type} = '{selector_value}'")
                login_button = driver.find_element(selector_type, selector_value)
                print(f"✅ Found login button with: {selector_type} = '{selector_value}'")
                break
            except:
                continue
        
        if not login_button:
            print("❌ Could not find login button with any selector")
            print("🔄 Trying direct navigation to login page...")
            
            # Try direct navigation to login page
            try:
                driver.get("https://www.naukri.com/nlogin/login")
                time.sleep(5)
                print("✅ Navigated directly to login page")
            except Exception as nav_error:
                print(f"❌ Direct navigation failed: {nav_error}")
                print("🔍 Current page source preview:")
                print(driver.page_source[:500] + "...")
                raise Exception("Login button not found and direct navigation failed")
        else:
            # Click the login button
            login_button.click()
            print("✅ Login button clicked successfully")
            time.sleep(3)
        
        print("🚀 Driver setup completed successfully")
        return driver
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        if 'driver' in locals() and driver:
            try:
                driver.quit()
            except:
                pass
        raise Exception(f"Failed to setup driver: {e}")

def login_with_google(driver: WebDriver, email: str) -> None:
    """
    Logs in to Naukri using Google OAuth authentication.

    Args:
        driver: The webdriver instance.
        email: The user's Google email address.
    """
    wait = WebDriverWait(driver, 15)
    
    try:
        # Look for Google login button
        google_login_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Google') or contains(@class, 'google') or contains(@id, 'google')]"))
        )
        google_login_button.click()
        print("🔍 Clicked Google login button")
        time.sleep(3)
        
        # Handle Google login popup/redirect
        # Check if new window opened (popup) or if it's a redirect
        if len(driver.window_handles) > 1:
            print("🔄 Switching to Google login popup window")
            switch_to_new_window(driver)
        
        # Wait for Google login page to load
        time.sleep(3)
        
        # Check if Google account selection page appears (user already logged in)
        try:
            # Look for account selection elements
            account_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'account') or contains(@class, 'profile') or contains(@class, 'user')]")
            if account_elements:
                print("🔍 Found Google account selection page")
                # Look for the specific email account or click the first available account
                try:
                    # Try to find account with matching email
                    target_account = driver.find_element(By.XPATH, f"//div[contains(text(), '{email}')]")
                    target_account.click()
                    print(f"✅ Selected account: {email}")
                except:
                    # If specific email not found, click the first available account
                    first_account = driver.find_element(By.XPATH, "//div[contains(@class, 'account') or contains(@class, 'profile')]")
                    first_account.click()
                    print("✅ Selected first available Google account")
                
                time.sleep(3)
                
                # Check if we need to click "Continue" or similar button
                try:
                    continue_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Continue') or contains(text(), 'Next') or contains(text(), 'Allow')]")
                    continue_button.click()
                    print("✅ Clicked Continue/Allow button")
                    time.sleep(3)
                except:
                    print("ℹ️ No continue button found, proceeding...")
                
                # Wait for redirect back to Naukri
                time.sleep(5)
                
                # If we're in a popup window, switch back to main window
                if len(driver.window_handles) > 1:
                    print("🔄 Switching back to main Naukri window")
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(2)
                
                # Navigate to profile page
                driver.get("https://www.naukri.com/mnjuser/profile")
                time.sleep(5)
                print("🎯 Navigated to profile page")
                return
                
        except Exception as account_error:
            print(f"ℹ️ No account selection found: {account_error}")
        
        # If no account selection, proceed with manual login
        print("🔐 Proceeding with manual Google login...")
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
        
        # Enter email
        email_input = driver.find_element(By.XPATH, "//input[@type='email']")
        email_input.clear()
        email_input.send_keys(email)
        print(f"📧 Entered email: {email}")
        
        # Click Next button
        next_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Next') or contains(text(), 'next')]")
        next_button.click()
        time.sleep(3)
        
        # For Google login, we might need to handle 2FA or password
        # This is simplified - in real scenario, you might need to handle 2FA
        print("⚠️ Manual Google login requires additional steps (2FA, password, etc.)")
        print("💡 Consider using existing Chrome session for automatic login")
        
        # Wait for redirect back to Naukri
        time.sleep(5)
        
        # If we're in a popup window, switch back to main window
        if len(driver.window_handles) > 1:
            print("🔄 Switching back to main Naukri window")
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(2)
        
        # Navigate to profile page
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(5)
        print("🎯 Navigated to profile page")
        
    except Exception as e:
        print(f"❌ Google login failed: {e}")
        raise


def login_with_email_password(driver: WebDriver, email: str, password: str) -> None:
    """
    Logs in to Naukri using email and password.

    Args:
        driver: The webdriver instance.
        email: The user's email address.
        password: The user's password.
    """
    import random
    wait = WebDriverWait(driver, 15)
    
    try:
        # Wait for login page to load
        time.sleep(3)
        
        # Check if we're on OTP tab and switch to email/password tab
        print("🔍 Checking which login tab is active...")
        
        # Look for OTP-related elements that indicate we're on OTP tab
        otp_indicators = [
            "//input[@type='tel' or @name='mobile' or contains(@placeholder, 'Mobile') or contains(@placeholder, 'Phone')]",
            "//div[contains(text(), 'OTP')]",
            "//button[contains(text(), 'Get OTP') or contains(text(), 'Send OTP')]",
            "//div[contains(@class, 'otp') or contains(@id, 'otp')]"
        ]
        
        is_otp_tab = False
        for indicator in otp_indicators:
            try:
                elements = driver.find_elements(By.XPATH, indicator)
                if elements and any(el.is_displayed() for el in elements):
                    print("⚠️ OTP tab detected - switching to email/password tab...")
                    is_otp_tab = True
                    break
            except:
                continue
        
        # If on OTP tab, look for button/tab to switch to email/password
        if is_otp_tab:
            print("🔄 Looking for email/password tab switch button...")
            # Comprehensive selectors for switching to email/password tab
            switch_selectors = [
                "//button[contains(text(), 'Login with Password') or contains(text(), 'Use Password')]",
                "//a[contains(text(), 'Login with Password') or contains(text(), 'Use Password')]",
                "//span[contains(text(), 'Login with Password') or contains(text(), 'Use Password')]",
                "//button[contains(text(), 'Email') and not(contains(text(), 'OTP'))]",
                "//a[contains(text(), 'Email') and not(contains(text(), 'OTP'))]",
                "//div[contains(@class, 'tab') and contains(text(), 'Email')]",
                "//div[contains(@class, 'tab') and contains(text(), 'Password')]",
                "//button[contains(@class, 'password')]",
                "//a[contains(@class, 'password')]",
                "//div[@role='tab' and contains(text(), 'Email') or contains(text(), 'Password')]",
                "//button[@role='tab' and contains(text(), 'Email') or contains(text(), 'Password')]",
                # Naukri-specific patterns
                "//div[contains(@class, 'emailLogin') or contains(@class, 'email-login')]",
                "//button[contains(@class, 'emailLogin') or contains(@class, 'email-login')]"
            ]
            
            switched = False
            for selector in switch_selectors:
                try:
                    elements = driver.find_elements(By.XPATH, selector)
                    for el in elements:
                        if el.is_displayed() and el.is_enabled():
                            print(f"✅ Found email/password switch button: {selector}")
                            # Scroll into view if needed
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
                            time.sleep(1)
                            el.click()
                            print("✅ Clicked email/password tab")
                            time.sleep(3)  # Wait for tab switch
                            switched = True
                            break
                    if switched:
                        break
                except Exception as e:
                    continue
            
            if not switched:
                print("⚠️ Could not find email/password tab switch button - proceeding anyway...")
        
        # Double-check: Verify we're NOT on OTP tab by checking for email input field
        print("🔍 Verifying we're on email/password tab...")
        email_field_found = False
        for selector in ["//input[@name='email']", "//input[@type='text' and contains(@placeholder, 'Email')]", "//input[@id='email']"]:
            try:
                elements = driver.find_elements(By.XPATH, selector)
                if elements and any(el.is_displayed() for el in elements):
                    email_field_found = True
                    print("✅ Email input field visible - on correct tab")
                    break
            except:
                continue
        
        if not email_field_found:
            print("⚠️ Email field not found - might still be on OTP tab")

        print("🔍 Looking for email input field...")
        # Find email input field with multiple possible selectors
        email_selectors = [
            "//input[@type='text']",
            "//input[@name='email']", 
            "//input[@id='email']",
            "//input[@placeholder='Email ID']",
            "//input[contains(@class, 'email')]"
        ]
        
        email_input = None
        for selector in email_selectors:
            try:
                email_input = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
                print(f"✅ Found email input with selector: {selector}")
                break
            except:
                continue
        
        if not email_input:
            print("❌ Could not find email input field")
            print("🔍 Current page URL:", driver.current_url)
            print("🔍 Page title:", driver.title)
            raise Exception("Email input field not found")
        
        # Simulate human-like typing for email
        email_input.clear()
        time.sleep(random.uniform(0.5, 1.5))  # Pause before typing
        
        # Type email character by character with random delays
        for char in email:
            email_input.send_keys(char)
            time.sleep(random.uniform(0.05, 0.2))  # Random typing speed
        
        print(f"📧 Entered email: {email}")
        
        # Simulate human pause between fields
        time.sleep(random.uniform(1, 3))
        
        print("🔍 Looking for password input field...")
        # Find password input field
        password_input = driver.find_element(By.XPATH, "//input[@type='password']")
        
        # Simulate human-like password entry
        password_input.clear()
        time.sleep(random.uniform(0.5, 1.5))  # Pause before typing
        
        # Type password character by character with random delays
        for char in password:
            password_input.send_keys(char)
            time.sleep(random.uniform(0.08, 0.25))  # Slightly slower for password
        
        print("🔒 Entered password")
        
        # Simulate human pause before clicking login
        time.sleep(random.uniform(2, 4))
        
        print("🔍 Looking for login button...")
        # Click login button with multiple possible selectors
        login_selectors = [
            "//button[contains(text(), 'Login')]",
            "//button[contains(text(), 'Sign In')]",
            "//input[@type='submit']",
            "//button[@type='submit']"
        ]
        
        login_button = None
        for selector in login_selectors:
            try:
                login_button = driver.find_element(By.XPATH, selector)
                print(f"✅ Found login button with selector: {selector}")
                break
            except:
                continue
        
        if not login_button:
            print("❌ Could not find login button")
            raise Exception("Login button not found")
        
        login_button.click()
        print("✅ Clicked login button")
        
        # Wait for login to process with dynamic waiting
        print("⏱️ Waiting for login to complete...")
        max_wait_time = 30  # Maximum wait time in seconds
        wait_interval = 2   # Check every 2 seconds
        
        for wait_attempt in range(max_wait_time // wait_interval):
            time.sleep(wait_interval)
            
            # Check if we've been redirected away from login page
            current_url = driver.current_url
            page_title = driver.title
            
            # Look for success indicators
            if ("login" not in current_url.lower() and 
                ("mynaukri" in current_url.lower() or 
                 "profile" in current_url.lower() or 
                 "dashboard" in current_url.lower() or
                 "homepage" in current_url.lower())):
                print(f"✅ Login completed successfully after {wait_attempt * wait_interval} seconds")
                print(f"📍 Redirected to: {current_url}")
                return  # Exit early if login is successful
            
            # Check for error messages
            try:
                error_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'error') or contains(text(), 'Invalid') or contains(text(), 'Wrong')]")
                if error_elements and error_elements[0].text.strip():
                    print(f"❌ Login error detected: {error_elements[0].text}")
                    raise Exception(f"Login failed: {error_elements[0].text}")
            except:
                pass
            
            print(f"⏱️ Still waiting for login... ({wait_attempt * wait_interval}s elapsed)")
        
        print("⚠️ Login timeout - proceeding with validation...")
        
        # Check for login success/failure with comprehensive validation
        print("🔍 Validating login status...")
        
        # First, check if we can see user-specific elements (indicating successful login)
        try:
            user_indicators = [
                "//a[contains(@href, 'mnjuser')]",
                "//div[contains(@class, 'user')]",
                "//span[contains(@class, 'user')]",
                "//div[contains(text(), 'Welcome')]",
                "//a[contains(text(), 'Profile')]",
                "//a[contains(text(), 'Dashboard')]"
            ]
            
            user_found = False
            for indicator in user_indicators:
                try:
                    elements = driver.find_elements(By.XPATH, indicator)
                    if elements:
                        print(f"✅ Found user indicator: {indicator}")
                        user_found = True
                        break
                except:
                    continue
            
            if user_found:
                print("🎯 Login appears successful - user elements detected")
        except:
            pass
        
        # Check session cookies and validate authentication
        try:
            print("🍪 Checking session cookies...")
            cookies = driver.get_cookies()
            session_cookies = [cookie for cookie in cookies if 'session' in cookie.get('name', '').lower() or 'auth' in cookie.get('name', '').lower() or 'login' in cookie.get('name', '').lower()]
            
            if session_cookies:
                print(f"✅ Found {len(session_cookies)} session cookies")
                for cookie in session_cookies:
                    print(f"   - {cookie['name']}: {cookie['value'][:20]}...")
            else:
                print("⚠️ No session cookies found - authentication may not be complete")
                
            # Check if we have naukri-specific cookies
            naukri_cookies = [cookie for cookie in cookies if 'naukri' in cookie.get('name', '').lower() or 'mnj' in cookie.get('name', '').lower()]
            if naukri_cookies:
                print(f"✅ Found {len(naukri_cookies)} Naukri-specific cookies")
            else:
                print("⚠️ No Naukri-specific cookies found")
                
        except Exception as cookie_error:
            print(f"⚠️ Could not check cookies: {cookie_error}")
        
        # Try to access a simple authenticated page first
        try:
            print("🔍 Testing session with simple authenticated request...")
            driver.get("https://www.naukri.com/mnjuser/homepage")
            time.sleep(3)
            
            test_url = driver.current_url
            test_title = driver.title
            print(f"📍 Test URL: {test_url}")
            print(f"📄 Test Title: {test_title}")
            
            if "login" not in test_url.lower() and "mynaukri" in test_title.lower():
                print("✅ Session is valid - can access authenticated pages")
                return  # Exit early if session is working
            else:
                print("⚠️ Session test failed - still redirected to login")
                
        except Exception as test_error:
            print(f"⚠️ Session test failed: {test_error}")
        
        # Check for error messages first
        error_found = False
        try:
            # Look for various error message patterns
            error_selectors = [
                "//div[contains(@class, 'error')]",
                "//div[contains(@class, 'alert')]",
                "//span[contains(@class, 'error')]",
                "//div[contains(text(), 'Invalid')]",
                "//div[contains(text(), 'Wrong')]",
                "//div[contains(text(), 'incorrect')]",
                "//div[contains(text(), 'failed')]",
                "//div[contains(text(), 'blocked')]"
            ]
            
            for selector in error_selectors:
                try:
                    error_elements = driver.find_elements(By.XPATH, selector)
                    for error_element in error_elements:
                        error_text = error_element.text.strip()
                        if error_text and len(error_text) > 0:
                            print(f"❌ Login error detected: {error_text}")
                            error_found = True
                            break
                    if error_found:
                        break
                except:
                    continue
        except:
            pass
        
        # Check current URL and page content
        current_url = driver.current_url
        page_title = driver.title
        print(f"📍 Current URL after login: {current_url}")
        print(f"📄 Page Title after login: {page_title}")
        
        # Check if we're still on login page or got redirected back
        if "login" in current_url.lower() or "signin" in current_url.lower():
            print("⚠️ Still on login page - checking for redirect issues...")
            
            # Check if this is a redirect loop with malformed URL
            if "URL=//" in current_url:
                print("🔧 Detected malformed redirect URL - attempting to fix...")
                # Extract the target URL and fix it
                try:
                    if "URL=//" in current_url:
                        # Extract the malformed URL and fix it
                        malformed_url = current_url.split("URL=")[1]
                        if malformed_url.startswith("//"):
                            fixed_url = "https:" + malformed_url
                            print(f"🔧 Fixed URL: {fixed_url}")
                            driver.get(fixed_url)
                            time.sleep(5)
                            
                            # Check if we can access the profile now
                            new_url = driver.current_url
                            if "login" not in new_url.lower() and "signin" not in new_url.lower():
                                print("✅ Successfully fixed redirect and accessed profile")
                                error_found = False
                            else:
                                print("❌ Still redirected to login after URL fix")
                                error_found = True
                        else:
                            error_found = True
                    else:
                        error_found = True
                except Exception as fix_error:
                    print(f"❌ Failed to fix redirect URL: {fix_error}")
                    error_found = True
            else:
                error_found = True
        
        # Check for CAPTCHA or additional verification with comprehensive detection
        try:
            print("🔍 Checking for CAPTCHA and verification challenges...")
            
            # Multiple CAPTCHA detection patterns
            captcha_selectors = [
                "//div[contains(@class, 'captcha')]",
                "//div[contains(@id, 'captcha')]",
                "//img[contains(@src, 'captcha')]",
                "//img[contains(@alt, 'captcha')]",
                "//div[contains(@class, 'recaptcha')]",
                "//div[contains(@id, 'recaptcha')]",
                "//iframe[contains(@src, 'recaptcha')]",
                "//div[contains(text(), 'captcha')]",
                "//div[contains(text(), 'verification')]",
                "//div[contains(text(), 'robot')]",
                "//div[contains(text(), 'human')]",
                "//div[contains(@class, 'challenge')]",
                "//div[contains(@class, 'verification')]"
            ]
            
            captcha_found = False
            for selector in captcha_selectors:
                try:
                    elements = driver.find_elements(By.XPATH, selector)
                    if elements:
                        print(f"⚠️ CAPTCHA/Verification detected with selector: {selector}")
                        captcha_found = True
                        break
                except:
                    continue
            
            if captcha_found:
                print("🚫 CAPTCHA detected - this requires manual intervention")
                print("💡 Possible solutions:")
                print("   1. Use a different login method (Google OAuth)")
                print("   2. Try logging in manually first to establish session")
                print("   3. Use a residential proxy or VPN")
                print("   4. Wait and retry later (CAPTCHA may be temporary)")
                
                # Try to suggest switching to Google OAuth
                print("🔄 Attempting to switch to Google OAuth login...")
                try:
                    # Look for Google login button
                    google_login_selectors = [
                        "//button[contains(text(), 'Google')]",
                        "//a[contains(text(), 'Google')]",
                        "//div[contains(@class, 'google')]",
                        "//button[contains(@class, 'google')]",
                        "//a[contains(@href, 'google')]"
                    ]
                    
                    google_button_found = False
                    for selector in google_login_selectors:
                        try:
                            google_button = driver.find_element(By.XPATH, selector)
                            print(f"✅ Found Google login button: {selector}")
                            google_button.click()
                            print("🔄 Clicked Google login button")
                            time.sleep(3)
                            google_button_found = True
                            break
                        except:
                            continue
                    
                    if google_button_found:
                        print("🎯 Switched to Google OAuth - this may bypass CAPTCHA")
                        # Let the Google login function handle the rest
                        return
                    else:
                        print("❌ No Google login option found")
                        
                except Exception as google_error:
                    print(f"⚠️ Failed to switch to Google OAuth: {google_error}")
                
                # Raise a specific CAPTCHA exception that can be caught by the main login function
                raise Exception("CAPTCHA detected - manual intervention required")
            else:
                print("✅ No CAPTCHA detected")
                
        except Exception as captcha_error:
            print(f"⚠️ Could not check for CAPTCHA: {captcha_error}")
            pass
        
        if error_found:
            print("❌ Login failed - please check credentials and try again")
            print("🔍 Debug: Current page source preview:")
            try:
                page_source = driver.page_source
                print(page_source[:1000] + "..." if len(page_source) > 1000 else page_source)
            except:
                print("Could not retrieve page source")
            raise Exception("Login failed - invalid credentials or additional verification required")
        
        # Navigate to profile page with better error handling
        print("🔍 Navigating to profile page...")
        
        # Try multiple approaches to access profile
        profile_urls = [
            "https://www.naukri.com/mnjuser/profile",
            "https://www.naukri.com/mnjuser/homepage",
            "https://www.naukri.com/mnjuser/dashboard"
        ]
        
        profile_accessed = False
        for profile_url in profile_urls:
            try:
                print(f"🔍 Trying to access: {profile_url}")
                driver.get(profile_url)
                time.sleep(5)
                
                # Check if we successfully accessed the profile
                final_url = driver.current_url
                page_title = driver.title
                print(f"📍 Final URL: {final_url}")
                print(f"📄 Final Page Title: {page_title}")
                
                # Check for success indicators
                success_indicators = [
                    "mynaukri" in final_url.lower(),
                    "profile" in final_url.lower(),
                    "dashboard" in final_url.lower(),
                    "homepage" in final_url.lower(),
                    "mynaukri" in page_title.lower(),
                    "profile" in page_title.lower()
                ]
                
                if any(success_indicators) and "login" not in final_url.lower():
                    print("🎯 Successfully accessed profile page")
                    print(f"Current URL: {final_url}")
                    profile_accessed = True
                    break
                else:
                    print(f"⚠️ Still on login page or redirected: {final_url}")
                    
            except Exception as nav_error:
                print(f"⚠️ Failed to access {profile_url}: {nav_error}")
                continue
        
        if not profile_accessed:
            print("❌ Could not access any profile page - authentication failed")
            raise Exception("Authentication failed - unable to access profile page")
        
    except Exception as e:
        print(f"❌ Email/Password login failed: {e}")
        print(f"Current URL: {driver.current_url}")
        print(f"Page title: {driver.title}")
        raise


def login_with_otp(driver: WebDriver, phone_number: str) -> None:
    """
    Logs in to Naukri using OTP (One Time Password) sent to phone.

    Args:
        driver: The webdriver instance.
        phone_number: The user's phone number.
    """
    wait = WebDriverWait(driver, 15)
    
    try:
        # Look for OTP login option
        otp_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'OTP') or contains(text(), 'Mobile') or contains(text(), 'Phone')]"))
        )
        otp_button.click()
        print("🔍 Clicked OTP login button")
        time.sleep(3)
        
        # Enter phone number
        phone_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='tel' or @name='mobile' or @id='mobile']"))
        )
        phone_input.clear()
        phone_input.send_keys(phone_number)
        print(f"📱 Entered phone number: {phone_number}")
        
        # Click send OTP button
        send_otp_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Send OTP') or contains(text(), 'Get OTP')]")
        send_otp_button.click()
        print("📤 OTP sent to phone")
        
        # Wait for user to enter OTP manually
        print("⏳ Please enter the OTP received on your phone...")
        input("Press Enter after entering the OTP in the browser...")
        
        # Click verify/login button
        verify_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Verify') or contains(text(), 'Login')]")
        verify_button.click()
        print("✅ OTP verified")
        time.sleep(5)
        
        # Navigate to profile page
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(5)
        print("🎯 Navigated to profile page")
        
    except Exception as e:
        print(f"❌ OTP login failed: {e}")
        raise


def login(driver: WebDriver, login_method: str, **kwargs) -> None:
    """
    Main login function that routes to the appropriate login method.

    Args:
        driver: The webdriver instance.
        login_method: The login method to use ('google', 'email_password', 'otp').
        **kwargs: Additional arguments for specific login methods.
    """
    print(f"🔐 Starting login with method: {login_method}")
    
    max_login_attempts = 2  # Try primary method, then fallback
    
    for attempt in range(max_login_attempts):
        try:
            if attempt == 0:
                # Primary login method
                if login_method.lower() == 'google':
                    email = kwargs.get('email')
                    if not email:
                        raise ValueError("Email is required for Google login")
                    login_with_google(driver, email)
                    
                elif login_method.lower() == 'email_password':
                    email = kwargs.get('email')
                    password = kwargs.get('password')
                    if not email or not password:
                        raise ValueError("Email and password are required for email/password login")
                    login_with_email_password(driver, email, password)
                    
                elif login_method.lower() == 'otp':
                    phone_number = kwargs.get('phone_number')
                    if not phone_number:
                        raise ValueError("Phone number is required for OTP login")
                    login_with_otp(driver, phone_number)
                    
                else:
                    raise ValueError(f"Unsupported login method: {login_method}. Supported methods: google, email_password, otp")
            else:
                # Fallback: Try Google OAuth if email/password fails due to CAPTCHA
                if login_method.lower() == 'email_password' and kwargs.get('email'):
                    print("🔄 Primary login failed, trying Google OAuth as fallback...")
                    login_with_google(driver, kwargs.get('email'))
                else:
                    raise Exception("No fallback method available")
            
            # If we reach here, login was successful
            print("✅ Login completed successfully")
            return
            
        except Exception as e:
            error_msg = str(e).lower()
            if "captcha" in error_msg or "verification" in error_msg:
                print(f"⚠️ Login attempt {attempt + 1} failed due to CAPTCHA: {e}")
                if attempt < max_login_attempts - 1:
                    print("🔄 Trying fallback method...")
                    time.sleep(3)  # Wait before retry
                    continue
                else:
                    print("❌ All login attempts failed due to CAPTCHA")
                    raise Exception("Login failed: CAPTCHA detected on all attempts. Please try manual login or use different credentials.")
            else:
                print(f"❌ Login attempt {attempt + 1} failed: {e}")
                if attempt < max_login_attempts - 1:
                    print("🔄 Retrying...")
                    time.sleep(5)  # Wait before retry
                    continue
                else:
                    raise e

def refresh_profile(driver: WebDriver, resume_file_path: str) -> None:
    """
    Refreshes the Naukri profile by re-uploading the resume.

    Args:
        driver: The webdriver instance.
        resume_file_path: The path to the resume file.
    """
    wait = WebDriverWait(driver, 20)
    try:
        resolved_path = os.path.abspath(os.path.expanduser(resume_file_path))
        if not os.path.exists(resolved_path):
            raise FileNotFoundError(f"Resume file does not exist: {resolved_path}")

        profile_url = "https://www.naukri.com/mnjuser/profile"
        if "mnjuser/profile" not in driver.current_url.lower():
            print("🔍 Navigating to Naukri profile page before resume upload...")
            driver.get(profile_url)
            time.sleep(3)

        wait.until(lambda d: "naukri.com" in d.current_url.lower())

        # Try the real upload form on the profile page and a few likely resume buttons.
        upload_input = None
        upload_selectors = [
            "//input[@type='file']",
            "//input[contains(@accept, 'pdf') or contains(@accept, 'doc') or contains(@accept, 'resume')]",
            "//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'upload resume')]",
            "//span[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'upload resume')]",
            "//a[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'upload resume')]",
            "//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'edit profile')]",
            "//span[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'edit profile')]",
        ]

        for selector in upload_selectors:
            try:
                element = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
                print(f"✅ Found resume/profile element with selector: {selector}")
                if element.tag_name.lower() == "input":
                    upload_input = element
                    break
                if element.is_displayed():
                    try:
                        element.click()
                        time.sleep(2)
                    except Exception:
                        pass
                    upload_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
                    break
            except Exception:
                continue

        if upload_input is None:
            raise Exception("No resume upload input found on the authenticated Naukri profile page")

        upload_input.send_keys(resolved_path)
        print(f"📎 Resume re-uploaded from: {resolved_path}")
        time.sleep(5)
        print(f"✅ Profile refreshed successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print("⚠️ Could not refresh profile:", e)
        print(f"📍 Current URL at failure: {driver.current_url}")
        try:
            print(f"📄 Page title at failure: {driver.title}")
        except Exception:
            pass

def cleanup(driver: WebDriver) -> None:
    """
    Closes the webdriver instance.

    Args:
        driver: The webdriver instance.
    """
    driver.quit()
    print("✅ Script finished")
