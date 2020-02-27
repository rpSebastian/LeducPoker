import sys
from loguru import logger
logger.remove()
fmt="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | " \
    "<level>{level}</level> | " \
    "<cyan>{file.path:}</cyan>:<cyan>{line:}</cyan> | " \
    "- <level>{message}</level>"
    # "<yellow>{process.name}</yellow> | " \
# fmt = "<level>{message}</level>"
logger.add(sys.stdout, format=fmt, level='DEBUG')
logger.add("logs/runtime.log", format=fmt)
# logger.add("file_1.log")
# @logger.catch
# def my_function(x, y, z):
#     # An error? It's caught anyway!
#     return 1 / (x + y + z)

# my_function(0, 0 , 0)
