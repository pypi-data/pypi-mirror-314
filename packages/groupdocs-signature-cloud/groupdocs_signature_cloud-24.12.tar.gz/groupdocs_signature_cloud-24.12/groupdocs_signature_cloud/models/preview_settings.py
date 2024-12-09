# coding: utf-8

# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="PreviewSettings.py">
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

from groupdocs_signature_cloud.models import BaseSettings

class PreviewSettings(BaseSettings):
    """
    Defines preview request settings
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'width': 'int',
        'height': 'int',
        'resolution': 'int',
        'page_numbers': 'list[int]',
        'preview_format': 'str',
        'hide_signatures': 'bool',
        'output_path': 'str'
    }

    attribute_map = {
        'width': 'Width',
        'height': 'Height',
        'resolution': 'Resolution',
        'page_numbers': 'PageNumbers',
        'preview_format': 'PreviewFormat',
        'hide_signatures': 'HideSignatures',
        'output_path': 'OutputPath'
    }

    def __init__(self, width=None, height=None, resolution=None, page_numbers=None, preview_format=None, hide_signatures=None, output_path=None, **kwargs):  # noqa: E501
        """Initializes new instance of PreviewSettings"""  # noqa: E501

        self._width = None
        self._height = None
        self._resolution = None
        self._page_numbers = None
        self._preview_format = None
        self._hide_signatures = None
        self._output_path = None

        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if resolution is not None:
            self.resolution = resolution
        if page_numbers is not None:
            self.page_numbers = page_numbers
        if preview_format is not None:
            self.preview_format = preview_format
        if hide_signatures is not None:
            self.hide_signatures = hide_signatures
        if output_path is not None:
            self.output_path = output_path

        base = super(PreviewSettings, self)
        base.__init__(**kwargs)

        self.swagger_types.update(base.swagger_types)
        self.attribute_map.update(base.attribute_map)
    
    @property
    def width(self):
        """
        Gets the width.  # noqa: E501

        Preview images width  # noqa: E501

        :return: The width.  # noqa: E501
        :rtype: int
        """
        return self._width

    @width.setter
    def width(self, width):
        """
        Sets the width.

        Preview images width  # noqa: E501

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

        Preview images height  # noqa: E501

        :return: The height.  # noqa: E501
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, height):
        """
        Sets the height.

        Preview images height  # noqa: E501

        :param height: The height.  # noqa: E501
        :type: int
        """
        if height is None:
            raise ValueError("Invalid value for `height`, must not be `None`")  # noqa: E501
        self._height = height
    
    @property
    def resolution(self):
        """
        Gets the resolution.  # noqa: E501

        Gets or sets the resolution of the preview images in DPI (dots per inch).  # noqa: E501

        :return: The resolution.  # noqa: E501
        :rtype: int
        """
        return self._resolution

    @resolution.setter
    def resolution(self, resolution):
        """
        Sets the resolution.

        Gets or sets the resolution of the preview images in DPI (dots per inch).  # noqa: E501

        :param resolution: The resolution.  # noqa: E501
        :type: int
        """
        if resolution is None:
            raise ValueError("Invalid value for `resolution`, must not be `None`")  # noqa: E501
        self._resolution = resolution
    
    @property
    def page_numbers(self):
        """
        Gets the page_numbers.  # noqa: E501

        Preview page numbers  # noqa: E501

        :return: The page_numbers.  # noqa: E501
        :rtype: list[int]
        """
        return self._page_numbers

    @page_numbers.setter
    def page_numbers(self, page_numbers):
        """
        Sets the page_numbers.

        Preview page numbers  # noqa: E501

        :param page_numbers: The page_numbers.  # noqa: E501
        :type: list[int]
        """
        self._page_numbers = page_numbers
    
    @property
    def preview_format(self):
        """
        Gets the preview_format.  # noqa: E501

        Preview format  # noqa: E501

        :return: The preview_format.  # noqa: E501
        :rtype: str
        """
        return self._preview_format

    @preview_format.setter
    def preview_format(self, preview_format):
        """
        Sets the preview_format.

        Preview format  # noqa: E501

        :param preview_format: The preview_format.  # noqa: E501
        :type: str
        """
        if preview_format is None:
            raise ValueError("Invalid value for `preview_format`, must not be `None`")  # noqa: E501
        allowed_values = ["PNG", "JPEG", "BMP"]  # noqa: E501
        if not preview_format.isdigit():	
            if preview_format not in allowed_values:
                raise ValueError(
                    "Invalid value for `preview_format` ({0}), must be one of {1}"  # noqa: E501
                    .format(preview_format, allowed_values))
            self._preview_format = preview_format
        else:
            self._preview_format = allowed_values[int(preview_format) if six.PY3 else long(preview_format)]
    
    @property
    def hide_signatures(self):
        """
        Gets the hide_signatures.  # noqa: E501

        Flag to hide signatures from page preview image. Only signatures are marked as IsSignature will be hidden from generated document page image  # noqa: E501

        :return: The hide_signatures.  # noqa: E501
        :rtype: bool
        """
        return self._hide_signatures

    @hide_signatures.setter
    def hide_signatures(self, hide_signatures):
        """
        Sets the hide_signatures.

        Flag to hide signatures from page preview image. Only signatures are marked as IsSignature will be hidden from generated document page image  # noqa: E501

        :param hide_signatures: The hide_signatures.  # noqa: E501
        :type: bool
        """
        if hide_signatures is None:
            raise ValueError("Invalid value for `hide_signatures`, must not be `None`")  # noqa: E501
        self._hide_signatures = hide_signatures
    
    @property
    def output_path(self):
        """
        Gets the output_path.  # noqa: E501

        Set path for output pages. If not set then default path used.  # noqa: E501

        :return: The output_path.  # noqa: E501
        :rtype: str
        """
        return self._output_path

    @output_path.setter
    def output_path(self, output_path):
        """
        Sets the output_path.

        Set path for output pages. If not set then default path used.  # noqa: E501

        :param output_path: The output_path.  # noqa: E501
        :type: str
        """
        self._output_path = output_path

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
        if not isinstance(other, PreviewSettings):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
