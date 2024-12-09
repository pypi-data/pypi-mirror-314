# coding: utf-8

# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd" file="DigitalVBA.py">
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

class DigitalVBA(object):
    """
    
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'password': 'str',
        'certificate_file_path': 'str',
        'sign_only_vba_project': 'bool',
        'comments': 'str'
    }

    attribute_map = {
        'password': 'Password',
        'certificate_file_path': 'CertificateFilePath',
        'sign_only_vba_project': 'SignOnlyVBAProject',
        'comments': 'Comments'
    }

    def __init__(self, password=None, certificate_file_path=None, sign_only_vba_project=None, comments=None, **kwargs):  # noqa: E501
        """Initializes new instance of DigitalVBA"""  # noqa: E501

        self._password = None
        self._certificate_file_path = None
        self._sign_only_vba_project = None
        self._comments = None

        if password is not None:
            self.password = password
        if certificate_file_path is not None:
            self.certificate_file_path = certificate_file_path
        if sign_only_vba_project is not None:
            self.sign_only_vba_project = sign_only_vba_project
        if comments is not None:
            self.comments = comments
    
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

        Gets or sets the digital certificate file path  # noqa: E501

        :return: The certificate_file_path.  # noqa: E501
        :rtype: str
        """
        return self._certificate_file_path

    @certificate_file_path.setter
    def certificate_file_path(self, certificate_file_path):
        """
        Sets the certificate_file_path.

        Gets or sets the digital certificate file path  # noqa: E501

        :param certificate_file_path: The certificate_file_path.  # noqa: E501
        :type: str
        """
        self._certificate_file_path = certificate_file_path
    
    @property
    def sign_only_vba_project(self):
        """
        Gets the sign_only_vba_project.  # noqa: E501

        Gets or sets setting of only VBA project signing. If set to true, the SpreadSheet document will not be signed, but the VBA project will be signed.               # noqa: E501

        :return: The sign_only_vba_project.  # noqa: E501
        :rtype: bool
        """
        return self._sign_only_vba_project

    @sign_only_vba_project.setter
    def sign_only_vba_project(self, sign_only_vba_project):
        """
        Sets the sign_only_vba_project.

        Gets or sets setting of only VBA project signing. If set to true, the SpreadSheet document will not be signed, but the VBA project will be signed.               # noqa: E501

        :param sign_only_vba_project: The sign_only_vba_project.  # noqa: E501
        :type: bool
        """
        if sign_only_vba_project is None:
            raise ValueError("Invalid value for `sign_only_vba_project`, must not be `None`")  # noqa: E501
        self._sign_only_vba_project = sign_only_vba_project
    
    @property
    def comments(self):
        """
        Gets the comments.  # noqa: E501

        Gets or sets the signature comments.  # noqa: E501

        :return: The comments.  # noqa: E501
        :rtype: str
        """
        return self._comments

    @comments.setter
    def comments(self, comments):
        """
        Sets the comments.

        Gets or sets the signature comments.  # noqa: E501

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
        if not isinstance(other, DigitalVBA):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
