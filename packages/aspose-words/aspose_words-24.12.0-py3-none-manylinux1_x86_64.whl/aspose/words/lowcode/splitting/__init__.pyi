import aspose.words
import aspose.pydrawing
import datetime
import decimal
import io
import uuid
from typing import Iterable, List
from enum import Enum

class SplitOptions:
    """Specifies options how the document is split into parts."""
    
    def __init__(self):
        ...
    
    @property
    def split_criteria(self) -> aspose.words.lowcode.splitting.SplitCriteria:
        """Specifies the criteria for splitting the document into parts."""
        ...
    
    @split_criteria.setter
    def split_criteria(self, value: aspose.words.lowcode.splitting.SplitCriteria):
        ...
    
    @property
    def split_style(self) -> str:
        """Specifies the paragraph style for splitting the document into parts when :attr:`SplitCriteria.STYLE` is used."""
        ...
    
    @split_style.setter
    def split_style(self, value: str):
        ...
    
    ...

class SplitCriteria(Enum):
    """Specifies how the document is split into parts."""
    
    """Specifies that the document is split into pages."""
    PAGE: int
    
    """Specifies that the document is split into parts at a section break of any type."""
    SECTION_BREAK: int
    
    """Specifies that the document is split into parts at a paragraph formatted using the style specified in :attr:`SplitOptions.split_style`."""
    STYLE: int
    

