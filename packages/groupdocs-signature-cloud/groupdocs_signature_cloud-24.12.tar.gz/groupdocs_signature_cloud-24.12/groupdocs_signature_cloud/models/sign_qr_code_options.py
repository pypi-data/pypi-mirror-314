# coding: utf-8

# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="SignQRCodeOptions.py">
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

from groupdocs_signature_cloud.models import SignTextOptions

class SignQRCodeOptions(SignTextOptions):
    """
    Represents the QR-code signature options
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'qr_code_type': 'str',
        'transparency': 'float',
        'code_text_alignment': 'str',
        'inner_margins': 'Padding',
        'logo_file_path': 'str'
    }

    attribute_map = {
        'qr_code_type': 'QRCodeType',
        'transparency': 'Transparency',
        'code_text_alignment': 'CodeTextAlignment',
        'inner_margins': 'InnerMargins',
        'logo_file_path': 'LogoFilePath'
    }

    def __init__(self, qr_code_type=None, transparency=None, code_text_alignment=None, inner_margins=None, logo_file_path=None, **kwargs):  # noqa: E501
        """Initializes new instance of SignQRCodeOptions"""  # noqa: E501

        self._qr_code_type = None
        self._transparency = None
        self._code_text_alignment = None
        self._inner_margins = None
        self._logo_file_path = None

        if qr_code_type is not None:
            self.qr_code_type = qr_code_type
        if transparency is not None:
            self.transparency = transparency
        if code_text_alignment is not None:
            self.code_text_alignment = code_text_alignment
        if inner_margins is not None:
            self.inner_margins = inner_margins
        if logo_file_path is not None:
            self.logo_file_path = logo_file_path

        base = super(SignQRCodeOptions, self)
        base.__init__(**kwargs)

        self.swagger_types.update(base.swagger_types)
        self.attribute_map.update(base.attribute_map)
    
    @property
    def qr_code_type(self):
        """
        Gets the qr_code_type.  # noqa: E501

        Get or set QRCode type. Value should be one from supported QRCode types list  # noqa: E501

        :return: The qr_code_type.  # noqa: E501
        :rtype: str
        """
        return self._qr_code_type

    @qr_code_type.setter
    def qr_code_type(self, qr_code_type):
        """
        Sets the qr_code_type.

        Get or set QRCode type. Value should be one from supported QRCode types list  # noqa: E501

        :param qr_code_type: The qr_code_type.  # noqa: E501
        :type: str
        """
        self._qr_code_type = qr_code_type
    
    @property
    def transparency(self):
        """
        Gets the transparency.  # noqa: E501

        Gets or sets the signature transparency (value from 0.0 (opaque) through 1.0 (clear)). Default value is 0 (opaque).               # noqa: E501

        :return: The transparency.  # noqa: E501
        :rtype: float
        """
        return self._transparency

    @transparency.setter
    def transparency(self, transparency):
        """
        Sets the transparency.

        Gets or sets the signature transparency (value from 0.0 (opaque) through 1.0 (clear)). Default value is 0 (opaque).               # noqa: E501

        :param transparency: The transparency.  # noqa: E501
        :type: float
        """
        if transparency is None:
            raise ValueError("Invalid value for `transparency`, must not be `None`")  # noqa: E501
        self._transparency = transparency
    
    @property
    def code_text_alignment(self):
        """
        Gets the code_text_alignment.  # noqa: E501

        Gets or sets the alignment of text in the result QR-code Default value is None  # noqa: E501

        :return: The code_text_alignment.  # noqa: E501
        :rtype: str
        """
        return self._code_text_alignment

    @code_text_alignment.setter
    def code_text_alignment(self, code_text_alignment):
        """
        Sets the code_text_alignment.

        Gets or sets the alignment of text in the result QR-code Default value is None  # noqa: E501

        :param code_text_alignment: The code_text_alignment.  # noqa: E501
        :type: str
        """
        if code_text_alignment is None:
            raise ValueError("Invalid value for `code_text_alignment`, must not be `None`")  # noqa: E501
        allowed_values = ["None", "Above", "Below", "Right"]  # noqa: E501
        if not code_text_alignment.isdigit():	
            if code_text_alignment not in allowed_values:
                raise ValueError(
                    "Invalid value for `code_text_alignment` ({0}), must be one of {1}"  # noqa: E501
                    .format(code_text_alignment, allowed_values))
            self._code_text_alignment = code_text_alignment
        else:
            self._code_text_alignment = allowed_values[int(code_text_alignment) if six.PY3 else long(code_text_alignment)]
    
    @property
    def inner_margins(self):
        """
        Gets the inner_margins.  # noqa: E501

        Gets or sets the space between QRCode elements and result image borders  # noqa: E501

        :return: The inner_margins.  # noqa: E501
        :rtype: Padding
        """
        return self._inner_margins

    @inner_margins.setter
    def inner_margins(self, inner_margins):
        """
        Sets the inner_margins.

        Gets or sets the space between QRCode elements and result image borders  # noqa: E501

        :param inner_margins: The inner_margins.  # noqa: E501
        :type: Padding
        """
        self._inner_margins = inner_margins
    
    @property
    def logo_file_path(self):
        """
        Gets the logo_file_path.  # noqa: E501

        Gets or sets the QR-code logo image file name. This property in use only if LogoStream is not specified. Using of this property could cause problems with verification. Use it carefully  # noqa: E501

        :return: The logo_file_path.  # noqa: E501
        :rtype: str
        """
        return self._logo_file_path

    @logo_file_path.setter
    def logo_file_path(self, logo_file_path):
        """
        Sets the logo_file_path.

        Gets or sets the QR-code logo image file name. This property in use only if LogoStream is not specified. Using of this property could cause problems with verification. Use it carefully  # noqa: E501

        :param logo_file_path: The logo_file_path.  # noqa: E501
        :type: str
        """
        self._logo_file_path = logo_file_path

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
        if not isinstance(other, SignQRCodeOptions):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
