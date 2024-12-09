import abc
import time
from typing import Union

from selenium.common.exceptions import WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select

from P_EO.common.config import Default
from P_EO.common.error import ElementNotEnableError, ElementInputError, \
    ElementFindTimeoutError, ElementNotFoundError
from P_EO.common.log import LogMixin
from P_EO.common.time_ import get_time
from P_EO.core.javascript import JavaScript


class Action(LogMixin, metaclass=abc.ABCMeta):
    def __init__(self):
        self._driver: Union[WebDriver, WebElement] = None
        self._desc = ''
        self._loc = ''
        self._method: By = None
        self.__pos = None

    def __get__(self, instance, owner):
        if self._driver is None:
            self._driver = instance.web_driver
        return self

    @property
    @abc.abstractmethod
    def ele(self) -> WebElement:
        """
        返回一个 WebElement 对象
        :return:
        """
        raise NotImplementedError('该方法需要重写')

    def find_ele(self, locator: str, selector: By = None, describe: str = ''):
        """
        在当前Element中，查找一个指定元素
        :param locator:
        :param selector:
        :param describe:
        :return:
        """
        from P_EO import Element
        return Element(locator=locator, selector=selector, describe=describe, driver=self.ele)

    def find_eles(self, locator: str, selector: By = None, describe: str = ''):
        """
        在当前Element中，查找一个指定元素组
        :param locator:
        :param selector:
        :param describe:
        :return:
        """
        from P_EO import Elements
        return Elements(locator=locator, selector=selector, describe=describe, driver=self.ele)

    @property
    def driver(self):
        """
        返回当前的 WebDriver 对象
        :return:
        """
        if not isinstance(self._driver, (WebDriver, WebElement)):
            raise ValueError(f'当前的 driver 对象属性不正确 {type(self._driver)}')
        return self._driver

    @property
    def __js(self):
        return JavaScript(self.driver)

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

    def click(self, wait=Default.ACTION_WAIT, check_enabled=True):
        """
        元素点击
        :param wait:
        :param check_enabled: 校验元素是否可交互
        :return:
        """
        if check_enabled and not self.enabled:
            self.log.error(
                f'当前元素存在但不可交互 describe: {self.describe}, method: {self.method}, loc: {self.loc}')
            raise ElementNotEnableError(driver=self.driver, desc=self.describe, loc=self.loc, method=self.method)

        try:
            self.ele.click()
        except WebDriverException as e:
            self.log.error(f'Selenium Exception: {e}')
            raise

        self.log.info(f'元素 {self.describe} 点击成功')
        time.sleep(wait)

        return self

    def action_chains(self, wait=Default.ACTION_WAIT):
        """
        元素滚动到可见，并返回一个ActionChains对象
        :param wait:
        :return:
        """
        self.scrolled_into_view()
        # ActionChains(self.web_driver).scroll_to_element(self.ele).perform()  # selenium==3.141.0 好像没有这个语法，>=4以上好像才有
        time.sleep(wait)
        return ActionChains(self.driver)

    def click_by_action_chains(self, wait=Default.ACTION_WAIT):
        """
        元素滚动并点击
        :param wait:
        :return:
        """
        self.action_chains(wait).click(self.ele).perform()
        self.log.info(f'元素 {self.describe} 点击(ActionChains)成功')
        time.sleep(wait)

        return self

    def double_click(self, wait=Default.ACTION_WAIT):
        """
        元素滚动并双击
        :param wait:
        :return:
        """
        self.action_chains(wait).double_click(self.ele).perform()
        self.log.info(f'元素 {self.describe} 双击(ActionChains)成功')
        time.sleep(wait)

        return self

    def right_click(self, wait=Default.ACTION_WAIT):
        """
        元素滚动并右键
        :param wait:
        :return:
        """
        self.action_chains(wait).context_click(self.ele).perform()
        self.log.info(f'元素 {self.describe} 右键(ActionChains)成功')
        time.sleep(wait)

        return self

    def click_by_pos(self, wait=Default.ACTION_WAIT):
        """
        根据元素坐标点击
        :param wait:
        :return:
        """
        if self.__pos is None:
            raise ValueError('请先调用 hover 方法获取坐标')
        pos = self.__pos
        self.action_chains(wait=wait).move_to_element_with_offset(
            self.ele,
            pos['x'],
            pos['y']
        ).click().perform()
        self.log.info(f'元素 {self.describe} 坐标({pos["x"], pos["y"]})点击(ActionChains)成功')
        time.sleep(wait)

        return self

    def drag_to_pos(self, x, y, wait=Default.ACTION_WAIT):
        """
        拖拽到指定坐标
        :param x:
        :param y:
        :param wait:
        :return:
        """
        self.action_chains(wait).drag_and_drop_by_offset(self.ele, xoffset=x, yoffset=y).perform()
        self.log.info(f'元素 {self.describe} 拖拽(ActionChains)至 {x}, {y} 成功')
        time.sleep(wait)

        return self

    def drag_to_ele(self, ele, wait=Default.ACTION_WAIT):
        """
        拖拽到指定元素上
        :param ele:
        :param wait:
        :return:
        """
        from P_EO import Element
        if isinstance(ele, Element):
            ele = ele.ele

        if not isinstance(ele, WebElement):
            raise TypeError('ele 参数类型错误，必须是 WebElement 类型')

        self.action_chains(wait).drag_and_drop(source=self.ele, target=ele).perform()
        self.log.info(f'元素 {self.describe} 拖拽(ActionChains)至元素 {ele} 成功')
        time.sleep(wait)

        return self

    def hover(self, wait=Default.ACTION_WAIT):
        """
        悬停
        :param wait:
        :return:
        """
        self.__pos = self.ele.location

        self.action_chains(wait).move_to_element(self.ele).perform()
        self.log.info(f'元素 {self.describe} 悬停(ActionChains)成功')
        time.sleep(wait)

        return self

    @property
    def get_input_values(self):
        """
        获取输入框内容
        :return:
        """
        return self.ele.get_attribute('value')

    def clear(self, force_clear=False):
        """
        清理输入内容
        :param force_clear:
        :return:
        """
        _ele = self.ele
        _ele.clear()
        if force_clear:
            self.__js.clear_input_control(_ele)
        # assert self.get_input_values == '', f'元素 {self.describe} 清理输入失败'
        self.log.info(f'元素 {self.describe} 清理输入成功')

        return self

    def send_keys(self, *values):
        """
        输入内容
        :param values:
        :return:
        """
        self.ele.send_keys(*values)
        _values = ','.join(values)
        self.log.info(f'元素 {self.describe} 输入内容 {_values}')

    def send_keys_by_str(self, value, wait=Default.ACTION_WAIT, clear=False, force_clear=False):
        """
        输入字符串内容
        :param value:
        :param wait:
        :param clear:
        :param force_clear:
        :return:
        """
        if not isinstance(value, str):
            value = str(value)

        self.scrolled_into_view()
        if clear:
            self.clear(force_clear)

        self.send_keys(value)
        tag = self.get_input_values
        if tag != value:
            self.log.error(
                f'当前输入内容不正确 describe: {self.describe}, '
                f'method: {self.method}, '
                f'loc: {self.loc}, '
                f'expect: {value}, '
                f'target: {tag}'
            )
            raise ElementInputError(
                driver=self.driver,
                desc=self.describe,
                loc=self.loc,
                method=self.method,
                send_value=value,
                tag_value=tag
            )
        self.log.info(f'元素 {self.describe} 输入内容成功 {value}')
        time.sleep(wait)

    @property
    def text(self):
        """
        返回与元素文本
        :return:
        """
        return self.ele.text.strip()

    def get_attribute(self, attribute):
        """
        返回元素属性
        :param attribute:
        :return:
        """
        return self.ele.get_attribute(attribute).strip()

    def wait(self, timeout=Default.TIMEOUT, interval=Default.INTERVAL):
        """
        等待元素出现并操作
        :param timeout:
        :param interval:
        :return:
        """
        if self.wait_exists(timeout=timeout, interval=interval):
            self.log.info(f'元素 {self.describe} 等待完成')
            return self
        self.log.error(f'当前元素查找超时 describe: {self.describe}, method: {self.method}, loc: {self.loc}')
        raise ElementFindTimeoutError(driver=self.driver, desc=self.describe, loc=self.loc, method=self.method)

    def wait_exists(self, timeout=Default.TIMEOUT, interval=Default.INTERVAL):
        """
        轮询判断元素是否存在
        :param timeout:
        :param interval:
        :return:
        """
        start = time.time()
        while time.time() - start <= timeout:
            try:
                if self.displayed is True:
                    self.log.info(f'元素 {self.describe} 确认存在')
                    return True
            except ElementNotFoundError:
                pass
            time.sleep(interval)
        self.log.warning(f'元素 {self.describe} 确认不存在')
        return False

    def wait_disappear(self, timeout=Default.TIMEOUT, interval=Default.INTERVAL):
        """
        轮询判断元素是否消失
        :param timeout:
        :param interval:
        :return:
        """
        start = time.time()
        while time.time() - start <= timeout:
            try:
                if self.displayed is False:
                    break
            except ElementNotFoundError:
                break
            time.sleep(interval)
        else:
            self.log.warning(f'元素 {self.describe} 确认未消失')
            return False
        self.log.info(f'元素 {self.describe} 确认消失')
        return True

    @property
    def displayed(self):
        """
        判断元素是否可见
        :return:
        """
        return self.ele.is_displayed()

    @property
    def selected(self):
        """
        判断元素是否已选中
        :return:
        """
        return self.ele.is_selected()

    @property
    def enabled(self):
        """
        判断元素是否可交互
        :return:
        """
        return self.ele.is_enabled()

    def scrolled_into_view(self):
        """
        滚动元素到当前视图
        :return:
        """
        self.__js.scroll_into_view(self.ele)
        return self

    def save_screenshot(self, file_path=None):
        """
        保存当前元素为图片
        :param file_path:
        :return:
        """
        if not file_path:
            file_path = Default.WEB_PAGE_PATH
            file_path.mkdir(parents=True, exist_ok=True)
            file_path.joinpath(f'element_{get_time()}_{self.describe}.png')

        self.ele.screenshot(file_path)
        self.log.info(f'元素 {self.describe} 保存成功 {file_path}')
        return file_path

    @property
    def tag_name(self):
        """
        返回当前元素的tag标签
        :return:
        """
        return self.ele.tag_name

    @property
    def id(self):
        return self.ele.id

    @property
    def size(self):
        """
        返回元素大小
        :return:
        """
        return self.ele.size

    @property
    def location(self):
        """
        返回元素位置
        :return:
        """
        if not self.__pos:
            self.__pos = self.ele.location
        return self.__pos

    @property
    def get_location_by_view(self):
        """
        返回元素在当前视图中的位置
        :return:
        """
        return self.__js.get_location_by_view(self.ele)

    @property
    def select(self):
        return Select(self.ele)
