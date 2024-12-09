import os

from P_EO import Default
from P_EO.common.time_ import get_time
from P_EO.public_variables.public_variables import Public


class PEOBaseError(Exception):
    """
    异常基类
    """

    def __init__(self, err_msg, desc='', loc='', method='', driver=None, **kwargs):
        self.msg = err_msg
        self.desc = desc
        self.loc = loc
        self.method = method
        self.kwargs = kwargs
        self.driver = driver
        self.path = ''
        self.url = ''
        self.screenshots()

    def __str__(self):
        _msg = self.msg
        _msg += f', describe: {self.desc}' if self.desc else ''
        _msg += f', method: {self.method}' if self.method else ''
        _msg += f', loc: {self.loc}' if self.loc else ''
        _msg += f', url: {self.url}' if self.url else ''
        _msg += f', screenshots: {self.path}' if self.path else ''
        _msg += f', {self.kwargs}' if self.kwargs else ''
        return _msg

    def screenshots(self):
        parent_path = Default.ERROR_PATH
        if parent_path and self.driver:
            from P_EO.core.driver import Driver

            if not isinstance(self.driver, Driver):
                self.driver = Driver(self.driver)
            self.url = self.driver.get_cur_url

            parent_path.mkdir(parents=True, exist_ok=True)
            self.path = os.path.join(parent_path, f'{get_time()}_{self.desc}.png')
            self.driver.screenshots(self.path)
            Public.last_error_image = self.path


class ElementNotFoundError(PEOBaseError):
    def __init__(self, desc, loc, method, driver=None):
        self.msg = '元素未找到'
        super().__init__(err_msg=self.msg, desc=desc, loc=loc, method=method, driver=driver)


class ElementFindTimeoutError(PEOBaseError):
    def __init__(self, desc, loc, method, driver=None):
        self.msg = '元素查找超时'
        super().__init__(err_msg=self.msg, desc=desc, loc=loc, method=method, driver=driver)


class ElementNotDisplayedError(PEOBaseError):
    def __init__(self, desc, loc, method, driver=None):
        self.msg = '元素存在但是不可见'
        super().__init__(err_msg=self.msg, desc=desc, loc=loc, method=method, driver=driver)


class ElementNotEnableError(PEOBaseError):
    def __init__(self, desc, loc, method, driver=None):
        self.msg = '元素存在但是不可交互'
        super().__init__(err_msg=self.msg, desc=desc, loc=loc, method=method, driver=driver)


class ElementInputError(PEOBaseError):
    def __init__(self, desc, loc, method, send_value, tag_value, driver=None):
        self.msg = '元素输入内容错误'
        super().__init__(err_msg=self.msg, desc=desc, loc=loc, method=method, send_value=send_value,
                         tag_value=tag_value, driver=driver)
