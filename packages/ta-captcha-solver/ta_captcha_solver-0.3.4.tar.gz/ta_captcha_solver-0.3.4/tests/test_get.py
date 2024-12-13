#!/usr/bin/env python

import pytest
import os

from RPA.Browser.Selenium import Selenium

from ta_captcha_solver.ta_captcha_solver import TACaptchaSolver
from ta_captcha_solver.exceptions import ParamsException
from ta_captcha_solver.captcha.image_captcha import ImageCaptcha
from ta_captcha_solver.captcha.re_captcha_v2 import ReCaptchaV2


class TestGet:
    """
    For succesfull execution you need to have such env vars with valid values available in your system:
      - CAPTCHA_GURU_API_KEY
      - TWO_CAPTCHA_API_KEY
    """

    @classmethod
    def setup_class(self):
        self.captcha_guru_api_key = os.getenv("CAPTCHA_GURU_API_KEY")
        self.two_captcha_api_key = os.getenv("TWO_CAPTCHA_API_KEY")

    def test_empty_params(self):
        with pytest.raises(ParamsException) as e:
            TACaptchaSolver.get()
        assert "No captcha_type provided" in str(e.value)

    def test_random_params(self):
        with pytest.raises(TypeError):
            TACaptchaSolver.get("!!!!", 123, [])

    def test_no_type(self):
        with pytest.raises(ParamsException) as e:
            TACaptchaSolver.get(browser=Selenium(), captcha_guru_api_key=self.captcha_guru_api_key)
        assert "No captcha_type provided" in str(e.value)

    def test_no_browser_for_v2(self):
        with pytest.raises(ParamsException) as e:
            TACaptchaSolver.get(captcha_type="v2", captcha_guru_api_key=self.captcha_guru_api_key)
        assert "No browser provided" in str(e.value)

    def test_no_browser_for_fun_captcha(self):
        with pytest.raises(ParamsException) as e:
            TACaptchaSolver.get(captcha_type="fun_captcha", captcha_guru_api_key=self.captcha_guru_api_key)
        assert "No browser provided" in str(e.value)

    def test_no_service_provider_info(self):
        with pytest.raises(ParamsException) as e:
            TACaptchaSolver.get(captcha_type="v2", browser=Selenium())
        assert "No Service Provider Name or Key provided" in str(e.value)

    def test_no_service_provider_name(self):
        with pytest.raises(ParamsException) as e:
            TACaptchaSolver.get(
                captcha_type="v2",
                browser=Selenium(),
                service_provider_key=self.two_captcha_api_key,
            )
        assert "No Service Provider Name or Key provided" in str(e.value)

    def test_no_service_provider_key(self):
        with pytest.raises(ParamsException) as e:
            TACaptchaSolver.get(captcha_type="v2", browser=Selenium(), service_provider_name="2captcha")
        assert "No Service Provider Name or Key provided" in str(e.value)

    def test_no_image_source_or_browser(self):
        with pytest.raises(ParamsException) as e:
            TACaptchaSolver.get(captcha_type="image", captcha_guru_api_key=self.captcha_guru_api_key)
        assert "No browser or image source provided." in str(e.value)

    def test_image_source_and_browser(self):
        with pytest.raises(ParamsException) as e:
            TACaptchaSolver.get(
                captcha_type="image",
                browser=Selenium(),
                image_source="cdefre.jpg",
                captcha_guru_api_key=self.captcha_guru_api_key,
            )
        assert "Browser and image source both provided" in str(e.value)

    def test_incorret_image_source(self):
        with pytest.raises(ParamsException) as e:
            TACaptchaSolver.get(
                captcha_type="image",
                captcha_guru_api_key=self.captcha_guru_api_key,
                image_source="cdefre",
            )
        assert "No image path valid provided on image_source" in str(e.value)

    def test_incorrect_type(self):
        with pytest.raises(ParamsException) as e:
            TACaptchaSolver.get(
                captcha_type="123",
                browser=Selenium(),
                captcha_guru_api_key=self.captcha_guru_api_key,
            )
        assert "Incorrect captcha_type" in str(e.value)

    def test_incorrect_browser(self):
        with pytest.raises(NotImplementedError) as e:
            TACaptchaSolver.get(
                captcha_type="v2",
                browser=123,
                captcha_guru_api_key=self.captcha_guru_api_key,
            )
        assert "Currently only Selenium is supported!" in str(e.value)

    def test_incorrect_service_provider_name(self):
        with pytest.raises(ParamsException) as e:
            TACaptchaSolver.get(
                captcha_type="v2",
                browser=Selenium(),
                service_provider_name="123",
                service_provider_key=self.two_captcha_api_key,
            )
        assert "Unknown Service Provider" in str(e.value)

    def test_incorrect_captcha_guru_api_key_value(self):
        with pytest.raises(ParamsException) as e:
            TACaptchaSolver.get(
                captcha_type="v2",
                browser=Selenium(),
                service_provider_name="captcha.guru",
                service_provider_key="incorrect_key",
            )
        assert "Incorrect api_key provided" in str(e.value)

    def test_incorrect_2_captcha_key_value(self):
        with pytest.raises(ParamsException) as e:
            TACaptchaSolver.get(
                captcha_type="v2",
                browser=Selenium(),
                service_provider_name="2captcha",
                service_provider_key="incorrect_key",
            )
        assert "Incorrect api_key provided" in str(e.value)

    def test_no_image_xpath(self):
        with pytest.raises(ParamsException) as e:
            TACaptchaSolver.get(
                captcha_type="image",
                browser=Selenium(),
                captcha_guru_api_key=self.captcha_guru_api_key,
            )
        assert "No image_xpath provided" in str(e.value)

    def test_image_captcha_guru_valid_creation(self):
        captcha = TACaptchaSolver.get(
            captcha_type="image",
            browser=Selenium(),
            captcha_guru_api_key=self.captcha_guru_api_key,
            image_xpath="123",
        )
        assert isinstance(captcha, ImageCaptcha)

    def test_recaptchav2_captcha_guru_valid_creation(self):
        captcha = TACaptchaSolver.get(
            captcha_type="v2",
            browser=Selenium(),
            captcha_guru_api_key=self.captcha_guru_api_key,
        )
        assert isinstance(captcha, ReCaptchaV2)

    def test_image_captcha_guru_valid_creation2(self):
        captcha = TACaptchaSolver.get(
            captcha_type="image",
            browser=Selenium(),
            service_provider_name="captcha.guru",
            service_provider_key=self.captcha_guru_api_key,
            image_xpath="123",
        )
        assert isinstance(captcha, ImageCaptcha)

    def test_recaptchav2_2_captcha_valid_creation(self):
        captcha = TACaptchaSolver.get(
            captcha_type="v2",
            browser=Selenium(),
            service_provider_name="2captcha",
            service_provider_key=self.two_captcha_api_key,
        )
        assert isinstance(captcha, ReCaptchaV2)
