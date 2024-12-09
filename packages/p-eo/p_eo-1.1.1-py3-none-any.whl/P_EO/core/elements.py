from typing import List, Tuple, Union

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from P_EO.common.error import ElementNotFoundError
from P_EO.common.log import LogMixin
from P_EO.core.action import Action


class Element(Action, LogMixin):
    def __init__(
            self,
            locator: str,
            selector: By = None,
            describe: str = '',
            driver: Union[WebDriver, WebElement] = None,
    ):
        super().__init__()
        self._loc = locator
        self._method = selector
        self._driver = driver
        self._desc = describe if describe else 'element'

    def __get__(self, instance, owner):
        if self._driver is None:
            self._driver = instance.web_driver
        return self

    @property
    def __loc(self) -> Tuple[By, str]:
        """
        返回确定的locator
        :return:
        """
        if self._method is None:
            if self._loc.startswith('//') or self._loc.startswith('/html'):
                self._method = By.XPATH
            else:
                self._method = By.CSS_SELECTOR
        self.log.debug(f'元素信息: {self.describe} - {self.method} - {self.loc}')
        return self.method, self.loc

    @property
    def ele(self):
        """
        查找元素，并返回一个WebElement对象
        :return:
        """
        assert isinstance(self.driver, (WebDriver, WebElement, Element)), \
            TypeError(f'传入的 ele 参数类型错误！应为 WebElement 类型，实际为：{type(self.driver)} !')

        # 这里需要适配链式查找元素的逻辑
        if isinstance(self.driver, (WebElement, Element)):
            if not self.loc:
                return self.driver if isinstance(self.driver, WebElement) else self.driver.ele
        try:
            __ele = self.driver.find_element(*self.__loc)
            self.log.debug(f'元素查找成功! 父节点type {type(self.driver)}')
        except NoSuchElementException:
            self.log.error(f'元素查找失败! describe: {self.describe}, method: {self.method}, loc: {self.loc}')
            # self.log.error(traceback.format_exc())
            raise ElementNotFoundError(driver=self.driver, desc=self.describe, loc=self.loc, method=self.method)

        return __ele


class Elements(LogMixin):
    def __init__(
            self,
            locator: str,
            selector: By = None,
            describe: str = '',
            driver: Union[WebDriver, WebElement] = None,
    ):
        super().__init__()
        self._loc = locator
        self._method = selector
        self._driver = driver
        self._desc = describe if describe else 'element'
        self.__elements = []

    def __get__(self, instance, owner):
        if self._driver is None:
            self._driver = instance.web_driver
        return self

    def __repr__(self):
        return str(self.eles)

    def __len__(self):
        return len(self.eles)

    def __getitem__(self, index):
        return self.eles[index]

    @property
    def driver(self):
        """
        返回当前的 WebDriver 对象
        :return:
        """
        return self._driver

    @property
    def describe(self) -> str:
        """
        返回当前元素的描述
        :return:
        """
        return self._desc

    @property
    def loc(self) -> str:
        """
        返回当前元素的定位写法
        :return:
        """
        return self._loc

    @loc.setter
    def loc(self, value):
        """
        给当前元素的定位重新赋值
        :param value:
        :return:
        """
        self._loc = value

    def loc_replace(self, **kwargs):
        """
        替换 loc 中指定字符串
        :param kwargs:
        :return:
        """
        for key, value in kwargs.items():
            self.loc = self.loc.replace(key, value)
        return self

    @property
    def method(self) -> By:
        """
        返回当前元素的定位方法
        :return:
        """
        return self._method

    # noinspection DuplicatedCode
    @property
    def __loc(self):
        """
        返回确定的locator
        :return:
        """
        if self._method is None:
            if self._loc.startswith('//') or self._loc.startswith('/html'):
                self._method = By.XPATH
            else:
                self._method = By.CSS_SELECTOR
        self.log.debug(f'元素组信息: {self.describe} - {self.method} - {self.loc}')
        return self.method, self.loc

    @property
    def eles(self) -> List[Element]:
        """
        查找元素，并返回一个List对象，List元素中为Element对象
        :return:
        """
        if not self.__elements:
            try:
                _eles = self.driver.find_elements(*self.__loc)
                self.log.debug(f'元素组查找成功! 父节点type {type(self.driver)}')
            except NoSuchElementException:
                self.log.error(f'元素组查找失败! describe: {self.describe}, method: {self.method}, loc: {self.loc}')
                # self.log.error(traceback.format_exc())
                raise ElementNotFoundError(driver=self.driver, desc=self.describe, loc=self.loc, method=self.method)

            self.__elements = [
                Element(
                    locator='',
                    driver=ele,
                    describe=f'{self.describe}_{index + 1}'
                ) for index, ele in enumerate(_eles)
            ]

        return self.__elements


class IFrame:
    def __init__(self, ele: Union[str, Element, WebElement], driver: WebDriver = None):
        self._driver = driver
        self.__ele = ele

    def __get__(self, instance, owner):
        if self._driver is None:
            self._driver = instance.web_driver
        return self

    @property
    def ele(self):
        if isinstance(self.__ele, Element):
            return self.__ele.ele
        return self.__ele

    # def switch_frame_to_default(self):
    #     self._switch_frame('default')

    def switch_frame(self):
        """
        切换到当前元素的 iframe 里
        :return:
        """
        self._switch_frame(self.ele)

    def _switch_frame(self, frame):
        """
        切换 iframe
        :param frame:
        :return:
        """
        if frame == 'default':
            self._driver.switch_to.default_content()
        else:
            self._driver.switch_to.frame(frame)
