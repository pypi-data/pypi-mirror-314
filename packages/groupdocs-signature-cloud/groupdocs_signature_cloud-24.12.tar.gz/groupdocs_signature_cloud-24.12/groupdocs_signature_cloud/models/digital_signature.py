# coding: utf-8

# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="DigitalSignature.py">
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

from groupdocs_signature_cloud.models import Signature

class DigitalSignature(Signature):
    """
    Contains digital Signature properties
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'comments': 'str',
        'is_valid': 'bool',
        'sign_time': 'datetime',
        'pdf_digital_signature': 'PdfDigitalSignature'
    }

    attribute_map = {
        'comments': 'Comments',
        'is_valid': 'IsValid',
        'sign_time': 'SignTime',
        'pdf_digital_signature': 'PdfDigitalSignature'
    }

    def __init__(self, comments=None, is_valid=None, sign_time=None, pdf_digital_signature=None, **kwargs):  # noqa: E501
        """Initializes new instance of DigitalSignature"""  # noqa: E501

        self._comments = None
        self._is_valid = None
        self._sign_time = None
        self._pdf_digital_signature = None

        if comments is not None:
            self.comments = comments
        if is_valid is not None:
            self.is_valid = is_valid
        if sign_time is not None:
            self.sign_time = sign_time
        if pdf_digital_signature is not None:
            self.pdf_digital_signature = pdf_digital_signature

        base = super(DigitalSignature, self)
        base.__init__(**kwargs)

        self.swagger_types.update(base.swagger_types)
        self.attribute_map.update(base.attribute_map)
    
    @property
    def comments(self):
        """
        Gets the comments.  # noqa: E501

        Gets or sets the signing purpose comment  # noqa: E501

        :return: The comments.  # noqa: E501
        :rtype: str
        """
        return self._comments

    @comments.setter
    def comments(self, comments):
        """
        Sets the comments.

        Gets or sets the signing purpose comment  # noqa: E501

        :param comments: The comments.  # noqa: E501
        :type: str
        """
        self._comments = comments
    
    @property
    def is_valid(self):
        """
        Gets the is_valid.  # noqa: E501

        Keeps true if this digital signature is valid and the document has not been tampered with  # noqa: E501

        :return: The is_valid.  # noqa: E501
        :rtype: bool
        """
        return self._is_valid

    @is_valid.setter
    def is_valid(self, is_valid):
        """
        Sets the is_valid.

        Keeps true if this digital signature is valid and the document has not been tampered with  # noqa: E501

        :param is_valid: The is_valid.  # noqa: E501
        :type: bool
        """
        if is_valid is None:
            raise ValueError("Invalid value for `is_valid`, must not be `None`")  # noqa: E501
        self._is_valid = is_valid
    
    @property
    def sign_time(self):
        """
        Gets the sign_time.  # noqa: E501

        Gets or sets the time the document was signed  # noqa: E501

        :return: The sign_time.  # noqa: E501
        :rtype: datetime
        """
        return self._sign_time

    @sign_time.setter
    def sign_time(self, sign_time):
        """
        Sets the sign_time.

        Gets or sets the time the document was signed  # noqa: E501

        :param sign_time: The sign_time.  # noqa: E501
        :type: datetime
        """
        if sign_time is None:
            raise ValueError("Invalid value for `sign_time`, must not be `None`")  # noqa: E501
        self._sign_time = sign_time
    
    @property
    def pdf_digital_signature(self):
        """
        Gets the pdf_digital_signature.  # noqa: E501

        Pdf digital signature properties  # noqa: E501

        :return: The pdf_digital_signature.  # noqa: E501
        :rtype: PdfDigitalSignature
        """
        return self._pdf_digital_signature

    @pdf_digital_signature.setter
    def pdf_digital_signature(self, pdf_digital_signature):
        """
        Sets the pdf_digital_signature.

        Pdf digital signature properties  # noqa: E501

        :param pdf_digital_signature: The pdf_digital_signature.  # noqa: E501
        :type: PdfDigitalSignature
        """
        self._pdf_digital_signature = pdf_digital_signature

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
        if not isinstance(other, DigitalSignature):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
