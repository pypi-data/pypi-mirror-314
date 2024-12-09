# coding: utf-8

# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="PdfTextAnnotationAppearance.py">
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

class PdfTextAnnotationAppearance(SignatureAppearance):
    """
    Describes appearance of PDF text annotation object (Title, Subject, Content).
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'border': 'BorderLine',
        'border_effect': 'str',
        'border_effect_intensity': 'int',
        'contents': 'str',
        'h_corner_radius': 'int',
        'subject': 'str',
        'title': 'str',
        'v_corner_radius': 'int'
    }

    attribute_map = {
        'border': 'Border',
        'border_effect': 'BorderEffect',
        'border_effect_intensity': 'BorderEffectIntensity',
        'contents': 'Contents',
        'h_corner_radius': 'HCornerRadius',
        'subject': 'Subject',
        'title': 'Title',
        'v_corner_radius': 'VCornerRadius'
    }

    def __init__(self, border=None, border_effect=None, border_effect_intensity=None, contents=None, h_corner_radius=None, subject=None, title=None, v_corner_radius=None, **kwargs):  # noqa: E501
        """Initializes new instance of PdfTextAnnotationAppearance"""  # noqa: E501

        self._border = None
        self._border_effect = None
        self._border_effect_intensity = None
        self._contents = None
        self._h_corner_radius = None
        self._subject = None
        self._title = None
        self._v_corner_radius = None

        if border is not None:
            self.border = border
        if border_effect is not None:
            self.border_effect = border_effect
        if border_effect_intensity is not None:
            self.border_effect_intensity = border_effect_intensity
        if contents is not None:
            self.contents = contents
        if h_corner_radius is not None:
            self.h_corner_radius = h_corner_radius
        if subject is not None:
            self.subject = subject
        if title is not None:
            self.title = title
        if v_corner_radius is not None:
            self.v_corner_radius = v_corner_radius

        base = super(PdfTextAnnotationAppearance, self)
        base.__init__(**kwargs)

        self.swagger_types.update(base.swagger_types)
        self.attribute_map.update(base.attribute_map)
    
    @property
    def border(self):
        """
        Gets the border.  # noqa: E501

        Represents border appearance  # noqa: E501

        :return: The border.  # noqa: E501
        :rtype: BorderLine
        """
        return self._border

    @border.setter
    def border(self, border):
        """
        Sets the border.

        Represents border appearance  # noqa: E501

        :param border: The border.  # noqa: E501
        :type: BorderLine
        """
        self._border = border
    
    @property
    def border_effect(self):
        """
        Gets the border_effect.  # noqa: E501

        Gets or sets border effect.  # noqa: E501

        :return: The border_effect.  # noqa: E501
        :rtype: str
        """
        return self._border_effect

    @border_effect.setter
    def border_effect(self, border_effect):
        """
        Sets the border_effect.

        Gets or sets border effect.  # noqa: E501

        :param border_effect: The border_effect.  # noqa: E501
        :type: str
        """
        if border_effect is None:
            raise ValueError("Invalid value for `border_effect`, must not be `None`")  # noqa: E501
        allowed_values = ["None", "Cloudy"]  # noqa: E501
        if not border_effect.isdigit():	
            if border_effect not in allowed_values:
                raise ValueError(
                    "Invalid value for `border_effect` ({0}), must be one of {1}"  # noqa: E501
                    .format(border_effect, allowed_values))
            self._border_effect = border_effect
        else:
            self._border_effect = allowed_values[int(border_effect) if six.PY3 else long(border_effect)]
    
    @property
    def border_effect_intensity(self):
        """
        Gets the border_effect_intensity.  # noqa: E501

        Gets or sets border effect intensity. Valid range of value is [0..2].  # noqa: E501

        :return: The border_effect_intensity.  # noqa: E501
        :rtype: int
        """
        return self._border_effect_intensity

    @border_effect_intensity.setter
    def border_effect_intensity(self, border_effect_intensity):
        """
        Sets the border_effect_intensity.

        Gets or sets border effect intensity. Valid range of value is [0..2].  # noqa: E501

        :param border_effect_intensity: The border_effect_intensity.  # noqa: E501
        :type: int
        """
        if border_effect_intensity is None:
            raise ValueError("Invalid value for `border_effect_intensity`, must not be `None`")  # noqa: E501
        self._border_effect_intensity = border_effect_intensity
    
    @property
    def contents(self):
        """
        Gets the contents.  # noqa: E501

        Gets or sets content of annotation object.  # noqa: E501

        :return: The contents.  # noqa: E501
        :rtype: str
        """
        return self._contents

    @contents.setter
    def contents(self, contents):
        """
        Sets the contents.

        Gets or sets content of annotation object.  # noqa: E501

        :param contents: The contents.  # noqa: E501
        :type: str
        """
        self._contents = contents
    
    @property
    def h_corner_radius(self):
        """
        Gets the h_corner_radius.  # noqa: E501

        Gets or sets horizontal corner radius.  # noqa: E501

        :return: The h_corner_radius.  # noqa: E501
        :rtype: int
        """
        return self._h_corner_radius

    @h_corner_radius.setter
    def h_corner_radius(self, h_corner_radius):
        """
        Sets the h_corner_radius.

        Gets or sets horizontal corner radius.  # noqa: E501

        :param h_corner_radius: The h_corner_radius.  # noqa: E501
        :type: int
        """
        if h_corner_radius is None:
            raise ValueError("Invalid value for `h_corner_radius`, must not be `None`")  # noqa: E501
        self._h_corner_radius = h_corner_radius
    
    @property
    def subject(self):
        """
        Gets the subject.  # noqa: E501

        Gets or sets Subject representing description of the object.  # noqa: E501

        :return: The subject.  # noqa: E501
        :rtype: str
        """
        return self._subject

    @subject.setter
    def subject(self, subject):
        """
        Sets the subject.

        Gets or sets Subject representing description of the object.  # noqa: E501

        :param subject: The subject.  # noqa: E501
        :type: str
        """
        self._subject = subject
    
    @property
    def title(self):
        """
        Gets the title.  # noqa: E501

        Gets or sets a Title that will be displayed in title bar of annotation object.  # noqa: E501

        :return: The title.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """
        Sets the title.

        Gets or sets a Title that will be displayed in title bar of annotation object.  # noqa: E501

        :param title: The title.  # noqa: E501
        :type: str
        """
        self._title = title
    
    @property
    def v_corner_radius(self):
        """
        Gets the v_corner_radius.  # noqa: E501

        Gets or sets vertical corner radius.  # noqa: E501

        :return: The v_corner_radius.  # noqa: E501
        :rtype: int
        """
        return self._v_corner_radius

    @v_corner_radius.setter
    def v_corner_radius(self, v_corner_radius):
        """
        Sets the v_corner_radius.

        Gets or sets vertical corner radius.  # noqa: E501

        :param v_corner_radius: The v_corner_radius.  # noqa: E501
        :type: int
        """
        if v_corner_radius is None:
            raise ValueError("Invalid value for `v_corner_radius`, must not be `None`")  # noqa: E501
        self._v_corner_radius = v_corner_radius

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
        if not isinstance(other, PdfTextAnnotationAppearance):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
