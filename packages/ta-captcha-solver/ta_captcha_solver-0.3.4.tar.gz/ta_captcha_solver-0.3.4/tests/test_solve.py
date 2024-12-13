#!/usr/bin/env python

import os
from time import sleep

import pytest
from RPA.Browser.Selenium import Selenium
from ta_captcha_solver.exceptions import APICaptchaUnsolvable, UICaptchaNotSolved
from ta_captcha_solver.ta_captcha_solver import TACaptchaSolver


class TestSolve:
    """
    For succesfull execution you need to have such env vars with valid values available in your system:
      - CAPTCHA_GURU_API_KEY
      - TWO_CAPTCHA_API_KEY

    If no SELENIUM_GRID_URL provided, test will be executed on local instance of chrome driver
    """

    @classmethod
    def setup_class(self):
        self.captcha_guru_api_key = os.getenv("CAPTCHA_GURU_API_KEY")
        self.two_captcha_api_key = os.getenv("TWO_CAPTCHA_API_KEY")
        self.remote_url = os.getenv("SELENIUM_GRID_URL")
        self.v2_url = "https://google.com/recaptcha/api2/demo"
        self.fun_captcha_url = "https://www.linkedin.com/checkpoint/rp/request-password-reset"
        self.fun_captcha_url2 = "https://client-demo.arkoselabs.com/solo-animals"
        self.image_url = "https://captcha.com/demos/features/captcha-demo.aspx"
        self.hcaptcha_url = "https://accounts.hcaptcha.com/demo"
        self.image_source = os.path.join(os.getcwd(), "tests/captcha_screenshot.png")
        self.incorrect_image_source = os.path.join(os.getcwd(), "tests/incorrect_captcha_screenshot.png")

        # We need this var for bitbucket pipelines sucessfull run
        self.executable_path = os.path.join(os.getcwd(), "chromedriver")
        if not os.path.exists(self.executable_path):
            self.executable_path = None

    def setup_method(self):
        self.browser = Selenium()

    def teardown_method(self):
        self.browser.close_browser()

    def test_image_req_params_browser(self):
        self.browser.open_browser(
            browser="chrome",
            url=self.image_url,
            remote_url=self.remote_url,
            executable_path=self.executable_path,
        )
        captcha = TACaptchaSolver.get(
            captcha_type="image",
            browser=self.browser,
            captcha_guru_api_key=self.captcha_guru_api_key,
            image_xpath="//img[@id='demoCaptcha_CaptchaImage']",
        )
        captcha.solve()
        self.browser.input_text_when_element_is_visible("//input[@id='captchaCode']", captcha.token)
        self.browser.click_element_when_visible("//input[@id='validateCaptchaButton']")
        self.browser.wait_until_page_contains_element("//span[@id='validationResult']/span", timeout=5)
        assert self.browser.does_page_contain_element("//span[@id='validationResult']/span[@class='correct']")

    def test_image_req_params_image_source(self):
        captcha = TACaptchaSolver.get(
            captcha_type="image",
            captcha_guru_api_key=self.captcha_guru_api_key,
            image_source=self.image_source,
        )
        assert captcha.solve()

    def test_recaptchav2_req_params(self):
        self.browser.open_browser(
            browser="chrome",
            url=self.v2_url,
            remote_url=self.remote_url,
            executable_path=self.executable_path,
        )
        captcha = TACaptchaSolver.get(
            captcha_type="v2",
            browser=self.browser,
            service_provider_name="captcha.guru",
            service_provider_key=self.captcha_guru_api_key,
        )
        captcha.solve()
        self.browser.click_element_when_visible("//input[@id='recaptcha-demo-submit']")
        assert self.browser.does_page_contain_element("//div[@class='recaptcha-success']")

    def test_cloudflare_challenge(self):
        page_url = "https://2captcha.com/demo/cloudflare-turnstile-challenge"
        self.browser = Selenium()
        self.browser.open_browser(
            browser="chrome",
            url=page_url,
        )
        captcha = TACaptchaSolver()
        cloudflare_challenge = captcha.get(
            captcha_type="cloudflare_challenge",
            service_provider_name="2captcha",
            service_provider_key=self.two_captcha_api_key,
            browser=self.browser,
        )
        assert cloudflare_challenge.solve()

    def test_cloudflare_turnstile(self):
        self.browser.open_browser(
            browser="chrome",
            url="https://2captcha.com/demo/cloudflare-turnstile",
            remote_url=self.remote_url,
            executable_path=self.executable_path,
        )
        captcha = TACaptchaSolver.get(
            captcha_type="cloudflare_turnstile",
            browser=self.browser,
            service_provider_name="2captcha",
            service_provider_key=self.two_captcha_api_key,
            click_xpath='//button[text()="Check"]',
            check_xpath='//*[text()="Captcha is passed successfully!"]',
        )
        assert captcha.solve()

    def test_image_all_params_browser(self):
        self.browser.open_browser(
            browser="chrome",
            url=self.image_url,
            remote_url=self.remote_url,
            executable_path=self.executable_path,
        )
        captcha = TACaptchaSolver.get(
            captcha_type="image",
            browser=self.browser,
            service_provider_name="captcha.guru",
            service_provider_key=self.captcha_guru_api_key,
            image_xpath="//img[@id='demoCaptcha_CaptchaImage']",
            input_xpath="//input[@id='captchaCode']",
            click_xpath="//input[@id='validateCaptchaButton']",
            check_xpath="//span[@id='validationResult']/span[@class='correct']",
            upper=False,
        )
        assert captcha.solve()

    def test_recaptchav2_all_params(self):
        self.browser.open_browser(
            browser="chrome",
            url=self.v2_url,
            remote_url=self.remote_url,
            executable_path=self.executable_path,
        )
        captcha = TACaptchaSolver.get(
            captcha_type="v2",
            browser=self.browser,
            captcha_guru_api_key=self.captcha_guru_api_key,
            click_xpath="//input[@id='recaptcha-demo-submit']",
            check_xpath="//div[@class='recaptcha-success']",
        )
        assert captcha.solve()

    def test_fun_captcha_req_params(self):
        self.browser.open_browser(
            browser="chrome",
            url=self.fun_captcha_url,
            remote_url=self.remote_url,
            executable_path=self.executable_path,
        )
        self.browser.input_text_when_element_is_visible("//input[@id='username']", "asdasdasdasd@asdasd.ads")
        self.browser.click_element_when_visible("//button[@id='reset-password-submit-button']")
        for i in range(10):
            try:
                self.browser.click_element("//button[@id='reset-password-submit-button']")
            except Exception:
                continue
        sleep(10)
        captcha = TACaptchaSolver.get(
            captcha_type="fun_captcha",
            browser=self.browser,
            service_provider_name="2captcha",
            service_provider_key=self.two_captcha_api_key,
        )
        captcha.solve()
        assert self.browser.does_page_contain_element("//input[@id='username']")

    def test_fun_captcha_all_params(self):
        self.browser.open_browser(
            browser="chrome",
            url=self.fun_captcha_url2,
            remote_url=self.remote_url,
            executable_path=self.executable_path,
        )
        self.browser.input_text_when_element_is_visible("//input[@id='username']", "Test")
        sleep(10)
        captcha = TACaptchaSolver.get(
            captcha_type="fun_captcha",
            browser=self.browser,
            service_provider_name="2captcha",
            service_provider_key=self.two_captcha_api_key,
            check_xpath="//h3[.='Solved!']",
        )
        assert captcha.solve()

    def test_recaptcha_not_solved(self):
        self.browser.open_browser(
            browser="chrome",
            url=self.v2_url,
            remote_url=self.remote_url,
            executable_path=self.executable_path,
        )
        captcha = TACaptchaSolver.get(
            captcha_type="v2",
            browser=self.browser,
            captcha_guru_api_key=self.captcha_guru_api_key,
            click_xpath="//input[@id='recaptcha-demo-submit']",
            check_xpath="//div[@id='not_existing_element']",
        )
        with pytest.raises(UICaptchaNotSolved):
            captcha.solve()

    def test_image_not_solved_browser(self):
        self.browser.open_browser(
            browser="chrome",
            url=self.image_url,
            remote_url=self.remote_url,
            executable_path=self.executable_path,
        )
        captcha = TACaptchaSolver.get(
            captcha_type="image",
            browser=self.browser,
            captcha_guru_api_key=self.captcha_guru_api_key,
            image_xpath="//img[@id='demoCaptcha_CaptchaImage']",
            input_xpath="//input[@id='captchaCode']",
            click_xpath="//input[@id='validateCaptchaButton']",
            check_xpath="//span[@id='not_existing_element']",
            upper=False,
        )
        with pytest.raises(UICaptchaNotSolved):
            captcha.solve()

    def test_image_not_solved_image(self):
        captcha = TACaptchaSolver.get(
            captcha_type="image",
            captcha_guru_api_key=self.captcha_guru_api_key,
            image_source=self.incorrect_image_source,
        )
        with pytest.raises(APICaptchaUnsolvable):
            captcha.solve()

    def test_hcaptcha_req_params(self):
        self.browser.open_browser(
            browser="chrome",
            url=self.hcaptcha_url,
            remote_url=self.remote_url,
            executable_path=self.executable_path,
        )
        sleep(5)
        captcha = TACaptchaSolver.get(
            captcha_type="hcaptcha",
            browser=self.browser,
            service_provider_name="2captcha",
            service_provider_key=self.two_captcha_api_key,
            check_xpath="//pre[@class='hcaptcha-success']",
            click_xpath="//input[@type='submit']",
        )
        assert captcha.solve()
