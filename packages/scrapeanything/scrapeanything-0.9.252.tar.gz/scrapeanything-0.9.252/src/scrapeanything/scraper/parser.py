import time
from scrapeanything.scraper.models.element import Element
from scrapeanything.scraper.types import Types
from scrapeanything.utils.config import Config
from scrapeanything.utils.utils import Utils
from scrapeanything.scraper.scraper import Scraper

class Parser:

    scraper: Scraper = None

    def __init__(self, config: Config, user_dir: str=None, headless: bool=True, timeout: int=None, is_error: bool=True, fullscreen: bool=False, disable_javascript: bool=False, window: dict={}, proxy_address: str=None) -> None:
        self.config = config
        self.scraper = self.get_scraper(config=config, headless=headless, timeout=timeout, is_error=is_error, fullscreen=fullscreen, disable_javascript=disable_javascript, window=window, user_dir=user_dir, proxy_address=proxy_address)

    # region methods
    def click(self, path: str, element: Element=None, timeout: int=None, pos: int=0, is_error: bool=True, sleep_before: int=0, sleep_after: int=0) -> None:
        time.sleep(sleep_before)
        self.scraper.click(path=path, element=element, timeout=timeout, pos=pos, is_error=is_error)
        time.sleep(sleep_after)
        
    def click_all(self, path: str, element: Element=None, timeout: int=None, is_error: bool=True, sleep_before: int=0, sleep_after: int=0) -> None:
        time.sleep(sleep_before)
        self.scraper.click_all(path=path, element=element, timeout=timeout, is_error=is_error)
        time.sleep(sleep_after)

    def hover(self, path: str, element: Element=None, is_error: bool=True, timeout: int=None, sleep_before: int=0, sleep_after: int=0) -> None:
        time.sleep(sleep_before)
        self.scraper.hover(path=path, element=element, is_error=is_error, timeout=timeout)
        time.sleep(sleep_after)

    def click_and_hold(self, path: str, seconds: float, element: Element=None, timeout: int=None, is_error: bool=True, sleep_before: int=0, sleep_after: int=0) -> None:
        time.sleep(sleep_before)
        self.scraper.click_and_hold(path=path, element=element, timeout=timeout, seconds=seconds, is_error=is_error)
        time.sleep(sleep_after)

    def back(self, sleep_before: int=0, sleep_after: int=0) -> None:
        time.sleep(sleep_before)
        self.scraper.back()
        time.sleep(sleep_after)

    def get_current_url(self) -> str:
        return self.scraper.get_current_url()

    def enter_text(self, path: str, text: str, clear: bool=False, element: Element=None, timeout: int=None, is_error: bool=True, sleep_before: int=0, sleep_after: int=0):
        time.sleep(sleep_before)
        return self.scraper.enter_text(path=path, text=text, clear=clear, element=element, timeout=timeout, is_error=is_error)

    def wget(self, url: str, tries: int=0) -> None:
        return self.scraper.wget(url=url, tries=tries)

    def xPath(self, path: str, element: Element=None, pos: int=None, data_type: str=Types.STRING, prop: str=None, explode=None, condition=None, substring=None, transform=None, replace=None, join=None, timeout=None, is_error: bool=True, sleep_before: int=0, sleep_after: int=0) -> any:
        time.sleep(sleep_before)
        v = self.scraper.xPath(path=path, element=element, pos=pos, data_type=data_type, prop=prop, explode=explode, condition=condition, substring=substring, transform=transform, replace=replace, join=join, timeout=timeout, is_error=is_error)
        time.sleep(sleep_after)
        return v

    def exists(self, path: str, element: Element=None, timeout: int=None, is_error: bool=False, sleep_before: int=0, sleep_after: int=0) -> bool:
        time.sleep(sleep_before)
        v = self.scraper.exists(path=path, element=element, timeout=timeout, is_error=is_error)
        time.sleep(sleep_after)
        return v

    def get_css(self, element: any, prop: str, sleep_before: int=0, sleep_after: int=0) -> str:
        time.sleep(sleep_before)
        return self.scraper.get_css(element=self, prop=prop)
        time.sleep(sleep_after)

    def login(self, username_text: str=None, username: str=None, password_text: str=None, password: str=None, is_error: bool=True, sleep_before: int=0, sleep_after: int=0) -> None:
        time.sleep(sleep_before)
        self.scraper.login(username_text, username, password_text, password, is_error=is_error)
        time.sleep(sleep_after)

    def search(self, path: str=None, text: str=None, timeout: int=None, is_error: bool=True, sleep_before: int=0, sleep_after: int=0) -> None:
        time.sleep(sleep_before)
        self.scraper.search(path=path, text=text, timeout=timeout, is_error=is_error)
        time.sleep(sleep_after)

    def scroll_to_bottom(self, sleep_before: int=0, sleep_after: int=0) -> None:
        time.sleep(sleep_before)
        self.scraper.scroll_to_bottom()
        time.sleep(sleep_after)

    def get_scroll_top(self, sleep_before: int=0, sleep_after: int=0) -> None:
        time.sleep(sleep_before)
        return self.scraper.get_scroll_top()
        time.sleep(sleep_after)

    def get_scroll_bottom(self, sleep_before: int=0, sleep_after: int=0) -> None:
        time.sleep(sleep_before)
        return self.scraper.get_scroll_bottom()

    def select(self, path: str, option: str, sleep_before: int=0, sleep_after: int=0) -> None:
        time.sleep(sleep_before)
        self.scraper.select(path=path, option=option)
        time.sleep(sleep_after)

    def get_image_from_canvas(self, path: str, local_path: str, element: Element=None) -> str:
        return self.scraper.get_image_from_canvas(path=path, local_path=local_path, element=element)

    def switch_to(self, element: any) -> None:
        self.scraper.switch_to(element=element)

    def screenshot(self, path: str=None, file: str=None, sleep_before: int=0, sleep_after: int=0) -> None:
        time.sleep(sleep_before)
        data = self.scraper.screenshot(path=path, file=file)
        return data

    def freeze(self) -> None:
        self.scraper.freeze()

    def unfreeze(self) -> None:
        self.scraper.unfreeze()

    def get_cookies(self) -> 'list[dict]':
        return self.scraper.get_cookies()

    def close(self) -> None:
        self.scraper.close()

    #endregion methods

    def get_scraper(self, config: Config, user_dir: str=None, headless: bool=True, is_error: bool=True, timeout: int=None, fullscreen: bool=False, disable_javascript: bool=False, window: dict={}, proxy_address: str=None) -> Scraper:
        scraper_type = self.config.get('PROJECT', 'scraper')
        if scraper_type is not None:
            module_name = self.config.get('PROJECT', 'scraper')
            class_name = ''.join([ slug.capitalize() for slug in scraper_type.split('_') ])
        else:
            module_name = 'selenium'
            class_name = 'Selenium'

        return Utils.instantiate(module_name=f'scrapeanything.scraper.scrapers.{module_name}', class_name=class_name, args={ 'headless': headless, 'is_error': is_error, 'timeout': timeout, 'fullscreen': fullscreen, 'disable_javascript': disable_javascript, 'window': window, 'config': config, 'user_dir': user_dir, 'proxy_address': proxy_address })