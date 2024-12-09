# coding: utf-8

# -----------------------------------------------------------------------------------
# <copyright company="Aspose Pty Ltd">
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

from __future__ import absolute_import

import unittest
import os

from groupdocs_signature_cloud import *
from test.test_context import TestContext
from test.test_file import TestFile

class TestVerifyCollection(TestContext):

    def test_verify_collection_image(self):
        test_file = TestFile.image_signed()
        settings = self.populate_options_image(test_file)            
        response = self.sign_api.verify_signatures(VerifySignaturesRequest(settings))
        self.check_response(response, test_file)

    def test_verify_collection_pdf(self):
        test_file = TestFile.pdf_signed()
        settings = self.populate_options(test_file)            
        response = self.sign_api.verify_signatures(VerifySignaturesRequest(settings))
        self.check_response(response, test_file)

    def test_verify_collection_presentation(self):
        test_file = TestFile.presentation_signed()
        settings = self.populate_options_image(test_file)            
        response = self.sign_api.verify_signatures(VerifySignaturesRequest(settings))
        self.check_response(response, test_file)

    def test_verify_collection_spreadsheet(self):
        test_file = TestFile.spreadsheet_signed()
        settings = self.populate_options(test_file)            
        response = self.sign_api.verify_signatures(VerifySignaturesRequest(settings))
        self.check_response(response, test_file)

    def test_verify_collection_wordprocessing(self):
        test_file = TestFile.wordprocessing_signed()
        settings = self.populate_options(test_file)            
        response = self.sign_api.verify_signatures(VerifySignaturesRequest(settings))
        self.check_response(response, test_file)                       

    @staticmethod
    def barcode_opts():
        opts = VerifyBarcodeOptions()
        
        opts.signature_type = 'Barcode'
        opts.text = '123456789012'
        opts.barcode_type = 'Code39'
        opts.match_type = 'Contains'

        opts.page = 1
        opts.all_pages = True
        ps = PagesSetup()
        ps.even_pages = False
        ps.first_page = True
        ps.last_page = False
        ps.odd_pages = False
        ps.page_numbers = [1]
        opts.pages_setup = ps

        return opts

    @staticmethod
    def qr_code_opts():
        opts = VerifyQRCodeOptions()
        
        opts.signature_type = 'QRCode'
        opts.text = 'John Smith'
        opts.qr_code_type = 'Aztec'
        opts.match_type = 'Contains'

        opts.page = 1
        opts.all_pages = True
        ps = PagesSetup()
        ps.even_pages = False
        ps.first_page = True
        ps.last_page = False
        ps.odd_pages = False
        ps.page_numbers = [1]
        opts.pages_setup = ps

        return opts

    @staticmethod
    def digital_opts():
        opts = VerifyDigitalOptions()
        
        opts.signature_type = 'Digital'

        opts.page = 1
        opts.all_pages = True
        ps = PagesSetup()
        ps.even_pages = False
        ps.first_page = True
        ps.last_page = False
        ps.odd_pages = False
        ps.page_numbers = [1]
        opts.pages_setup = ps

        return opts        

    @staticmethod
    def text_opts():
        opts = VerifyTextOptions()
        
        opts.signature_type = 'Text'
        opts.text = 'John Smith'
        opts.match_type = 'Contains'

        opts.page = 1
        opts.all_pages = True
        ps = PagesSetup()
        ps.even_pages = False
        ps.first_page = True
        ps.last_page = False
        ps.odd_pages = False
        ps.page_numbers = [1]
        opts.pages_setup = ps

        return opts         

    @staticmethod
    def populate_options_image(testFile):
        settings = VerifySettings()
        settings.file_info = testFile.ToFileInfo()        
        settings.options = [TestVerifyCollection.barcode_opts(),
                            TestVerifyCollection.qr_code_opts()]
        return settings

    @staticmethod
    def populate_options(testFile):
        settings = VerifySettings()
        settings.file_info = testFile.ToFileInfo()
        settings.options = [TestVerifyCollection.barcode_opts(),
                            TestVerifyCollection.qr_code_opts(),
                            TestVerifyCollection.digital_opts(),
                            TestVerifyCollection.text_opts()]
        return settings        
    
    def check_response(self, response, test_file):
        self.assertTrue(response)
        self.assertTrue(response.file_info)
        self.assertEqual(response.file_info.file_path, test_file.FilePath())     


if __name__ == '__main__':
    unittest.main()
