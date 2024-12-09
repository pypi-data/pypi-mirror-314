# coding: utf-8

# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="Signature.py">
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

class Signature(object):
    """
    Describes base class for signatures
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'signature_type': 'str',
        'page_number': 'int',
        'signature_id': 'str',
        'is_signature': 'bool',
        'created_on': 'datetime',
        'modified_on': 'datetime',
        'top': 'int',
        'left': 'int',
        'width': 'int',
        'height': 'int'
    }

    attribute_map = {
        'signature_type': 'SignatureType',
        'page_number': 'PageNumber',
        'signature_id': 'SignatureId',
        'is_signature': 'IsSignature',
        'created_on': 'CreatedOn',
        'modified_on': 'ModifiedOn',
        'top': 'Top',
        'left': 'Left',
        'width': 'Width',
        'height': 'Height'
    }

    def __init__(self, signature_type=None, page_number=None, signature_id=None, is_signature=None, created_on=None, modified_on=None, top=None, left=None, width=None, height=None, **kwargs):  # noqa: E501
        """Initializes new instance of Signature"""  # noqa: E501

        self._signature_type = None
        self._page_number = None
        self._signature_id = None
        self._is_signature = None
        self._created_on = None
        self._modified_on = None
        self._top = None
        self._left = None
        self._width = None
        self._height = None

        if signature_type is not None:
            self.signature_type = signature_type
        if page_number is not None:
            self.page_number = page_number
        if signature_id is not None:
            self.signature_id = signature_id
        if is_signature is not None:
            self.is_signature = is_signature
        if created_on is not None:
            self.created_on = created_on
        if modified_on is not None:
            self.modified_on = modified_on
        if top is not None:
            self.top = top
        if left is not None:
            self.left = left
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
    
    @property
    def signature_type(self):
        """
        Gets the signature_type.  # noqa: E501

        Specifies the signature type (Text, Image, Digital, Barcode, QRCode, Stamp)  # noqa: E501

        :return: The signature_type.  # noqa: E501
        :rtype: str
        """
        return self._signature_type

    @signature_type.setter
    def signature_type(self, signature_type):
        """
        Sets the signature_type.

        Specifies the signature type (Text, Image, Digital, Barcode, QRCode, Stamp)  # noqa: E501

        :param signature_type: The signature_type.  # noqa: E501
        :type: str
        """
        if signature_type is None:
            raise ValueError("Invalid value for `signature_type`, must not be `None`")  # noqa: E501
        allowed_values = ["None", "Text", "Image", "Digital", "Barcode", "QRCode", "Stamp", "FormField", "Metadata"]  # noqa: E501
        if not signature_type.isdigit():	
            if signature_type not in allowed_values:
                raise ValueError(
                    "Invalid value for `signature_type` ({0}), must be one of {1}"  # noqa: E501
                    .format(signature_type, allowed_values))
            self._signature_type = signature_type
        else:
            self._signature_type = allowed_values[int(signature_type) if six.PY3 else long(signature_type)]
    
    @property
    def page_number(self):
        """
        Gets the page_number.  # noqa: E501

        Specifies the page signature was found on  # noqa: E501

        :return: The page_number.  # noqa: E501
        :rtype: int
        """
        return self._page_number

    @page_number.setter
    def page_number(self, page_number):
        """
        Sets the page_number.

        Specifies the page signature was found on  # noqa: E501

        :param page_number: The page_number.  # noqa: E501
        :type: int
        """
        self._page_number = page_number
    
    @property
    def signature_id(self):
        """
        Gets the signature_id.  # noqa: E501

        Unique signature identifier to modify signature in the document over Update or Delete methods. This property will be set automatically after Sign or Search method being called. If this property was saved before it can be set manually to manipulate the signature.  # noqa: E501

        :return: The signature_id.  # noqa: E501
        :rtype: str
        """
        return self._signature_id

    @signature_id.setter
    def signature_id(self, signature_id):
        """
        Sets the signature_id.

        Unique signature identifier to modify signature in the document over Update or Delete methods. This property will be set automatically after Sign or Search method being called. If this property was saved before it can be set manually to manipulate the signature.  # noqa: E501

        :param signature_id: The signature_id.  # noqa: E501
        :type: str
        """
        self._signature_id = signature_id
    
    @property
    def is_signature(self):
        """
        Gets the is_signature.  # noqa: E501

        Get or set flag to indicate if this component is Signature or document content. This property is being used with Update method to set element as signature (true) or document element (false).               # noqa: E501

        :return: The is_signature.  # noqa: E501
        :rtype: bool
        """
        return self._is_signature

    @is_signature.setter
    def is_signature(self, is_signature):
        """
        Sets the is_signature.

        Get or set flag to indicate if this component is Signature or document content. This property is being used with Update method to set element as signature (true) or document element (false).               # noqa: E501

        :param is_signature: The is_signature.  # noqa: E501
        :type: bool
        """
        if is_signature is None:
            raise ValueError("Invalid value for `is_signature`, must not be `None`")  # noqa: E501
        self._is_signature = is_signature
    
    @property
    def created_on(self):
        """
        Gets the created_on.  # noqa: E501

        Get or set the signature creation date  # noqa: E501

        :return: The created_on.  # noqa: E501
        :rtype: datetime
        """
        return self._created_on

    @created_on.setter
    def created_on(self, created_on):
        """
        Sets the created_on.

        Get or set the signature creation date  # noqa: E501

        :param created_on: The created_on.  # noqa: E501
        :type: datetime
        """
        if created_on is None:
            raise ValueError("Invalid value for `created_on`, must not be `None`")  # noqa: E501
        self._created_on = created_on
    
    @property
    def modified_on(self):
        """
        Gets the modified_on.  # noqa: E501

        Get or set the signature modification date  # noqa: E501

        :return: The modified_on.  # noqa: E501
        :rtype: datetime
        """
        return self._modified_on

    @modified_on.setter
    def modified_on(self, modified_on):
        """
        Sets the modified_on.

        Get or set the signature modification date  # noqa: E501

        :param modified_on: The modified_on.  # noqa: E501
        :type: datetime
        """
        if modified_on is None:
            raise ValueError("Invalid value for `modified_on`, must not be `None`")  # noqa: E501
        self._modified_on = modified_on
    
    @property
    def top(self):
        """
        Gets the top.  # noqa: E501

        Specifies top position of signature  # noqa: E501

        :return: The top.  # noqa: E501
        :rtype: int
        """
        return self._top

    @top.setter
    def top(self, top):
        """
        Sets the top.

        Specifies top position of signature  # noqa: E501

        :param top: The top.  # noqa: E501
        :type: int
        """
        if top is None:
            raise ValueError("Invalid value for `top`, must not be `None`")  # noqa: E501
        self._top = top
    
    @property
    def left(self):
        """
        Gets the left.  # noqa: E501

        Specifies left position of signature  # noqa: E501

        :return: The left.  # noqa: E501
        :rtype: int
        """
        return self._left

    @left.setter
    def left(self, left):
        """
        Sets the left.

        Specifies left position of signature  # noqa: E501

        :param left: The left.  # noqa: E501
        :type: int
        """
        if left is None:
            raise ValueError("Invalid value for `left`, must not be `None`")  # noqa: E501
        self._left = left
    
    @property
    def width(self):
        """
        Gets the width.  # noqa: E501

        Specifies width of signature  # noqa: E501

        :return: The width.  # noqa: E501
        :rtype: int
        """
        return self._width

    @width.setter
    def width(self, width):
        """
        Sets the width.

        Specifies width of signature  # noqa: E501

        :param width: The width.  # noqa: E501
        :type: int
        """
        if width is None:
            raise ValueError("Invalid value for `width`, must not be `None`")  # noqa: E501
        self._width = width
    
    @property
    def height(self):
        """
        Gets the height.  # noqa: E501

        Specifies height of signature  # noqa: E501

        :return: The height.  # noqa: E501
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, height):
        """
        Sets the height.

        Specifies height of signature  # noqa: E501

        :param height: The height.  # noqa: E501
        :type: int
        """
        if height is None:
            raise ValueError("Invalid value for `height`, must not be `None`")  # noqa: E501
        self._height = height

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
        if not isinstance(other, Signature):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
