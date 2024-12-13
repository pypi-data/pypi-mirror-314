import aspose.words
import aspose.pydrawing
import datetime
import decimal
import io
import uuid
from typing import Iterable, List

class ReportBuilderOptions:
    """Represents options for the LINQ Reporting Engine functionality."""
    
    def __init__(self):
        ...
    
    @property
    def options(self) -> aspose.words.reporting.ReportBuildOptions:
        """Gets or sets a set of flags controlling behavior of this :class:`aspose.words.reporting.ReportingEngine` instance
        while building a report."""
        ...
    
    @options.setter
    def options(self, value: aspose.words.reporting.ReportBuildOptions):
        ...
    
    @property
    def missing_member_message(self) -> str:
        """Gets or sets a string value printed instead of a template expression that represents a plain reference to
        a missing member of an object. The default value is an empty string.
        
        The property should be used in conjunction with the :attr:`aspose.words.reporting.ReportBuildOptions.ALLOW_MISSING_MEMBERS`
        option. Otherwise, an exception is thrown when a missing member of an object is encountered.
        
        The property affects only printing of a template expression representing a plain reference to a missing
        object member. For example, printing of a binary operator, one of which operands references a missing
        object member, is not affected.
        
        The value of this property cannot be set to null."""
        ...
    
    @missing_member_message.setter
    def missing_member_message(self, value: str):
        ...
    
    @property
    def known_types(self) -> aspose.words.reporting.KnownTypeSet:
        """Gets an unordered set (i.e. a collection of unique items) containing  objects
        which fully or partially qualified names can be used within report templates processed by this engine
        instance to invoke the corresponding types' static members, perform type casts, etc."""
        ...
    
    ...

