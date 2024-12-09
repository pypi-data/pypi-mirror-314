###############################################################################
# Project: md_iso
# Purpose: Classes to manage transformation between mdJson and ISO19115-2
# Author:  Paul M. Breen
# Date:    2020-10-01
###############################################################################

__version__ = '0.1.0'

import os
import json

from beelzebub.base import BaseReader, BaseWriter, BaseProcessor, BaseWorkflow

ISO19115_2_DEFAULT_TEMPLATE = '{}/templates/iso19115-2.xml.j2'.format(os.path.dirname(os.path.realpath(__file__)))

class MdjsonReader(BaseReader):
    """
    Context manager for reading Mdjson input
    """

    def read(self):
        """
        Read the input source

        The input Mdjson is loaded as a dict and accessible via self.input

        :returns: The input
        :rtype: dict
        """

        self.input = json.load(self.fp)

        return self.input

class ISO19115_2Writer(BaseWriter):
    """
    Context manager for writing ISO19115_2 output
    """

    DEFAULTS = {
       'template': ISO19115_2_DEFAULT_TEMPLATE
    }

class MdjsonToISO19115_2Processor(BaseProcessor):
    """
    Execute an Mdjson to Iso19115_2 processing workflow
    """

class MdjsonToISO19115_2(BaseWorkflow):
    """
    Setup an Mdjson to ISO19115_2 processing workflow
    """

    def __init__(self, reader_class=MdjsonReader, writer_class=ISO19115_2Writer, processor_class=MdjsonToISO19115_2Processor, conf={}):
        """
        Constructor

        :param reader: reader class
        :type reader: class
        :param writer: writer class
        :type writer: class
        :param processor: input to output processor class
        :type processor: class
        :param conf: Optional configuration
        :type conf: dict
        """

        super().__init__(reader_class=reader_class, writer_class=writer_class, processor_class=processor_class, conf=conf)

