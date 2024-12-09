from selenium.webdriver.remote.webdriver import WebDriver


class JavaScript:
    def __init__(self, driver: WebDriver = None):
        self._d = driver

    def __get__(self, instance, owner):
        if self._d is None:
            self._d = instance.web_driver
        return self

    def run_execute_script(self, script_code, *args):
        """
        运行JavaScript脚本
        :param script_code:
        :param args:
        :return:
        """
        return self._d.execute_script(script_code, *args)

    def open_new_tab(self, url=''):
        """
        打开一个新的tab页面
        :param url: 默认为空，如果url有值，则默认打开这个url
        :return:
        """
        _code = f'window.open({url})'
        self.run_execute_script(_code)

    def clear_input_control(self, ele):
        """
        js 清除输入框内容
        :return:
        """
        _code = "arguments[0].value = '';"
        self.run_execute_script(_code, ele)

    def goto_new_route(self, route):
        """
        切换到当前窗口到新路由上
        只针对同网站的不同路由进行切换
        :param route:
        :return:
        """
        _code = f"window.location.href='{route}'"
        self.run_execute_script(_code)

    @property
    def get_webdriver_arguments(self):
        """
        获取浏览器版本
        :return:
        """
        return self.run_execute_script("return window.navigator.webdriver")

    @property
    def get_local_storage(self):
        """
        获取本地存储信息
        :return:
        """
        return self.run_execute_script("return window.localStorage")

    @property
    def get_session_storage(self):
        """
        获取会话存储信息
        :return:
        """
        return self.run_execute_script("return window.sessionStorage")

    @property
    def get_all_iframes(self):
        js_script = """
        function getAllIframesWithHierarchy(context = document, path = '') {
            const iframes = context.querySelectorAll('iframe');
            let result = [];

            iframes.forEach((iframe, index) => {
                const currentPath = `${path}/iframe[${index}]`;
                result.push({ path: currentPath, src: iframe.src });

                try {
                    // Try to access the iframe's document
                    const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
                    result = result.concat(getAllIframesWithHierarchy(iframeDoc, currentPath));
                } catch (e) {
                    console.warn(`Cannot access iframe at ${currentPath}:`, e);
                }
            });

            return result;
        }

        return getAllIframesWithHierarchy();
        """
        return self.run_execute_script(js_script)

    def scroll_into_view(self, ele):
        """
        滚动元素到页面可见
        :param ele:
        :return:
        """
        self.run_execute_script('arguments[0].scrollIntoView(true)', ele)

    def get_location_by_view(self, ele):
        return self.run_execute_script('return arguments[0].getBoundingClientRect()', ele)['value']
