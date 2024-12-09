from typing import Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from P_EO import Element, Elements
from P_EO.core.driver import Driver
from P_EO.core.elements import IFrame


class Page:
    def __init__(self, driver: WebDriver):
        self.__driver = Driver(driver=driver)

    @property
    def driver(self) -> Driver:
        """
        返回 Driver 对象
        :return:
        """
        return self.__driver

    @property
    def web_driver(self):
        """
        返回 WebDriver 对象
        """
        return self.driver.web_driver

    def element(self, locator: str, describe: str = '', selector: By = None) -> Element:
        """
        定义一个 Element 对象
        :param locator:
        :param selector:
        :param describe:
        :return:
        """
        return Element(locator=locator, selector=selector, describe=describe, driver=self.web_driver)

    def elements(self, locator: str, describe: str = '', selector: By = None) -> Elements:
        """
        定义一个 Elements 对象
        :param locator:
        :param selector:
        :param describe:
        :return:
        """
        return Elements(locator=locator, selector=selector, describe=describe, driver=self.web_driver)

    def iframe(self, element: Union[str, Element, WebElement]) -> IFrame:
        """
        定义一个 IFrame 对象
        :param element:
        :return:
        """
        return IFrame(ele=element, driver=self.web_driver)
