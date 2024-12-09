# coding: utf-8

# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="PdfDigitalSignatureAppearance.py">
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

class PdfDigitalSignatureAppearance(SignatureAppearance):
    """
    Describes appearance of Digital Signature are on PDF documents.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'background': 'Color',
        'foreground': 'Color',
        'contact_info_label': 'str',
        'date_signed_at_label': 'str',
        'digital_signed_label': 'str',
        'font_family_name': 'str',
        'font_size': 'float',
        'location_label': 'str',
        'reason_label': 'str'
    }

    attribute_map = {
        'background': 'Background',
        'foreground': 'Foreground',
        'contact_info_label': 'ContactInfoLabel',
        'date_signed_at_label': 'DateSignedAtLabel',
        'digital_signed_label': 'DigitalSignedLabel',
        'font_family_name': 'FontFamilyName',
        'font_size': 'FontSize',
        'location_label': 'LocationLabel',
        'reason_label': 'ReasonLabel'
    }

    def __init__(self, background=None, foreground=None, contact_info_label=None, date_signed_at_label=None, digital_signed_label=None, font_family_name=None, font_size=None, location_label=None, reason_label=None, **kwargs):  # noqa: E501
        """Initializes new instance of PdfDigitalSignatureAppearance"""  # noqa: E501

        self._background = None
        self._foreground = None
        self._contact_info_label = None
        self._date_signed_at_label = None
        self._digital_signed_label = None
        self._font_family_name = None
        self._font_size = None
        self._location_label = None
        self._reason_label = None

        if background is not None:
            self.background = background
        if foreground is not None:
            self.foreground = foreground
        if contact_info_label is not None:
            self.contact_info_label = contact_info_label
        if date_signed_at_label is not None:
            self.date_signed_at_label = date_signed_at_label
        if digital_signed_label is not None:
            self.digital_signed_label = digital_signed_label
        if font_family_name is not None:
            self.font_family_name = font_family_name
        if font_size is not None:
            self.font_size = font_size
        if location_label is not None:
            self.location_label = location_label
        if reason_label is not None:
            self.reason_label = reason_label

        base = super(PdfDigitalSignatureAppearance, self)
        base.__init__(**kwargs)

        self.swagger_types.update(base.swagger_types)
        self.attribute_map.update(base.attribute_map)
    
    @property
    def background(self):
        """
        Gets the background.  # noqa: E501

        Get or set background color of signature appearance.   # noqa: E501

        :return: The background.  # noqa: E501
        :rtype: Color
        """
        return self._background

    @background.setter
    def background(self, background):
        """
        Sets the background.

        Get or set background color of signature appearance.   # noqa: E501

        :param background: The background.  # noqa: E501
        :type: Color
        """
        self._background = background
    
    @property
    def foreground(self):
        """
        Gets the foreground.  # noqa: E501

        Get or set foreground text color of signature appearance. By default the value is Color.FromArgb(76, 100, 255)  # noqa: E501

        :return: The foreground.  # noqa: E501
        :rtype: Color
        """
        return self._foreground

    @foreground.setter
    def foreground(self, foreground):
        """
        Sets the foreground.

        Get or set foreground text color of signature appearance. By default the value is Color.FromArgb(76, 100, 255)  # noqa: E501

        :param foreground: The foreground.  # noqa: E501
        :type: Color
        """
        self._foreground = foreground
    
    @property
    def contact_info_label(self):
        """
        Gets the contact_info_label.  # noqa: E501

        Gets or sets contact info label. Default value: \"Contact\". if this value is empty then no contact label will appear on digital signature area.               # noqa: E501

        :return: The contact_info_label.  # noqa: E501
        :rtype: str
        """
        return self._contact_info_label

    @contact_info_label.setter
    def contact_info_label(self, contact_info_label):
        """
        Sets the contact_info_label.

        Gets or sets contact info label. Default value: \"Contact\". if this value is empty then no contact label will appear on digital signature area.               # noqa: E501

        :param contact_info_label: The contact_info_label.  # noqa: E501
        :type: str
        """
        self._contact_info_label = contact_info_label
    
    @property
    def date_signed_at_label(self):
        """
        Gets the date_signed_at_label.  # noqa: E501

        Gets or sets date signed label. Default value: \"Date\".  # noqa: E501

        :return: The date_signed_at_label.  # noqa: E501
        :rtype: str
        """
        return self._date_signed_at_label

    @date_signed_at_label.setter
    def date_signed_at_label(self, date_signed_at_label):
        """
        Sets the date_signed_at_label.

        Gets or sets date signed label. Default value: \"Date\".  # noqa: E501

        :param date_signed_at_label: The date_signed_at_label.  # noqa: E501
        :type: str
        """
        self._date_signed_at_label = date_signed_at_label
    
    @property
    def digital_signed_label(self):
        """
        Gets the digital_signed_label.  # noqa: E501

        Gets or sets digital signed label. Default value: \"Digitally signed by\".  # noqa: E501

        :return: The digital_signed_label.  # noqa: E501
        :rtype: str
        """
        return self._digital_signed_label

    @digital_signed_label.setter
    def digital_signed_label(self, digital_signed_label):
        """
        Sets the digital_signed_label.

        Gets or sets digital signed label. Default value: \"Digitally signed by\".  # noqa: E501

        :param digital_signed_label: The digital_signed_label.  # noqa: E501
        :type: str
        """
        self._digital_signed_label = digital_signed_label
    
    @property
    def font_family_name(self):
        """
        Gets the font_family_name.  # noqa: E501

        Gets or sets the Font family name to display the labels. Default value is \"Arial\".  # noqa: E501

        :return: The font_family_name.  # noqa: E501
        :rtype: str
        """
        return self._font_family_name

    @font_family_name.setter
    def font_family_name(self, font_family_name):
        """
        Sets the font_family_name.

        Gets or sets the Font family name to display the labels. Default value is \"Arial\".  # noqa: E501

        :param font_family_name: The font_family_name.  # noqa: E501
        :type: str
        """
        self._font_family_name = font_family_name
    
    @property
    def font_size(self):
        """
        Gets the font_size.  # noqa: E501

        Gets or sets the Font size to display the labels. Default value is 10.  # noqa: E501

        :return: The font_size.  # noqa: E501
        :rtype: float
        """
        return self._font_size

    @font_size.setter
    def font_size(self, font_size):
        """
        Sets the font_size.

        Gets or sets the Font size to display the labels. Default value is 10.  # noqa: E501

        :param font_size: The font_size.  # noqa: E501
        :type: float
        """
        self._font_size = font_size
    
    @property
    def location_label(self):
        """
        Gets the location_label.  # noqa: E501

        Gets or sets location label. Default value: \"Location\". if this value is empty then no location label will appear on digital signature area.  # noqa: E501

        :return: The location_label.  # noqa: E501
        :rtype: str
        """
        return self._location_label

    @location_label.setter
    def location_label(self, location_label):
        """
        Sets the location_label.

        Gets or sets location label. Default value: \"Location\". if this value is empty then no location label will appear on digital signature area.  # noqa: E501

        :param location_label: The location_label.  # noqa: E501
        :type: str
        """
        self._location_label = location_label
    
    @property
    def reason_label(self):
        """
        Gets the reason_label.  # noqa: E501

        Gets or sets reason label. Default value: \"Reason\". if this value is empty then no reason label will appear on digital signature area.  # noqa: E501

        :return: The reason_label.  # noqa: E501
        :rtype: str
        """
        return self._reason_label

    @reason_label.setter
    def reason_label(self, reason_label):
        """
        Sets the reason_label.

        Gets or sets reason label. Default value: \"Reason\". if this value is empty then no reason label will appear on digital signature area.  # noqa: E501

        :param reason_label: The reason_label.  # noqa: E501
        :type: str
        """
        self._reason_label = reason_label

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
        if not isinstance(other, PdfDigitalSignatureAppearance):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
