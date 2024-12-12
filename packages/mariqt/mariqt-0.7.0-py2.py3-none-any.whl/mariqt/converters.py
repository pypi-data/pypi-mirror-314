import abc
import inspect
import math
import datetime

import mariqt.variables as miqtv

class ConverterBase(abc.ABC):
    """ base of container that holds a convert function"""
    def __init__(self,name="undefined"):
        self._name = name
        self._params = None

    def setParams(self,params):
        self._params = params

    def getParams(self):
        return self._params

    def getName(self):
        return self._name

    @abc.abstractmethod
    def convert(self,value:str) -> str:
        """ takes string argument and converts to string """
        pass

    @staticmethod
    def getAllConverters(baseClass):
        """ Gets all non abstract sub classes """
        subClasses = []
        for subClass in baseClass.__subclasses__():
            if not inspect.isabstract(subClass):
                subClasses.append(subClass)
            subClasses += ConverterBase.getAllConverters(subClass)
        return subClasses


class NoneConverter(ConverterBase):
    """ Converter that does nothing """
    def __init__(self):
        super().__init__("None")

    def convert(self, value: str) -> str:
        return value


class Rad2DegreeConvert(ConverterBase):
    def __init__(self):
        super().__init__("Rad2Degree")

    def convert(self, value: str) -> str:
        return str(math.degrees(float(value)))


class DateConverter(ConverterBase):
    def __init__(self):
        super().__init__("Date")

    def convert(self, value: str) -> str:
        dt = datetime.datetime.strptime(value,self.getParams())
        return dt.strftime(miqtv.date_formats["mariqt"].split(" ")[0])
         

class TimeConverter(ConverterBase):
    def __init__(self):
        super().__init__("Time")

    def convert(self, value: str) -> str:
        dt = datetime.datetime.strptime(value,self.getParams())
        return dt.strftime(miqtv.date_formats["mariqt"].split(" ")[1])


class DateTimeConverter(ConverterBase):
    def __init__(self):
        super().__init__("DateTime")

    def convert(self, value: str) -> str:
        dt = datetime.datetime.strptime(value,self.getParams())
        return dt.strftime(miqtv.date_formats["mariqt"])


class UnixDateTimeConverter(ConverterBase):
    def __init__(self):
        super().__init__("Unix DateTime")

    def convert(self, value: str) -> str:
        dt = datetime.datetime.utcfromtimestamp(float(value))
        return dt.strftime(miqtv.date_formats["mariqt"])


class DateSince1970Converter(ConverterBase):
    def __init__(self):
        super().__init__("Date days since 1970")

    def convert(self, value: str) -> str:
        dt = datetime.datetime(1970,1,1,0,0,0) + datetime.timedelta(days=float(value))
        return dt.strftime(miqtv.date_formats["mariqt"].split(" ")[0])


class DoubleMinMaxConverter(ConverterBase):
    """ Set values outside min max range to None """
    def __init__(self):
        super().__init__("Double Min Max Converer")

    def convert(self, value: str) -> str:
        if float(value) < self.getParams()[1] and float(value) > self.getParams()[0]:
            return str(float(value))
        else:
            return None


class DoubleConstOffsetConverter(ConverterBase):
    """ add a const offset to value """
    def __init__(self):
        super().__init__("Double Const Offset Converter")

    def convert(self, value: str) -> str:
        return str(float(value) + self.getParams())


class DoubleMinMaxAndOffsetConverter(ConverterBase):
    """ Set values outside min max range to None and add const offset if not None """
    def __init__(self):
        super().__init__("Double Min Max + Offset Converer")
        self._minMaxConverter = DoubleMinMaxConverter()
        self._offsetConverter = DoubleConstOffsetConverter()

    def convert(self, value: str) -> str:
        value = self._minMaxConverter.convert(value)
        if not value is None:
            value =  self._offsetConverter.convert(value)
        return value

    def setParams(self,params):
        self._minMaxConverter.setParams(params[0])
        self._offsetConverter.setParams(params[1])

    def getParams(self):
        return [self._minMaxConverter.getParams(),self._offsetConverter.getParams()]


class DoubleConstFactorConverter(ConverterBase):
    """ multiply with const offset to value """
    def __init__(self):
        super().__init__("Double Const Factor Converter")

    def convert(self, value: str) -> str:
        return str(float(value) * self.getParams())


class ConstDoubleConverter(ConverterBase):
    """ returns const value """
    def __init__(self):
        super().__init__("Const Double")

    def convert(self, value: str) -> str:
        return str(self.getParams())


class ConstDateConverter(ConverterBase):
    def __init__(self):
        super().__init__("Const Date")

    def convert(self, value: str) -> str:
        return self.getParams()

    def setParams(self,params):
        "date in %Y-%m-%d"
        # check format
        dt = datetime.datetime.strptime(params,miqtv.date_formats["mariqt"].split(" ")[0])
        super().setParams(params)


class ConstTimeConverter(ConverterBase):
    def __init__(self):
        super().__init__("Const Time")

    def convert(self, value: str) -> str:
        return self.getParams()

    def setParams(self,params):
        "time in %H:%M:%S.f"
        # check format
        dt = datetime.datetime.strptime(params,miqtv.date_formats["mariqt"].split(" ")[1])
        super().setParams(params)


class ConstDateTimeConverter(ConverterBase):
    def __init__(self):
        super().__init__("Const DateTime")

    def convert(self, value: str) -> str:
        return self.getParams()

    def setParams(self,params):
        "date time in %Y-%m-%d %H:%M:%S.%f"
        # check format
        dt = datetime.datetime.strptime(params,miqtv.date_formats["mariqt"])
        super().setParams(params)