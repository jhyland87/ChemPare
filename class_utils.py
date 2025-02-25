import os
import sys
import time
import math
import re
import regex
from typing import List, Set, Tuple, Dict, Any, Optional, Union
from abcplus import ABCMeta, finalmethod
from urllib.parse import urlparse, parse_qs

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

class ClassUtils(metaclass=ABCMeta):
    @finalmethod
    def _parse_price(self, string:str) -> Optional[Dict]:
        """Parse a string for a price value (currency and value)

        Args:
            string (str): String with price

        Returns:
            Dict: Returns a dictionary with 'currency' and 'price' values
        """

        # Partial test at https://regex101.com/r/KFaYjq/4
        #iso_4217_pattern = r'(?:AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD?|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BOV|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHE|CHF|CHW|CLF|CLP|CNY|COP|COU|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR?|FJD|FKP|GBP|GEL|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|INR|IQD|IRR|ISK|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRU|MUR|MVR|MWK|MXN|MXV|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SRD|SSP|STN|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TWD|TZS|UAH|UGX|USD?|USN|UYI|UYU|UYW|UZS|VES|VND|VUV|WST|XAF|XAG|XAU|XBA|XBB|XBC|XBD|XCD|XDR|XOF|XPD|XPF|XPT|XSU|XTS|XUA|XXX|YER|ZAR|ZMW|ZWL)'
        pattern = (r'^(?:(?P<currency>\p{Sc}|'
           r'(?P<currency>'
            r'A(?:[EM]D|[FZ]N|LL|[NW]G|OA|RS|UD?)|'
            r'B(?:AM|[BHMNZS]D|DT|[GT]N|IF|OB|RL|WP|YR)|'
            r'C(?:AD|[DH]F|[LOU]P|NY|[RU]C|VE|ZK)|'
            r'D(?:JF|KK|OP|ZD)|'
            r'E(?:GP|RN|TB|UR?)|'
            r'F(?:JD|KP)|'
            r'G(?:[BGI]P|EL|HS|[YM]D|NF|TQ)|'
            r'H(?:KD|NL|RK|TG|UF)|'
            r'I(?:[NRD]R|LS|MP|QD|SK)|'
            r'J(?:EP|MD|OD|PY)|'
            r'K(?:[GE]S|HR|MF|[PR]W|[WY]D|ZT)|'
            r'L(?:AK|BP|KR|[RY]D|SL)|'
            r'M(?:[AK]D|DL|GA|[MW]K|NT|OP|RO|[UVY]R|[XZ]N)|'
            r'N(?:[AZ]D|GN|IO|OK|PR)|'
            r'(?:QA|OM|YE)R|'
            r'P(?:AB|[EKL]N|GK|HP|KR|YG)|'
            r'R(?:ON|SD|UB|WF)|'
            r'S(?:[AC]R|[BRGDT]D|DG|EK|[HY]P|[LZP]L|OS|VC)|'
            r'T(?:HB|[JZ]S|MT|[NTVW]D|OP|RY)|'
            r'U(?:AH|GX|SD?|YU|ZS)|'
            r'V(?:EF|ND|UV)|WST|'
            r'X(?:[AOP]F|CD|DR)|'
            r'Z(?:AR|MW|WD)))'
           r'\s?(?P<price>[0-9]+(?:[,\.][0-9]+)*)'
           r'|(?P<price>[0-9]+(?:[,\.][0-9]+)*)\s?(?P<currency>\p{Sc}|'
           #r'(?:us|au|ca)d?|eur?|chf|rub|gbp|jyp|pln|sek|uah|hrk)'
           r'(?P<currency>'
            r'A(?:[EM]D|[FZ]N|LL|[NW]G|OA|RS|UD?)|'
            r'B(?:AM|[BHMNZS]D|DT|[GT]N|IF|OB|RL|WP|YR)|'
            r'C(?:AD|[DH]F|[LOU]P|NY|[RU]C|VE|ZK)|'
            r'D(?:JF|KK|OP|ZD)|'
            r'E(?:GP|RN|TB|UR?)|'
            r'F(?:JD|KP)|'
            r'G(?:[BGI]P|EL|HS|[YM]D|NF|TQ)|'
            r'H(?:KD|NL|RK|TG|UF)|'
            r'I(?:[NRD]R|LS|MP|QD|SK)|'
            r'J(?:EP|MD|OD|PY)|'
            r'K(?:[GE]S|HR|MF|[PR]W|[WY]D|ZT)|'
            r'L(?:AK|BP|KR|[RY]D|SL)|'
            r'M(?:[AK]D|DL|GA|[MW]K|NT|OP|RO|[UVY]R|[XZ]N)|'
            r'N(?:[AZ]D|GN|IO|OK|PR)|'
            r'(?:QA|OM|YE)R|'
            r'P(?:AB|[EKL]N|GK|HP|KR|YG)|'
            r'R(?:ON|SD|UB|WF)|'
            r'S(?:[AC]R|[BRGDT]D|DG|EK|[HY]P|[LZP]L|OS|VC)|'
            r'T(?:HB|[JZ]S|MT|[NTVW]D|OP|RY)|'
            r'U(?:AH|GX|SD?|YU|ZS)|'
            r'V(?:EF|ND|UV)|WST|'
            r'X(?:[AOP]F|CD|DR)|'
            r'Z(?:AR|MW|WD)))'
           r')$')
        
        matches = regex.match(pattern, string, regex.IGNORECASE)
        if not matches:
            return None
        
        return matches.groupdict()

    @finalmethod
    def _parse_quantity(self, string:str) -> Optional[Dict]:
        """Parse a string for the quantity and unit of measurement

        Args:
            string (str): Suspected quantity string

        Returns:
            Optional[Dict]: Returns a dictionary with the 'quantity' and 'uom' values
        """
        if type(string) is not str:
            return None
        
        string = string.strip()

        if not string or string.isspace():
            return None
        
        #https://regex101.com/r/am7wLs/3
        #qty_pattern = re.compile(r'(?P<quantity>[0-9\.\,]+)\s?(?P<uom>oz|ounces?|grams?|g|lbs?|pounds?|l|qt|m?[glm]|milli(?:gram|meter|liter)s?)', re.IGNORECASE)
        pattern = r'(?P<quantity>\d+(?:[\.,]\d+)?)(?=\s?(?:[μmck]?[glm]|gal|gallon))\s?(?P<uom>[μmck]?[glm]|gal|gallon)(?:[^\w]|$)'

        matches = regex.match(pattern, string, regex.IGNORECASE)

        if not matches: 
            return None
        
        return matches.groupdict()

    @finalmethod 
    def _get_param_from_url(self, url:str, param:str=None) -> Optional[Any]:
        """Get a specific arameter from a GET URL

        Args:
            url (str): HREF address
            param (str): Param key to find (optional)

        Returns:
            Any: Whatver the value was of the key, or nothing

        Example:
            self._get_param_from_url('http://google.com?foo=bar&product_id=12345')
            {'foo':'bar','product_id':'12345'}
            self._get_param_from_url('http://google.com?foo=bar&product_id=12345', 'product_id')
            '12345'
        """

        parsed_url = urlparse(url)
        parsed_query = parse_qs(parsed_url.query)

        # Replace any ['values'] with just 'values'
        parsed_query = {k: v[0] if len(v) == 1 else v for k, v in parsed_query.items()}

        if not param:
            return parsed_query
        
        # If no specific parameter was defined, then just return this
        if param not in parsed_query:
            return None
        
        if not parsed_query[param]:
            return None
        
        return parsed_query[param]
    
    @finalmethod
    def _split_array_into_groups(
            self, 
            arr: List, 
            size: int=2) -> List:
        """Splits an array into sub-arrays of 2 elements each.

        Args:
            arr: The input array.
            size: Size to group array elements by

        Returns:
            A list of sub-arrays, where each sub-array contains {size} elements, or an empty list if the input array is empty.

        Example:
            self._split_array_into_groups(['Variant', '500 g', 'CAS', '1762-95-4'])
            [['Variant', '500 g'],['CAS', '1762-95-4']]
        """

        result = []
        for i in range(0, len(arr), size):
            result.append(arr[i:i + size])

        return result
    
    @finalmethod
    def _nested_arr_to_dict(self, arr: List) -> Optional[Dict]:
        """Splits an array into sub-arrays of 2 elements each.

        Args:
            arr: The input array.
            size: Size to group array elements by

        Returns:
            A list of sub-arrays, where each sub-array contains {size} elements, or an empty list if the input array is empty.

        Example:
            self._split_array_into_groups(['Variant', '500 g', 'CAS', '1762-95-4'])
            [['Variant', '500 g'],['CAS', '1762-95-4']]
        """

        # Only works if the array has even amount of elements
        if len(arr) % 2 != 0: 
            return None

        grouped_elem = self._split_array_into_groups(arr, 2)

        variant_dict = [dict(item) for item in [grouped_elem]]

        return variant_dict[0] or None
    
    @property
    @finalmethod 
    def _epoch(self) -> int:
        """Get epoch string - Used for unique values in searches (sometimes _)

        Returns:
            int: Current time in epoch
        """

        return math.floor(time.time()*1000)
    
    @finalmethod 
    def _is_cas(self, value:Any) -> bool:
        """Check if a string is a valid CAS registry number

        This is done by taking the first two segments and iterating over each individual
        intiger in reverse order, multiplying each by its position, then taking the 
        modulous of the sum of those values.

        Example:
            1234-56-6 is valid because the result of the below equation matches the checksum,
            (which is 6)
                (6*1 + 5*2 + 4*3 + 3*4 + 2*5 + 1*6) % 10 == 6

            This can be simplified in the below aggregation:
                cas_chars = [1, 2, 3, 4, 5, 6]
                sum([(idx+1)*int(n) for idx, n in enumerate(cas_chars[::-1])]) % 10

        See: 
            https://www.cas.org/training/documentation/chemical-substances/checkdig

        Args:
            value (str): The value to determine if its a CAS # or not

        Returns:
            bool: True if its a valid format and the checksum matches
        """

        if type(value) is not str:
            return False
        
        # value='1234-56-6'
        # https://regex101.com/r/xPF1Yp/2
        cas_pattern_check = re.match(r'^(?P<seg_a>[0-9]{2,7})-(?P<seg_b>[0-9]{2})-(?P<checksum>[0-9])$', value)

        if cas_pattern_check is None:
            return False

        cas_dict = cas_pattern_check.groupdict()
        # cas_dict = dict(seg_a='1234', seg_b='56', checksum='6')

        cas_chars = list(cas_dict['seg_a'] + cas_dict['seg_b'])
        # cas_chars = ['1','2','3','4','5','6']

        checksum = sum([(idx+1)*int(n) for idx, n in enumerate(cas_chars[::-1])]) % 10
        # checksum = 6

        return int(checksum) == int(cas_dict['checksum'])

    @finalmethod 
    def _cast_type(self, value: Union[str,int,float,bool] = None) -> Any:
        """Cast a value to the proper type. This is mostly used for casting int/float/bool

        Args:
            value (Union[str,int,float,bool]): Value to be casted (optional)

        Returns:
            Any: Casted value
        """

        # If it's not a string, then its probably a valid type..
        if type(value) != str:
            return value
        
        # Most castable values just need to be trimmed to be compatible
        value = value.strip()

        if not value or value.isspace():
            return None
            
        if value.lower() == 'true':
            return True
            
        if value.lower() == 'false':
            return False
            
        if value.isdecimal() or re.match(f'^[0-9]+.[0-9]+$', value): 
            return float(value) 
                
        if value.isnumeric() or re.match(f'^[0-9]+$', value):
            return int(value)   
            
        return value
    
    @finalmethod 
    def _is_cas(self, value:Any) -> bool:
        """Check if a string is a valid CAS registry number

        This is done by taking the first two segments and iterating over each individual
        intiger in reverse order, multiplying each by its position, then taking the 
        modulous of the sum of those values.

        Example:
            1234-56-6 is valid because the result of the below equation matches the checksum,
            (which is 6)
                (6*1 + 5*2 + 4*3 + 3*4 + 2*5 + 1*6) % 10 == 6

            This can be simplified in the below aggregation:
                cas_chars = [1, 2, 3, 4, 5, 6]
                sum([(idx+1)*int(n) for idx, n in enumerate(cas_chars[::-1])]) % 10

        See: 
            https://www.cas.org/training/documentation/chemical-substances/checkdig

        Args:
            value (str): The value to determine if its a CAS # or not

        Returns:
            bool: True if its a valid format and the checksum matches
        """

        if type(value) is not str:
            return False
        
        # value='1234-56-6'
        # https://regex101.com/r/xPF1Yp/2
        cas_pattern_check = re.match(r'^(?P<seg_a>[0-9]{2,7})-(?P<seg_b>[0-9]{2})-(?P<checksum>[0-9])$', value)

        if cas_pattern_check is None:
            return False

        cas_dict = cas_pattern_check.groupdict()
        # cas_dict = dict(seg_a='1234', seg_b='56', checksum='6')

        cas_chars = list(cas_dict['seg_a'] + cas_dict['seg_b'])
        # cas_chars = ['1','2','3','4','5','6']

        checksum = sum([(idx+1)*int(n) for idx, n in enumerate(cas_chars[::-1])]) % 10
        # checksum = 6

        return int(checksum) == int(cas_dict['checksum'])
    
__all__ = 'ClassUtils'