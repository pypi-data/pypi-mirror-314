from .internal import Midas as Internal
from .types import RateListItem, ValueInfoItem, RateInfo
from typing import Literal
from enum import Enum
import json

class RINFilter(Enum):
        """Filter options for the RIN list."""
        ALL = 0
        TARIFF = 1
        GHG_EMISSION = 2
        FLEX_ALERT = 3

class Midas(Internal):

    def GetAvailableRates(self, signaltype: RINFilter) -> 'list[RateListItem]':
        """
        Get all the available rates.
        """

        def __rateListItemHook(dict):
             return RateListItem(**dict)

        url = 'https://midasapi.energy.ca.gov/api/valuedata?signaltype=' + str(signaltype.value)
        response = self.__request('GET', url)
        return (json.loads(response, object_hook=__rateListItemHook))
    
    def GetRateInfo(self, rateID: str, queryType: Literal['alldata', 'realtime'] = 'alldata') -> RateInfo:
        """
        Returns data about a given a rate.
        """

        def __rateInfoObjectHook(dict):
            # this has to handle both the parent object and its children
            if "DateStart" in dict:
                return ValueInfoItem(**dict)
            elif "RateID" in dict:
                return RateInfo(**dict)
            else:
                raise "Invalid object type for __rateInfoObjectHook"
            
        # TODO what does queryType=realtime even do? all properties are None
        url = 'https://midasapi.energy.ca.gov/api/valuedata?id=' + rateID + '&querytype=' + queryType
        pricing_response = self.__request('GET', url)

        return (json.loads(pricing_response, object_hook=__rateInfoObjectHook))