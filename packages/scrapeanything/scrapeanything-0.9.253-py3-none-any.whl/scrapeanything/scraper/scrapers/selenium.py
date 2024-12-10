from enum import Enum
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import time
from scrapeanything.scraper.models.element import Element
from scrapeanything.scraper.scraper import Scraper
from scrapeanything.utils.config import Config
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException        
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
import base64

class XPathReasons(Enum):
    SELECT = 0
    CLICK = 1

class Selenium(Scraper):

    def __init__(self, config: Config, headless: bool=True, is_error: bool=True, timeout: int=None, fullscreen: bool=False, window: dict={}, user_dir: str=None, disable_javascript: bool=False, proxy_address: str=None):
        url = config.get(section='SELENIUM', key='url')

        options = Options()
        options.add_argument('--disable-logging')
        options.add_argument('--log-level=3')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-extensions')
        options.add_argument('--enable-unsafe-swiftshader')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('prefs', { 'profile.default_content_settings.popups': 0, 'download.default_directory': os.path.join(os.getcwd(), 'data'), 'directory_upgrade': True })

        window_size = window['size'] if 'size' in window else []
        if len(window_size) == 0:
            options.add_argument('--start-maximized')
        else:
            self.driver.set_window_position(x=0, y=0)
            self.driver.set_window_size(width=window_size[0], height=window_size[1])

        if fullscreen is True: options.add_argument('--kiosk')
        if headless is True: options.add_argument('--headless')
        if proxy_address is not None: options.add_argument(f'--proxy-server={proxy_address}')

        if url is not None:
            self.driver = webdriver.Remote(command_executor=url, options=options)

        elif url is None:
            service = Service(ChromeDriverManager().install()) # Use webdriver_manager to automatically download and manage the correct version of chromedriver
            self.driver = webdriver.Chrome(service=service, options=options) # Initialize the WebDriver

        if timeout is not None: self.driver.implicitly_wait(timeout)

        # This is a workaround for Selenium's webdriver detection. Websites that use this detection
        # can prevent Selenium from working. This code sets the "webdriver" property of the navigator
        # object to undefined, effectively disabling this detection. This is a common technique used
        # in Selenium scripts to avoid detection. The property is set to undefined instead of being
        # deleted, so that the detection code doesn't throw an error when it tries to access it.
        self.driver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')
        
        # prepare options for all methods
        self.is_error = is_error
        self.timeout = timeout

        super().__init__()

    def on_wget(self, url: str) -> None:
        self.driver.get(url)

    def on_xPath(self, path: str, element: any=Element, timeout: int=99, is_error: bool=True) -> str | list[str] | int | list[int] | float | list[float] | Element | list[Element]:
        return self._xPath(path=path, mode=XPathReasons.SELECT, element=element, timeout=timeout, is_error=is_error)
    
    # TODO
    def on_exists(self, path: str, element: Element, timeout: int=0, is_error: bool=False) -> bool:
        element = self.driver if element.element is None else element.element

        if timeout > 0:
            try:
                ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
                element = WebDriverWait(driver=element, timeout=timeout, ignored_exceptions=ignored_exceptions).until(
                    EC.presence_of_element_located((By.XPATH, path)))
                
                if isinstance(element, list):
                    return len(element) > 0
                else:
                    return element is not None

            except Exception as ex:
                if is_error is True:
                    raise NoSuchElementException(msg=f'Element with xpath {path} was not found')
                else:
                    return False
        else:
            try:
                if is_error is False:
                    return len(element.find_elements(by=By.XPATH, value=path)) > 0
                elif is_error is True and len(element.find_elements(by=By.XPATH, value=path)) == 0:
                    raise NoSuchElementException(msg=f'Element with xpath {path} was not found')

            except NoSuchElementException as ex:
                if is_error is True:
                    raise ex
                else:
                    return False

            except StaleElementReferenceException:
                raise StaleElementReferenceException()

    def on_get_text(self, element: any) -> str:
        return element.text

    def on_get_html(self, element: any) -> str:
        return element.get_attribute('innerHTML')

    def on_get_attribute(self, element: any, prop: str) -> str:
        return element.get_attribute(prop)

    def on_hover(self, path: str, element: any, is_error: bool=True, timeout: int=99) -> None:
        element = self._xPath(element=element, path=path, is_error=is_error, timeout=timeout, mode=XPathReasons.SELECT)
        ActionChains(self.driver).move_to_element(element).perform()

    def on_click_and_hold(self, path: str, seconds: float, element: any=None, timeout: int=99, is_error: bool=True) -> None:
        element = self._xPath(path=path, timeout=timeout, is_error=is_error, mode=XPathReasons.CLICK)
        action = ActionChains(self.driver)
        action.click_and_hold(element).perform()
        time.sleep(seconds) # sleep for N seconds
        action.release().perform()

    # TODO: gestire is_error
    def on_click(self, path: str, element: any=None, timeout: int=None, pos: int=0, is_error: bool=True) -> None:
        if element is None and path is not None:
            elements = self._xPath(path=path, element=element, timeout=timeout, is_error=is_error, mode=XPathReasons.CLICK)
        
        if len(elements) == 0:
            return
        
        if type(elements) is list and len(elements) > 0:
            element = elements[pos]

        self._click(element=element, is_error=is_error)

    def on_click_all(self, path: str, element: any=None, timeout=0, is_error: bool=True) -> None:
        elements = self._xPath(path=path, element=element, timeout=timeout, is_error=is_error, mode=XPathReasons.CLICK)
        for element in elements:
            self._click(element=element, is_error=is_error)

    def on_back(self) -> None:
        self.driver.back()

    def on_get_current_url(self) -> str:
        return self.driver.current_url

    # TODO: gestire is_error
    def on_enter_text(self, path: str, text: str, clear: bool=False, element: any=None, timeout: int=99, is_error: bool=True) -> None:
        element = self._xPath(path=path, element=element, timeout=timeout, is_error=is_error, mode=XPathReasons.SELECT)

        if element is None:
            return

        if type(element) is list:
            element = element[0]

        if clear is True:
            element.send_keys(Keys.CONTROL + 'a')
            element.send_keys(Keys.BACKSPACE)

        element.send_keys(text)

    def on_solve_captcha(self, path: str) -> str:
        pass

    def on_login(self, username_text=None, username=None, password_text=None, password=None, is_error: bool=True) -> None:
        self.on_enter_text(username_text, username, is_error=is_error)
        self.on_enter_text(password_text, password, is_error=is_error)

        self.on_click('//button[@class="sign-in-form__submit-button"]')

    def on_search(self, path=None, text=None, timeout: int=99, is_error: bool=True) -> None:
        self.on_enter_text(path=path, text=text, timeout=timeout, is_error=is_error)
        self.on_enter_text(path=path, text=Keys.RETURN, timeout=timeout, is_error=is_error)

    def on_scroll_to_bottom(self) -> None:
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

    def on_get_scroll_top(self) -> None:
        return self.driver.execute_script('return document.documentElement.scrollTop;')

    def on_get_scroll_bottom(self) -> None:
        return self.driver.execute_script('return document.body.scrollHeight')

    def on_select(self, path: str, option: str, element: any=None) -> None:
        element = self._xPath(path=path, element=element, mode=XPathReasons.SELECT)

        if element is not None:
            Select(element).select_by_visible_text(option)

    def on_get_image_from_canvas(self, path: str, local_path: str, element: any) -> str:
        image_filename = f'{local_path}/image.png'

        # get the base64 representation of the canvas image (the part substring(21) is for removing the padding 'data:image/png;base64')
        base64_image = self.driver.execute_script(f"return document.querySelector('{path}').toDataURL('image/png').substring(21);")

        # decode the base64 image
        output_image = base64.b64decode(base64_image)

        # save to the output image
        with open(image_filename, 'wb') as f:
            f.write(output_image)

        return image_filename

    def on_switch_to(self, element: any) -> None:
        if element == 'default':
            self.driver.switch_to.default_content()
        else:
            self.driver.switch_to.frame(element)

    def on_screenshot(self, path: str=None, file: str=None) -> str:
        if path is not None:
            element = self._xPath(path=path, mode=XPathReasons.SELECT)
        
        if file is not None:
            if element is not None:
                self.driver.get_screenshot_as_file(file)
            else:
                return element.get_screenshot_as_file(file)
        else:
            if element is not None:
                return element.screenshot_as_base64
            else:
                return self.driver.screenshot_as_base64

    def on_freeze(self) -> None:
        self.driver.execute_cdp_cmd('Emulation.setScriptExecutionDisabled', { 'value': True })

    def on_unfreeze(self) -> None:
        self.driver.execute_cdp_cmd('Emulation.setScriptExecutionDisabled', { 'value': False })

    def on_get_cookies(self) -> list[dict]:
        return self.driver.get_cookies()
    
    def on_drag_and_drop(self, path_from: str, path_to: str) -> None:
        element = self._xPath(path=path_from, mode=XPathReasons.CLICK)
        target = self._xPath(path=path_to, mode=XPathReasons.CLICK)
        ActionChains(self.driver).drag_and_drop(element, target).perform()

    def on_close(self) -> None:
        self.driver.quit()

    #region private methods
    def _xPath(self, path: str, mode: str, element: Element=None, timeout: int=None, is_error: bool=True) -> str | list[str] | int | list[int] | float | list[float] | Element | list[Element]:
        if element is None: element = Element()
        if timeout is None and self.timeout is None:
            timeout = 99
        elif timeout is not None:
            timeout = timeout
        else:
            timeout = self.timeout
        
        if timeout == 0:
            return (self.driver if element.element is None else element.element).find_elements(by=By.XPATH, value=path)

        try:
            ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)              
            elements = WebDriverWait(driver=(self.driver if element.element is None else element.element), timeout=timeout, ignored_exceptions=ignored_exceptions).until(
                EC.visibility_of_all_elements_located((By.XPATH, path)) if mode == XPathReasons.SELECT else lambda x: [e for e in EC.visibility_of_all_elements_located((By.XPATH, path))(x) if e.is_enabled()]
            )

            return elements

        except Exception as ex:
            if is_error is True:
                raise NoSuchElementException(msg=f'Element with xpath {path} was not found')
            else:
                return []

    def _click(self, element: Element, is_error: bool=True) -> None:

            try:
                element.element.click()
                return

            except Exception as e:
                try:
                    self.driver.execute_script('arguments[0].click();', element)
                    return

                except Exception as e:

                    try:
                        actions = ActionChains(self.driver)
                        actions.click(element.element).perform()
                        return
                    except Exception as ex:
                        if is_error is True:
                            raise NoSuchElementException(msg=f'Element with was not found')

    #endregion private methods