"""Create a singleton manager to ensure a single instance of Selenium."""

import inspect
from RPA.Browser.Selenium import Selenium  # type: ignore


class SeleniumManager:
    """Singleton manager to ensure a single instance of Selenium."""

    _portal_instances: dict[str, Selenium] = {}

    @classmethod
    def get_instance(cls: Selenium) -> Selenium:
        """Get the instance of Selenium for the calling module. If it does not exist, create it."""
        caller_module = cls._find_caller_module()
        if not caller_module:
            raise ValueError("No valid portal found in the stack.")

        if caller_module not in cls._portal_instances:
            cls._portal_instances[caller_module] = Selenium()

        return cls._portal_instances[caller_module]

    @staticmethod
    def _find_caller_module() -> str:
        """Find the calling module's name based on specific criteria."""
        stack = inspect.stack()
        for frame_info in stack:
            module = inspect.getmodule(frame_info.frame)
            if module:
                for name in module.__name__.split("."):
                    if name.startswith("t_") and name != "t_page_object":
                        return name
        return ""
