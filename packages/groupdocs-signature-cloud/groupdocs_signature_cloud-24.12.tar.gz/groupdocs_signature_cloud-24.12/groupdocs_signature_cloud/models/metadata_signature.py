# coding: utf-8

# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="MetadataSignature.py">
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

class MetadataSignature(Signature):
    """
    Contains Metadata signature properties.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'type': 'str',
        'data_type': 'str',
        'value': 'str',
        'name': 'str',
        'id': 'int',
        'size': 'int',
        'description': 'str',
        'tag_prefix': 'str'
    }

    attribute_map = {
        'type': 'Type',
        'data_type': 'DataType',
        'value': 'Value',
        'name': 'Name',
        'id': 'Id',
        'size': 'Size',
        'description': 'Description',
        'tag_prefix': 'TagPrefix'
    }

    def __init__(self, type=None, data_type=None, value=None, name=None, id=None, size=None, description=None, tag_prefix=None, **kwargs):  # noqa: E501
        """Initializes new instance of MetadataSignature"""  # noqa: E501

        self._type = None
        self._data_type = None
        self._value = None
        self._name = None
        self._id = None
        self._size = None
        self._description = None
        self._tag_prefix = None

        if type is not None:
            self.type = type
        if data_type is not None:
            self.data_type = data_type
        if value is not None:
            self.value = value
        if name is not None:
            self.name = name
        if id is not None:
            self.id = id
        if size is not None:
            self.size = size
        if description is not None:
            self.description = description
        if tag_prefix is not None:
            self.tag_prefix = tag_prefix

        base = super(MetadataSignature, self)
        base.__init__(**kwargs)

        self.swagger_types.update(base.swagger_types)
        self.attribute_map.update(base.attribute_map)
    
    @property
    def type(self):
        """
        Gets the type.  # noqa: E501

        Specifies metadata type.  # noqa: E501

        :return: The type.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type.

        Specifies metadata type.  # noqa: E501

        :param type: The type.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        allowed_values = ["None", "Certificate", "Image", "Pdf", "Presentation", "Spreadsheet", "WordProcessing"]  # noqa: E501
        if not type.isdigit():	
            if type not in allowed_values:
                raise ValueError(
                    "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                    .format(type, allowed_values))
            self._type = type
        else:
            self._type = allowed_values[int(type) if six.PY3 else long(type)]
    
    @property
    def data_type(self):
        """
        Gets the data_type.  # noqa: E501

        Specifies metadata value type.  # noqa: E501

        :return: The data_type.  # noqa: E501
        :rtype: str
        """
        return self._data_type

    @data_type.setter
    def data_type(self, data_type):
        """
        Sets the data_type.

        Specifies metadata value type.  # noqa: E501

        :param data_type: The data_type.  # noqa: E501
        :type: str
        """
        if data_type is None:
            raise ValueError("Invalid value for `data_type`, must not be `None`")  # noqa: E501
        allowed_values = ["Undefined", "Boolean", "Integer", "Double", "DateTime", "String"]  # noqa: E501
        if not data_type.isdigit():	
            if data_type not in allowed_values:
                raise ValueError(
                    "Invalid value for `data_type` ({0}), must be one of {1}"  # noqa: E501
                    .format(data_type, allowed_values))
            self._data_type = data_type
        else:
            self._data_type = allowed_values[int(data_type) if six.PY3 else long(data_type)]
    
    @property
    def value(self):
        """
        Gets the value.  # noqa: E501

        Specifies metadata object value  # noqa: E501

        :return: The value.  # noqa: E501
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value.

        Specifies metadata object value  # noqa: E501

        :param value: The value.  # noqa: E501
        :type: str
        """
        self._value = value
    
    @property
    def name(self):
        """
        Gets the name.  # noqa: E501

        Specifies unique metadata name  # noqa: E501

        :return: The name.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name.

        Specifies unique metadata name  # noqa: E501

        :param name: The name.  # noqa: E501
        :type: str
        """
        self._name = name
    
    @property
    def id(self):
        """
        Gets the id.  # noqa: E501

        The identifier of Image Metadata signature. See GroupDocs.Signature.Domain.ImageMetadataSignatures class that contains standard Signature with predefined Id value.  # noqa: E501

        :return: The id.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id.

        The identifier of Image Metadata signature. See GroupDocs.Signature.Domain.ImageMetadataSignatures class that contains standard Signature with predefined Id value.  # noqa: E501

        :param id: The id.  # noqa: E501
        :type: int
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501
        self._id = id
    
    @property
    def size(self):
        """
        Gets the size.  # noqa: E501

        Size of  Image Metadata value  # noqa: E501

        :return: The size.  # noqa: E501
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """
        Sets the size.

        Size of  Image Metadata value  # noqa: E501

        :param size: The size.  # noqa: E501
        :type: int
        """
        if size is None:
            raise ValueError("Invalid value for `size`, must not be `None`")  # noqa: E501
        self._size = size
    
    @property
    def description(self):
        """
        Gets the description.  # noqa: E501

        Description for standard Image Metadata signature  # noqa: E501

        :return: The description.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description.

        Description for standard Image Metadata signature  # noqa: E501

        :param description: The description.  # noqa: E501
        :type: str
        """
        self._description = description
    
    @property
    def tag_prefix(self):
        """
        Gets the tag_prefix.  # noqa: E501

        The prefix tag of Pdf Metadata signature name. By default this property is set to \"xmp\". Possible values are  # noqa: E501

        :return: The tag_prefix.  # noqa: E501
        :rtype: str
        """
        return self._tag_prefix

    @tag_prefix.setter
    def tag_prefix(self, tag_prefix):
        """
        Sets the tag_prefix.

        The prefix tag of Pdf Metadata signature name. By default this property is set to \"xmp\". Possible values are  # noqa: E501

        :param tag_prefix: The tag_prefix.  # noqa: E501
        :type: str
        """
        self._tag_prefix = tag_prefix

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
        if not isinstance(other, MetadataSignature):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
