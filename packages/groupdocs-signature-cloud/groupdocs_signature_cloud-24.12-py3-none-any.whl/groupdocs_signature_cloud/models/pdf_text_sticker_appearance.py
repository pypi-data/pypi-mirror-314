# coding: utf-8

# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="PdfTextStickerAppearance.py">
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

from groupdocs_signature_cloud.models import SignatureAppearance

class PdfTextStickerAppearance(SignatureAppearance):
    """
    Describes appearance of PDF text annotation sticker object and pop-up window of sticker.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'contents': 'str',
        'icon': 'str',
        'opened': 'bool',
        'subject': 'str',
        'title': 'str'
    }

    attribute_map = {
        'contents': 'Contents',
        'icon': 'Icon',
        'opened': 'Opened',
        'subject': 'Subject',
        'title': 'Title'
    }

    def __init__(self, contents=None, icon=None, opened=None, subject=None, title=None, **kwargs):  # noqa: E501
        """Initializes new instance of PdfTextStickerAppearance"""  # noqa: E501

        self._contents = None
        self._icon = None
        self._opened = None
        self._subject = None
        self._title = None

        if contents is not None:
            self.contents = contents
        if icon is not None:
            self.icon = icon
        if opened is not None:
            self.opened = opened
        if subject is not None:
            self.subject = subject
        if title is not None:
            self.title = title

        base = super(PdfTextStickerAppearance, self)
        base.__init__(**kwargs)

        self.swagger_types.update(base.swagger_types)
        self.attribute_map.update(base.attribute_map)
    
    @property
    def contents(self):
        """
        Gets the contents.  # noqa: E501

        Gets or sets the contents of pop-up window.  # noqa: E501

        :return: The contents.  # noqa: E501
        :rtype: str
        """
        return self._contents

    @contents.setter
    def contents(self, contents):
        """
        Sets the contents.

        Gets or sets the contents of pop-up window.  # noqa: E501

        :param contents: The contents.  # noqa: E501
        :type: str
        """
        self._contents = contents
    
    @property
    def icon(self):
        """
        Gets the icon.  # noqa: E501

        Gets or sets the icon of sticker.  # noqa: E501

        :return: The icon.  # noqa: E501
        :rtype: str
        """
        return self._icon

    @icon.setter
    def icon(self, icon):
        """
        Sets the icon.

        Gets or sets the icon of sticker.  # noqa: E501

        :param icon: The icon.  # noqa: E501
        :type: str
        """
        if icon is None:
            raise ValueError("Invalid value for `icon`, must not be `None`")  # noqa: E501
        allowed_values = ["Note", "Comment", "Key", "Help", "NewParagraph", "Paragraph", "Insert", "Check", "Cross", "Circle", "Star"]  # noqa: E501
        if not icon.isdigit():	
            if icon not in allowed_values:
                raise ValueError(
                    "Invalid value for `icon` ({0}), must be one of {1}"  # noqa: E501
                    .format(icon, allowed_values))
            self._icon = icon
        else:
            self._icon = allowed_values[int(icon) if six.PY3 else long(icon)]
    
    @property
    def opened(self):
        """
        Gets the opened.  # noqa: E501

        Setup if sticker pop-up window will be opened by default.  # noqa: E501

        :return: The opened.  # noqa: E501
        :rtype: bool
        """
        return self._opened

    @opened.setter
    def opened(self, opened):
        """
        Sets the opened.

        Setup if sticker pop-up window will be opened by default.  # noqa: E501

        :param opened: The opened.  # noqa: E501
        :type: bool
        """
        if opened is None:
            raise ValueError("Invalid value for `opened`, must not be `None`")  # noqa: E501
        self._opened = opened
    
    @property
    def subject(self):
        """
        Gets the subject.  # noqa: E501

        Gets or sets subject.  # noqa: E501

        :return: The subject.  # noqa: E501
        :rtype: str
        """
        return self._subject

    @subject.setter
    def subject(self, subject):
        """
        Sets the subject.

        Gets or sets subject.  # noqa: E501

        :param subject: The subject.  # noqa: E501
        :type: str
        """
        self._subject = subject
    
    @property
    def title(self):
        """
        Gets the title.  # noqa: E501

        Gets or sets title of pop-up window.  # noqa: E501

        :return: The title.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """
        Sets the title.

        Gets or sets title of pop-up window.  # noqa: E501

        :param title: The title.  # noqa: E501
        :type: str
        """
        self._title = title

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
        if not isinstance(other, PdfTextStickerAppearance):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
