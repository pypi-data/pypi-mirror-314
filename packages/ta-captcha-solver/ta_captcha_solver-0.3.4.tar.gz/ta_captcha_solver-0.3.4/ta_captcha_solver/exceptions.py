class APICaptchaNotReady(Exception):
    """
    API: Captcha is still being solved
    """

    pass


class APICaptchaUnsolvable(Exception):
    """
    API: Error that captcha cannot be solved
    """

    pass


class APICaptchaNoSlotAvailableException(Exception):
    """
    API: Error that captcha has no slot available to be solved
    """


class APICaptchaWrongCaptchaID(Exception):
    """
    API: Error that captcha has wrong ID
    """


class UICaptchaNotSolved(Exception):
    """
    UI: Cannot find xpath that indicates solved captcha
    """

    pass


class ImageCaptchaNotSolved(Exception):
    """
    UI: Cannot find image source for solve captcha
    """

    pass


class ParamsException(Exception):
    """
    Some params are missing for captcha resolving
    """

    pass


class LowBalanceException(Exception):
    """
    API: Tool balance is low
    """

    pass


class FrameException(Exception):
    """
    UI: Captcha is probably inside iframe
    """

    pass


class ServiceProviderException(Exception):
    """
    Service provider is down
    """

    pass


class NoCaptchaException(Exception):
    """
    If there is no captcha on the page
    """

    pass


class NoTokenCaptchaException(Exception):
    """
    If there is no token to solve captcha on the page
    """

    pass
