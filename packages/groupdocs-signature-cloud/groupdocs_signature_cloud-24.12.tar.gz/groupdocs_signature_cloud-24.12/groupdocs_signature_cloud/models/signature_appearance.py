# coding: utf-8

# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="SignatureAppearance.py">
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

class SignatureAppearance(object):
    """
    Appearance is a base class for keeping additional information for various options
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'appearance_type': 'str'
    }

    attribute_map = {
        'appearance_type': 'AppearanceType'
    }

    def __init__(self, appearance_type=None, **kwargs):  # noqa: E501
        """Initializes new instance of SignatureAppearance"""  # noqa: E501

        self._appearance_type = None

        if appearance_type is not None:
            self.appearance_type = appearance_type
    
    @property
    def appearance_type(self):
        """
        Gets the appearance_type.  # noqa: E501

        Specifies the type of appearance  # noqa: E501

        :return: The appearance_type.  # noqa: E501
        :rtype: str
        """
        return self._appearance_type

    @appearance_type.setter
    def appearance_type(self, appearance_type):
        """
        Sets the appearance_type.

        Specifies the type of appearance  # noqa: E501

        :param appearance_type: The appearance_type.  # noqa: E501
        :type: str
        """
        if appearance_type is None:
            raise ValueError("Invalid value for `appearance_type`, must not be `None`")  # noqa: E501
        allowed_values = ["Undefined", "PdfTextAnnotation", "PdfTextSticker", "Image", "DigitalSignature", "PdfDigitalSignature"]  # noqa: E501
        if not appearance_type.isdigit():	
            if appearance_type not in allowed_values:
                raise ValueError(
                    "Invalid value for `appearance_type` ({0}), must be one of {1}"  # noqa: E501
                    .format(appearance_type, allowed_values))
            self._appearance_type = appearance_type
        else:
            self._appearance_type = allowed_values[int(appearance_type) if six.PY3 else long(appearance_type)]

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
        if not isinstance(other, SignatureAppearance):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
