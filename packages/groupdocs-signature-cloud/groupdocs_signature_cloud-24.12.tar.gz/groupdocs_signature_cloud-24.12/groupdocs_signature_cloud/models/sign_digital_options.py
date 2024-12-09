# coding: utf-8

# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="SignDigitalOptions.py">
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

from groupdocs_signature_cloud.models import SignImageOptions

class SignDigitalOptions(SignImageOptions):
    """
    Represents the Digital sign options
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'reason': 'str',
        'contact': 'str',
        'location': 'str',
        'visible': 'bool',
        'password': 'str',
        'certificate_file_path': 'str',
        'x_ad_es_type': 'str',
        'digital_vba': 'DigitalVBA',
        'sign_time': 'datetime',
        'comments': 'str'
    }

    attribute_map = {
        'reason': 'Reason',
        'contact': 'Contact',
        'location': 'Location',
        'visible': 'Visible',
        'password': 'Password',
        'certificate_file_path': 'CertificateFilePath',
        'x_ad_es_type': 'XAdESType',
        'digital_vba': 'DigitalVBA',
        'sign_time': 'SignTime',
        'comments': 'Comments'
    }

    def __init__(self, reason=None, contact=None, location=None, visible=None, password=None, certificate_file_path=None, x_ad_es_type=None, digital_vba=None, sign_time=None, comments=None, **kwargs):  # noqa: E501
        """Initializes new instance of SignDigitalOptions"""  # noqa: E501

        self._reason = None
        self._contact = None
        self._location = None
        self._visible = None
        self._password = None
        self._certificate_file_path = None
        self._x_ad_es_type = None
        self._digital_vba = None
        self._sign_time = None
        self._comments = None

        if reason is not None:
            self.reason = reason
        if contact is not None:
            self.contact = contact
        if location is not None:
            self.location = location
        if visible is not None:
            self.visible = visible
        if password is not None:
            self.password = password
        if certificate_file_path is not None:
            self.certificate_file_path = certificate_file_path
        if x_ad_es_type is not None:
            self.x_ad_es_type = x_ad_es_type
        if digital_vba is not None:
            self.digital_vba = digital_vba
        if sign_time is not None:
            self.sign_time = sign_time
        if comments is not None:
            self.comments = comments

        base = super(SignDigitalOptions, self)
        base.__init__(**kwargs)

        self.swagger_types.update(base.swagger_types)
        self.attribute_map.update(base.attribute_map)
    
    @property
    def reason(self):
        """
        Gets the reason.  # noqa: E501

        Gets or sets the reason of signature.  # noqa: E501

        :return: The reason.  # noqa: E501
        :rtype: str
        """
        return self._reason

    @reason.setter
    def reason(self, reason):
        """
        Sets the reason.

        Gets or sets the reason of signature.  # noqa: E501

        :param reason: The reason.  # noqa: E501
        :type: str
        """
        self._reason = reason
    
    @property
    def contact(self):
        """
        Gets the contact.  # noqa: E501

        Gets or sets the signature contact.  # noqa: E501

        :return: The contact.  # noqa: E501
        :rtype: str
        """
        return self._contact

    @contact.setter
    def contact(self, contact):
        """
        Sets the contact.

        Gets or sets the signature contact.  # noqa: E501

        :param contact: The contact.  # noqa: E501
        :type: str
        """
        self._contact = contact
    
    @property
    def location(self):
        """
        Gets the location.  # noqa: E501

        Gets or sets the signature location.  # noqa: E501

        :return: The location.  # noqa: E501
        :rtype: str
        """
        return self._location

    @location.setter
    def location(self, location):
        """
        Sets the location.

        Gets or sets the signature location.  # noqa: E501

        :param location: The location.  # noqa: E501
        :type: str
        """
        self._location = location
    
    @property
    def visible(self):
        """
        Gets the visible.  # noqa: E501

        Gets or sets the visibility of signature.  # noqa: E501

        :return: The visible.  # noqa: E501
        :rtype: bool
        """
        return self._visible

    @visible.setter
    def visible(self, visible):
        """
        Sets the visible.

        Gets or sets the visibility of signature.  # noqa: E501

        :param visible: The visible.  # noqa: E501
        :type: bool
        """
        if visible is None:
            raise ValueError("Invalid value for `visible`, must not be `None`")  # noqa: E501
        self._visible = visible
    
    @property
    def password(self):
        """
        Gets the password.  # noqa: E501

        Gets or sets the password of digital certificate  # noqa: E501

        :return: The password.  # noqa: E501
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """
        Sets the password.

        Gets or sets the password of digital certificate  # noqa: E501

        :param password: The password.  # noqa: E501
        :type: str
        """
        self._password = password
    
    @property
    def certificate_file_path(self):
        """
        Gets the certificate_file_path.  # noqa: E501

        Gets or sets the digital certificate file GUID  # noqa: E501

        :return: The certificate_file_path.  # noqa: E501
        :rtype: str
        """
        return self._certificate_file_path

    @certificate_file_path.setter
    def certificate_file_path(self, certificate_file_path):
        """
        Sets the certificate_file_path.

        Gets or sets the digital certificate file GUID  # noqa: E501

        :param certificate_file_path: The certificate_file_path.  # noqa: E501
        :type: str
        """
        self._certificate_file_path = certificate_file_path
    
    @property
    def x_ad_es_type(self):
        """
        Gets the x_ad_es_type.  # noqa: E501

        XAdES type GroupDocs.Signature.Options.DigitalSignOptions.XAdESType. Default value is None (XAdES is off). At this moment XAdES signature type is supported only for Spreadsheet documents.               # noqa: E501

        :return: The x_ad_es_type.  # noqa: E501
        :rtype: str
        """
        return self._x_ad_es_type

    @x_ad_es_type.setter
    def x_ad_es_type(self, x_ad_es_type):
        """
        Sets the x_ad_es_type.

        XAdES type GroupDocs.Signature.Options.DigitalSignOptions.XAdESType. Default value is None (XAdES is off). At this moment XAdES signature type is supported only for Spreadsheet documents.               # noqa: E501

        :param x_ad_es_type: The x_ad_es_type.  # noqa: E501
        :type: str
        """
        if x_ad_es_type is None:
            raise ValueError("Invalid value for `x_ad_es_type`, must not be `None`")  # noqa: E501
        allowed_values = ["None", "XAdES"]  # noqa: E501
        if not x_ad_es_type.isdigit():	
            if x_ad_es_type not in allowed_values:
                raise ValueError(
                    "Invalid value for `x_ad_es_type` ({0}), must be one of {1}"  # noqa: E501
                    .format(x_ad_es_type, allowed_values))
            self._x_ad_es_type = x_ad_es_type
        else:
            self._x_ad_es_type = allowed_values[int(x_ad_es_type) if six.PY3 else long(x_ad_es_type)]
    
    @property
    def digital_vba(self):
        """
        Gets the digital_vba.  # noqa: E501

        Options for signing VBA project  # noqa: E501

        :return: The digital_vba.  # noqa: E501
        :rtype: DigitalVBA
        """
        return self._digital_vba

    @digital_vba.setter
    def digital_vba(self, digital_vba):
        """
        Sets the digital_vba.

        Options for signing VBA project  # noqa: E501

        :param digital_vba: The digital_vba.  # noqa: E501
        :type: DigitalVBA
        """
        self._digital_vba = digital_vba
    
    @property
    def sign_time(self):
        """
        Gets the sign_time.  # noqa: E501

        The time the document was signed.  # noqa: E501

        :return: The sign_time.  # noqa: E501
        :rtype: datetime
        """
        return self._sign_time

    @sign_time.setter
    def sign_time(self, sign_time):
        """
        Sets the sign_time.

        The time the document was signed.  # noqa: E501

        :param sign_time: The sign_time.  # noqa: E501
        :type: datetime
        """
        self._sign_time = sign_time
    
    @property
    def comments(self):
        """
        Gets the comments.  # noqa: E501

        The signing purpose comment.  # noqa: E501

        :return: The comments.  # noqa: E501
        :rtype: str
        """
        return self._comments

    @comments.setter
    def comments(self, comments):
        """
        Sets the comments.

        The signing purpose comment.  # noqa: E501

        :param comments: The comments.  # noqa: E501
        :type: str
        """
        self._comments = comments

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
        if not isinstance(other, SignDigitalOptions):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
