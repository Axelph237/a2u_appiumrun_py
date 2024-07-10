from django.apps import AppConfig
import logging
import os
import importlib
import a2u_appiumrun.data_handlers.test_handler as th

logger = logging.getLogger(__name__)


class AppiumRunConfig(AppConfig):
    name = 'a2u_appiumrun'

    def ready(self):
        # Add your initialization code here
        th.init(os.path.join(os.getcwd(), 'a2u_appiumrun', 'tests'))
        print("\nGathering modules...")
        print(str(th.modules))
