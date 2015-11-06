from app.meloentjoer.config.GeneralConfig import GeneralConfig
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(4)
config = GeneralConfig()
