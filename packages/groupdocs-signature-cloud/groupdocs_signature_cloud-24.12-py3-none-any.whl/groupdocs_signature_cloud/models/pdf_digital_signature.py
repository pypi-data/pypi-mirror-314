# coding: utf-8

# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="PdfDigitalSignature.py">
#   Copyright (c) 2003-2023 Aspose Pty Ltd
# </copyright>
# <summary>
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
# </summary>
# -----------------------------------------------------------------------------------

import pprint
import re  # noqa: F401

import six

class PdfDigitalSignature(object):
    """
    Contains pdf digital Signature properties
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'contact_info': 'str',
        'location': 'str',
        'reason': 'str',
        'type': 'str',
        'time_stamp': 'TimeStamp',
        'show_properties': 'bool'
    }

    attribute_map = {
        'contact_info': 'ContactInfo',
        'location': 'Location',
        'reason': 'Reason',
        'type': 'Type',
        'time_stamp': 'TimeStamp',
        'show_properties': 'ShowProperties'
    }

    def __init__(self, contact_info=None, location=None, reason=None, type=None, time_stamp=None, show_properties=None, **kwargs):  # noqa: E501
        """Initializes new instance of PdfDigitalSignature"""  # noqa: E501

        self._contact_info = None
        self._location = None
        self._reason = None
        self._type = None
        self._time_stamp = None
        self._show_properties = None

        if contact_info is not None:
            self.contact_info = contact_info
        if location is not None:
            self.location = location
        if reason is not None:
            self.reason = reason
        if type is not None:
            self.type = type
        if time_stamp is not None:
            self.time_stamp = time_stamp
        if show_properties is not None:
            self.show_properties = show_properties
    
    @property
    def contact_info(self):
        """
        Gets the contact_info.  # noqa: E501

        Information provided by the signer to enable a recipient to contact the signer  # noqa: E501

        :return: The contact_info.  # noqa: E501
        :rtype: str
        """
        return self._contact_info

    @contact_info.setter
    def contact_info(self, contact_info):
        """
        Sets the contact_info.

        Information provided by the signer to enable a recipient to contact the signer  # noqa: E501

        :param contact_info: The contact_info.  # noqa: E501
        :type: str
        """
        self._contact_info = contact_info
    
    @property
    def location(self):
        """
        Gets the location.  # noqa: E501

        The CPU host name or physical location of the signing.  # noqa: E501

        :return: The location.  # noqa: E501
        :rtype: str
        """
        return self._location

    @location.setter
    def location(self, location):
        """
        Sets the location.

        The CPU host name or physical location of the signing.  # noqa: E501

        :param location: The location.  # noqa: E501
        :type: str
        """
        self._location = location
    
    @property
    def reason(self):
        """
        Gets the reason.  # noqa: E501

        The reason for the signing, such as (I agreeРІР‚В¦).  # noqa: E501

        :return: The reason.  # noqa: E501
        :rtype: str
        """
        return self._reason

    @reason.setter
    def reason(self, reason):
        """
        Sets the reason.

        The reason for the signing, such as (I agreeРІР‚В¦).  # noqa: E501

        :param reason: The reason.  # noqa: E501
        :type: str
        """
        self._reason = reason
    
    @property
    def type(self):
        """
        Gets the type.  # noqa: E501

        Type of Pdf digital signature.  # noqa: E501

        :return: The type.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type.

        Type of Pdf digital signature.  # noqa: E501

        :param type: The type.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        allowed_values = ["Signature", "Certificate"]  # noqa: E501
        if not type.isdigit():	
            if type not in allowed_values:
                raise ValueError(
                    "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                    .format(type, allowed_values))
            self._type = type
        else:
            self._type = allowed_values[int(type) if six.PY3 else long(type)]
    
    @property
    def time_stamp(self):
        """
        Gets the time_stamp.  # noqa: E501

        Time stamp for Pdf digital signature. Default value is null.  # noqa: E501

        :return: The time_stamp.  # noqa: E501
        :rtype: TimeStamp
        """
        return self._time_stamp

    @time_stamp.setter
    def time_stamp(self, time_stamp):
        """
        Sets the time_stamp.

        Time stamp for Pdf digital signature. Default value is null.  # noqa: E501

        :param time_stamp: The time_stamp.  # noqa: E501
        :type: TimeStamp
        """
        if time_stamp is None:
            raise ValueError("Invalid value for `time_stamp`, must not be `None`")  # noqa: E501
        self._time_stamp = time_stamp
    
    @property
    def show_properties(self):
        """
        Gets the show_properties.  # noqa: E501

        Force to show/hide signature properties  # noqa: E501

        :return: The show_properties.  # noqa: E501
        :rtype: bool
        """
        return self._show_properties

    @show_properties.setter
    def show_properties(self, show_properties):
        """
        Sets the show_properties.

        Force to show/hide signature properties  # noqa: E501

        :param show_properties: The show_properties.  # noqa: E501
        :type: bool
        """
        if show_properties is None:
            raise ValueError("Invalid value for `show_properties`, must not be `None`")  # noqa: E501
        self._show_properties = show_properties

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, PdfDigitalSignature):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
