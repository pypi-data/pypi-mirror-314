import time
from typing import Any

from .drission_bot import DrissionBot
from .selenium_bot import SeleniumBot
from ..common import BaseConfig, RuntimeConfig
from ..utils import AccountManager, KeyManager


def get_bot(runtime_config: RuntimeConfig, app_config: BaseConfig) -> Any:
    bot_classes = {"selenium": SeleniumBot, "drission": DrissionBot}

    bot_type = runtime_config.bot_type
    logger = runtime_config.logger
    key_manager = KeyManager(logger, app_config.encryption)
    account_manager = AccountManager(logger, key_manager)

    if bot_type not in bot_classes:
        raise ValueError(f"Unsupported automator type: {bot_type}")

    bot = bot_classes[bot_type](runtime_config, app_config, key_manager, account_manager)

    if bot.new_profile:
        init_new_profile(bot)
    return bot


def init_new_profile(bot: Any) -> None:
    # visit some websites for new chrome profile
    websites: list[str] = [
        # "https://www.google.com",
        # "https://www.youtube.com",
        # "https://www.wikipedia.org",
    ]

    for url in websites:
        if isinstance(bot, DrissionBot):
            bot.page.get(url)
        elif isinstance(bot, SeleniumBot):
            bot.driver.get(url)

        time.sleep(4)
