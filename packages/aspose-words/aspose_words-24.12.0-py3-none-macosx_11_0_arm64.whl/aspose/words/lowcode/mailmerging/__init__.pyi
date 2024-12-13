import aspose.words
import aspose.pydrawing
import datetime
import decimal
import io
import uuid
from typing import Iterable, List

class MailMergeOptions:
    """Represents options for the mail merge functionality."""
    
    def __init__(self):
        ...
    
    @property
    def region_start_tag(self) -> str:
        """Gets or sets a mail merge region start tag."""
        ...
    
    @region_start_tag.setter
    def region_start_tag(self, value: str):
        ...
    
    @property
    def region_end_tag(self) -> str:
        """Gets or sets a mail merge region end tag."""
        ...
    
    @region_end_tag.setter
    def region_end_tag(self, value: str):
        ...
    
    @property
    def cleanup_options(self) -> aspose.words.mailmerging.MailMergeCleanupOptions:
        """Gets or sets a set of flags that specify what items should be removed during mail merge."""
        ...
    
    @cleanup_options.setter
    def cleanup_options(self, value: aspose.words.mailmerging.MailMergeCleanupOptions):
        ...
    
    @property
    def cleanup_paragraphs_with_punctuation_marks(self) -> bool:
        """Gets or sets a value indicating whether paragraphs with punctuation marks are considered as empty
        and should be removed if the :attr:`aspose.words.mailmerging.MailMergeCleanupOptions.REMOVE_EMPTY_PARAGRAPHS` option is specified.
        
        The default value is ``True``.
        
        Here is the complete list of cleanable punctuation marks:
        
        * !
        
        * ,
        
        * .
        
        * :
        
        * ;
        
        * ?
        
        * ¡
        
        * ¿"""
        ...
    
    @cleanup_paragraphs_with_punctuation_marks.setter
    def cleanup_paragraphs_with_punctuation_marks(self, value: bool):
        ...
    
    @property
    def use_non_merge_fields(self) -> bool:
        """When ``True``, specifies that in addition to MERGEFIELD fields, mail merge is performed into some other types of fields and
        also into "{{fieldName}}" tags.
        
        Normally, mail merge is only performed into MERGEFIELD fields, but several customers had their reporting
        built using other fields and had many documents created this way. To simplify migration (and because this
        approach was independently used by several customers) the ability to mail merge into other fields was introduced.
        
        When :attr:`MailMergeOptions.use_non_merge_fields` is set to ``True``, Aspose.Words will perform mail merge into the following fields:
        
        MERGEFIELD FieldName
        
        MACROBUTTON NOMACRO FieldName
        
        IF 0 = 0 "{FieldName}" ""
        
        Also, when :attr:`MailMergeOptions.use_non_merge_fields` is set to ``True``, Aspose.Words will perform mail merge into text tags
        "{{fieldName}}". These are not fields, but just text tags."""
        ...
    
    @use_non_merge_fields.setter
    def use_non_merge_fields(self, value: bool):
        ...
    
    @property
    def preserve_unused_tags(self) -> bool:
        """Gets or sets a value indicating whether the unused "mustache" tags should be preserved.
        
        The default value is ``False``."""
        ...
    
    @preserve_unused_tags.setter
    def preserve_unused_tags(self, value: bool):
        ...
    
    @property
    def merge_duplicate_regions(self) -> bool:
        """Gets or sets a value indicating whether all of the document mail merge regions with the name of a data source
        should be merged while executing of a mail merge with regions against the data source or just the first one.
        
        The default value is ``False``."""
        ...
    
    @merge_duplicate_regions.setter
    def merge_duplicate_regions(self, value: bool):
        ...
    
    @property
    def merge_whole_document(self) -> bool:
        """Gets or sets a value indicating whether fields in whole document are updated while executing of a mail merge with regions.
        
        The default value is ``False``."""
        ...
    
    @merge_whole_document.setter
    def merge_whole_document(self, value: bool):
        ...
    
    @property
    def use_whole_paragraph_as_region(self) -> bool:
        """Gets or sets a value indicating whether whole paragraph with **TableStart** or **TableEnd** field
        or particular range between **TableStart** and **TableEnd** fields should be included into mail merge region.
        
        The default value is ``True``."""
        ...
    
    @use_whole_paragraph_as_region.setter
    def use_whole_paragraph_as_region(self, value: bool):
        ...
    
    @property
    def restart_lists_at_each_section(self) -> bool:
        """Gets or sets a value indicating whether lists are restarted at each section after executing of a mail merge.
        
        The default value is ``True``."""
        ...
    
    @restart_lists_at_each_section.setter
    def restart_lists_at_each_section(self, value: bool):
        ...
    
    @property
    def trim_whitespaces(self) -> bool:
        """Gets or sets a value indicating whether trailing and leading whitespaces are trimmed from mail merge values.
        
        The default value is ``True``."""
        ...
    
    @trim_whitespaces.setter
    def trim_whitespaces(self, value: bool):
        ...
    
    @property
    def unconditional_merge_fields_and_regions(self) -> bool:
        """Gets or sets a value indicating whether merge fields and merge regions are merged regardless of the parent IF field's condition.
        
        The default value is ``False``."""
        ...
    
    @unconditional_merge_fields_and_regions.setter
    def unconditional_merge_fields_and_regions(self, value: bool):
        ...
    
    @property
    def retain_first_section_start(self) -> bool:
        """Gets or sets a value indicating whether the section start of the first document section and its copies for subsequent data source rows
        are retained during mail merge or updated according to MS Word behaviour.
        
        The default value is ``True``."""
        ...
    
    @retain_first_section_start.setter
    def retain_first_section_start(self, value: bool):
        ...
    
    ...

