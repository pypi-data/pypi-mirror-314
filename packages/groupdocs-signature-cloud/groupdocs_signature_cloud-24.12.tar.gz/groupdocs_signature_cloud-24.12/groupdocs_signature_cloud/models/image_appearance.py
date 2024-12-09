# coding: utf-8

# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="ImageAppearance.py">
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

class ImageAppearance(SignatureAppearance):
    """
    Describes extended appearance features for Image Signature.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'brightness': 'float',
        'contrast': 'float',
        'gamma_correction': 'float',
        'grayscale': 'bool'
    }

    attribute_map = {
        'brightness': 'Brightness',
        'contrast': 'Contrast',
        'gamma_correction': 'GammaCorrection',
        'grayscale': 'Grayscale'
    }

    def __init__(self, brightness=None, contrast=None, gamma_correction=None, grayscale=None, **kwargs):  # noqa: E501
        """Initializes new instance of ImageAppearance"""  # noqa: E501

        self._brightness = None
        self._contrast = None
        self._gamma_correction = None
        self._grayscale = None

        if brightness is not None:
            self.brightness = brightness
        if contrast is not None:
            self.contrast = contrast
        if gamma_correction is not None:
            self.gamma_correction = gamma_correction
        if grayscale is not None:
            self.grayscale = grayscale

        base = super(ImageAppearance, self)
        base.__init__(**kwargs)

        self.swagger_types.update(base.swagger_types)
        self.attribute_map.update(base.attribute_map)
    
    @property
    def brightness(self):
        """
        Gets the brightness.  # noqa: E501

        Gets or sets image brightness. Default value is 1 it corresponds to original brightness of image.  # noqa: E501

        :return: The brightness.  # noqa: E501
        :rtype: float
        """
        return self._brightness

    @brightness.setter
    def brightness(self, brightness):
        """
        Sets the brightness.

        Gets or sets image brightness. Default value is 1 it corresponds to original brightness of image.  # noqa: E501

        :param brightness: The brightness.  # noqa: E501
        :type: float
        """
        if brightness is None:
            raise ValueError("Invalid value for `brightness`, must not be `None`")  # noqa: E501
        self._brightness = brightness
    
    @property
    def contrast(self):
        """
        Gets the contrast.  # noqa: E501

        Gets or sets image contrast. Default value is 1 it corresponds to original contrast of image.  # noqa: E501

        :return: The contrast.  # noqa: E501
        :rtype: float
        """
        return self._contrast

    @contrast.setter
    def contrast(self, contrast):
        """
        Sets the contrast.

        Gets or sets image contrast. Default value is 1 it corresponds to original contrast of image.  # noqa: E501

        :param contrast: The contrast.  # noqa: E501
        :type: float
        """
        if contrast is None:
            raise ValueError("Invalid value for `contrast`, must not be `None`")  # noqa: E501
        self._contrast = contrast
    
    @property
    def gamma_correction(self):
        """
        Gets the gamma_correction.  # noqa: E501

        Gets or sets image gamma. Default value is 1 it corresponds to original gamma of image.  # noqa: E501

        :return: The gamma_correction.  # noqa: E501
        :rtype: float
        """
        return self._gamma_correction

    @gamma_correction.setter
    def gamma_correction(self, gamma_correction):
        """
        Sets the gamma_correction.

        Gets or sets image gamma. Default value is 1 it corresponds to original gamma of image.  # noqa: E501

        :param gamma_correction: The gamma_correction.  # noqa: E501
        :type: float
        """
        if gamma_correction is None:
            raise ValueError("Invalid value for `gamma_correction`, must not be `None`")  # noqa: E501
        self._gamma_correction = gamma_correction
    
    @property
    def grayscale(self):
        """
        Gets the grayscale.  # noqa: E501

        Setup this flag to true if gray-scale filter is required.  # noqa: E501

        :return: The grayscale.  # noqa: E501
        :rtype: bool
        """
        return self._grayscale

    @grayscale.setter
    def grayscale(self, grayscale):
        """
        Sets the grayscale.

        Setup this flag to true if gray-scale filter is required.  # noqa: E501

        :param grayscale: The grayscale.  # noqa: E501
        :type: bool
        """
        if grayscale is None:
            raise ValueError("Invalid value for `grayscale`, must not be `None`")  # noqa: E501
        self._grayscale = grayscale

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
        if not isinstance(other, ImageAppearance):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
