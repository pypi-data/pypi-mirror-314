from abc import ABC, abstractmethod

"""
ai方法基类
"""


class aiBase(ABC):

    @abstractmethod
    def aiClick(self, value, *args, **kwargs):
        pass
