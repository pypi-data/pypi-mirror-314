from aspose.words.lowcode import mailmerging
from aspose.words.lowcode import reporting
from aspose.words.lowcode import splitting
import aspose.words
import aspose.pydrawing
import datetime
import decimal
import io
import uuid
from typing import Iterable, List
from enum import Enum

class Comparer:
    """Provides methods intended to compare documents."""
    
    @overload
    @staticmethod
    def compare(v1: str, v2: str, output_file_name: str, author: str, date_time: datetime.datetime) -> None:
        """Compares the document with another document producing changes as number of edit and format revisions.
        
        :param v1: The original document.
        :param v2: The modified document.
        :param output_file_name: The output file name.
        :param author: Initials of the author to use for revisions.
        :param date_time: The date and time to use for revisions."""
        ...
    
    @overload
    @staticmethod
    def compare(v1: str, v2: str, output_file_name: str, save_format: aspose.words.SaveFormat, author: str, date_time: datetime.datetime) -> None:
        """Compares the document with another document producing changes as number of edit and format revisions.
        
        :param v1: The original document.
        :param v2: The modified document.
        :param output_file_name: The output file name.
        :param save_format: The output's save format.
        :param author: Initials of the author to use for revisions.
        :param date_time: The date and time to use for revisions."""
        ...
    
    @overload
    @staticmethod
    def compare(v1: str, v2: str, output_file_name: str, author: str, date_time: datetime.datetime, compare_options: aspose.words.comparing.CompareOptions) -> None:
        """Compares the document with another document producing changes as number of edit and format revisions.
        
        :param v1: The original document.
        :param v2: The modified document.
        :param output_file_name: The output file name.
        :param author: Initials of the author to use for revisions.
        :param date_time: The date and time to use for revisions.
        :param compare_options: Document comparison options."""
        ...
    
    @overload
    @staticmethod
    def compare(v1: str, v2: str, output_file_name: str, save_format: aspose.words.SaveFormat, author: str, date_time: datetime.datetime, compare_options: aspose.words.comparing.CompareOptions) -> None:
        """Compares the document with another document producing changes as number of edit and format revisions.
        
        :param v1: The original document.
        :param v2: The modified document.
        :param output_file_name: The output file name.
        :param save_format: The output's save format.
        :param author: Initials of the author to use for revisions.
        :param date_time: The date and time to use for revisions.
        :param compare_options: Document comparison options."""
        ...
    
    @overload
    @staticmethod
    def compare(v1: io.BytesIO, v2: io.BytesIO, output_stream: io.BytesIO, save_format: aspose.words.SaveFormat, author: str, date_time: datetime.datetime) -> None:
        """Compares the document with another document producing changes as number of edit and format revisions.
        
        :param v1: The original document.
        :param v2: The modified document.
        :param output_stream: The output stream.
        :param save_format: The output's save format.
        :param author: Initials of the author to use for revisions.
        :param date_time: The date and time to use for revisions."""
        ...
    
    @overload
    @staticmethod
    def compare(v1: io.BytesIO, v2: io.BytesIO, output_stream: io.BytesIO, save_format: aspose.words.SaveFormat, author: str, date_time: datetime.datetime, compare_options: aspose.words.comparing.CompareOptions) -> None:
        """Compares the document with another document producing changes as number of edit and format revisions.
        
        :param v1: The original document.
        :param v2: The modified document.
        :param output_stream: The output stream.
        :param save_format: The output's save format.
        :param author: Initials of the author to use for revisions.
        :param date_time: The date and time to use for revisions.
        :param compare_options: Document comparison options."""
        ...
    
    ...

class Converter:
    """Represents a group of methods intended to convert a variety of different types of documents using a single line of code.
    
    The specified input and output files or streams, along with the desired save format,
    are used to convert the given input document of the one format into the output document
    of the other specified format.
    
    The convert functionality supports over 35+ different file formats.
    
    The :meth:`Converter.convert_to_images` group of methods are designed to transform documents into images,
    with each page being converted into a separate image file. These methods also convert PDF documents directly to fixed-page formats
    without loading them into the document model, which enhances both performance and accuracy.
    
    With :attr:`aspose.words.saving.ImageSaveOptions.page_set`, you can specify a particular set of pages to convert into images."""
    
    @overload
    @staticmethod
    def convert(input_file: str, output_file: str) -> None:
        """Converts the given input document into the output document using specified input output file names and its extensions.
        
        :param input_file: The input file name.
        :param output_file: The output file name."""
        ...
    
    @overload
    @staticmethod
    def convert(input_file: str, output_file: str, save_format: aspose.words.SaveFormat) -> None:
        """Converts the given input document into the output document using specified input output file names and the final document format.
        
        :param input_file: The input file name.
        :param output_file: The output file name.
        :param save_format: The save format."""
        ...
    
    @overload
    @staticmethod
    def convert(input_file: str, output_file: str, save_options: aspose.words.saving.SaveOptions) -> None:
        """Converts the given input document into the output document using specified input output file names and save options.
        
        :param input_file: The input file name.
        :param output_file: The output file name.
        :param save_options: The save options."""
        ...
    
    @overload
    @staticmethod
    def convert(input_file: str, load_options: aspose.words.loading.LoadOptions, output_file: str, save_options: aspose.words.saving.SaveOptions) -> None:
        """Converts the given input document into the output document using specified input output file names its load/save options.
        
        :param input_file: The input file name.
        :param load_options: The input document load options.
        :param output_file: The output file name.
        :param save_options: The save options."""
        ...
    
    @overload
    @staticmethod
    def convert(input_stream: io.BytesIO, output_stream: io.BytesIO, save_format: aspose.words.SaveFormat) -> None:
        """Converts the given input document into a single output document using specified input and output streams.
        
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        :param save_format: The save format."""
        ...
    
    @overload
    @staticmethod
    def convert(input_stream: io.BytesIO, output_stream: io.BytesIO, save_options: aspose.words.saving.SaveOptions) -> None:
        """Converts the given input document into a single output document using specified input and output streams.
        
        :param input_stream: The input streams.
        :param output_stream: The output stream.
        :param save_options: The save options."""
        ...
    
    @overload
    @staticmethod
    def convert(input_stream: io.BytesIO, load_options: aspose.words.loading.LoadOptions, output_stream: io.BytesIO, save_options: aspose.words.saving.SaveOptions) -> None:
        """Converts the given input document into a single output document using specified input and output streams.
        
        :param input_stream: The input streams.
        :param load_options: The input document load options.
        :param output_stream: The output stream.
        :param save_options: The save options."""
        ...
    
    @overload
    @staticmethod
    def convert_to_images(input_file: str, output_file: str) -> None:
        """Converts the input file pages to images.
        
        :param input_file: The input file name.
        :param output_file: The output file name used to generate file name for page images using rule "outputFile_pageIndex.extension""""
        ...
    
    @overload
    @staticmethod
    def convert_to_images(input_file: str, output_file: str, save_format: aspose.words.SaveFormat) -> None:
        """Converts the input file pages to images.
        
        :param input_file: The input file name.
        :param output_file: The output file name used to generate file name for page images using rule "outputFile_pageIndex.extension"
        :param save_format: Save format. Only image save formats are allowed."""
        ...
    
    @overload
    @staticmethod
    def convert_to_images(input_file: str, output_file: str, save_options: aspose.words.saving.ImageSaveOptions) -> None:
        """Converts the input file pages to images.
        
        :param input_file: The input file name.
        :param output_file: The output file name used to generate file name for page images using rule "outputFile_pageIndex.extension"
        :param save_options: Image save options."""
        ...
    
    @overload
    @staticmethod
    def convert_to_images(input_file: str, load_options: aspose.words.loading.LoadOptions, output_file: str, save_options: aspose.words.saving.ImageSaveOptions) -> None:
        """Converts the input file pages to images.
        
        :param input_file: The input file name.
        :param load_options: The input document load options.
        :param output_file: The output file name used to generate file name for page images using rule "outputFile_pageIndex.extension"
        :param save_options: Image save options."""
        ...
    
    @overload
    @staticmethod
    def convert_to_images(input_file: str, save_format: aspose.words.SaveFormat) -> List[io.BytesIO]:
        """Converts the input file pages to images.
        
        :param input_file: The input file name.
        :param save_format: Save format. Only image save formats are allowed.
        :returns: Returns array of image streams. The streams should be disposed by the enduser."""
        ...
    
    @overload
    @staticmethod
    def convert_to_images(input_file: str, save_options: aspose.words.saving.ImageSaveOptions) -> List[io.BytesIO]:
        """Converts the input file pages to images.
        
        :param input_file: The input file name.
        :param save_options: Image save options.
        :returns: Returns array of image streams. The streams should be disposed by the enduser."""
        ...
    
    @overload
    @staticmethod
    def convert_to_images(input_stream: io.BytesIO, save_format: aspose.words.SaveFormat) -> List[io.BytesIO]:
        """Converts the input stream pages to images.
        
        :param input_stream: The input stream.
        :param save_format: Save format. Only image save formats are allowed.
        :returns: Returns array of image streams. The streams should be disposed by the enduser."""
        ...
    
    @overload
    @staticmethod
    def convert_to_images(input_stream: io.BytesIO, save_options: aspose.words.saving.ImageSaveOptions) -> List[io.BytesIO]:
        """Converts the input stream pages to images.
        
        :param input_stream: The input stream.
        :param save_options: Image save options.
        :returns: Returns array of image streams. The streams should be disposed by the enduser."""
        ...
    
    @overload
    @staticmethod
    def convert_to_images(input_stream: io.BytesIO, load_options: aspose.words.loading.LoadOptions, save_options: aspose.words.saving.ImageSaveOptions) -> List[io.BytesIO]:
        """Converts the input stream pages to images.
        
        :param input_stream: The input stream.
        :param load_options: The input document load options.
        :param save_options: Image save options.
        :returns: Returns array of image streams. The streams should be disposed by the enduser."""
        ...
    
    @overload
    @staticmethod
    def convert_to_images(doc: aspose.words.Document, save_format: aspose.words.SaveFormat) -> List[io.BytesIO]:
        """Converts the document pages to images.
        
        :param doc: The input document.
        :param save_format: Save format. Only image save formats are allowed.
        :returns: Returns array of image streams. The streams should be disposed by the enduser."""
        ...
    
    @overload
    @staticmethod
    def convert_to_images(doc: aspose.words.Document, save_options: aspose.words.saving.ImageSaveOptions) -> List[io.BytesIO]:
        """Converts the document pages to images.
        
        :param doc: The input document.
        :param save_options: Image save options.
        :returns: Returns array of image streams. The streams should be disposed by the enduser."""
        ...
    
    ...

class MailMerger:
    """Provides methods intended to fill template with data using simple mail merge and mail merge with regions operations."""
    
    @overload
    @staticmethod
    def execute(input_file_name: str, output_file_name: str, field_names: List[str], field_values: List[object]) -> None:
        """Performs a mail merge operation for a single record.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name.
        :param field_names: Array of merge field names. Field names are not case sensitive. If a field name that is not found in the document is encountered, it is ignored.
        :param field_values: Array of values to be inserted into the merge fields. Number of elements in this array must be the same as the number of elements in fieldNames."""
        ...
    
    @overload
    @staticmethod
    def execute(input_file_name: str, output_file_name: str, save_format: aspose.words.SaveFormat, field_names: List[str], field_values: List[object]) -> None:
        """Performs a mail merge operation for a single record.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name.
        :param save_format: The output's save format.
        :param field_names: Array of merge field names. Field names are not case sensitive. If a field name that is not found in the document is encountered, it is ignored.
        :param field_values: Array of values to be inserted into the merge fields. Number of elements in this array must be the same as the number of elements in fieldNames."""
        ...
    
    @overload
    @staticmethod
    def execute(input_file_name: str, output_file_name: str, save_format: aspose.words.SaveFormat, mail_merge_options: aspose.words.lowcode.mailmerging.MailMergeOptions, field_names: List[str], field_values: List[object]) -> None:
        """Performs a mail merge operation for a single record.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name.
        :param save_format: The output's save format.
        :param mail_merge_options: Mail merge options.
        :param field_names: Array of merge field names. Field names are not case sensitive. If a field name that is not found in the document is encountered, it is ignored.
        :param field_values: Array of values to be inserted into the merge fields. Number of elements in this array must be the same as the number of elements in fieldNames."""
        ...
    
    @overload
    @staticmethod
    def execute(input_stream: io.BytesIO, output_stream: io.BytesIO, save_format: aspose.words.SaveFormat, field_names: List[str], field_values: List[object]) -> None:
        """Performs a mail merge operation for a single record.
        
        :param input_stream: The input file stream.
        :param output_stream: The output file stream.
        :param save_format: The output's save format.
        :param field_names: Array of merge field names. Field names are not case sensitive. If a field name that is not found in the document is encountered, it is ignored.
        :param field_values: Array of values to be inserted into the merge fields. Number of elements in this array must be the same as the number of elements in fieldNames."""
        ...
    
    @overload
    @staticmethod
    def execute(input_stream: io.BytesIO, output_stream: io.BytesIO, save_format: aspose.words.SaveFormat, mail_merge_options: aspose.words.lowcode.mailmerging.MailMergeOptions, field_names: List[str], field_values: List[object]) -> None:
        """Performs a mail merge operation for a single record.
        
        :param input_stream: The input file stream.
        :param output_stream: The output file stream.
        :param save_format: The output's save format.
        :param mail_merge_options: Mail merge options.
        :param field_names: Array of merge field names. Field names are not case sensitive. If a field name that is not found in the document is encountered, it is ignored.
        :param field_values: Array of values to be inserted into the merge fields. Number of elements in this array must be the same as the number of elements in fieldNames."""
        ...
    
    ...

class Merger:
    """Represents a group of methods intended to merge a variety of different types of documents into a single output document.
    
    The specified input and output files or streams, along with the desired merge and save options,
    are used to merge the given input documents into a single output document.
    
    The merging functionality supports over 35 different file formats."""
    
    @overload
    @staticmethod
    def merge(output_file: str, input_files: List[str]) -> None:
        """Merges the given input documents into a single output document using specified input and output file names.
        
        :param output_file: The output file name.
        :param input_files: The input file names.
        
        By default :attr:`MergeFormatMode.KEEP_SOURCE_FORMATTING` is used."""
        ...
    
    @overload
    @staticmethod
    def merge(output_file: str, input_files: List[str], save_format: aspose.words.SaveFormat, merge_format_mode: aspose.words.lowcode.MergeFormatMode) -> None:
        """Merges the given input documents into a single output document using specified input output file names and the final document format.
        
        :param output_file: The output file name.
        :param input_files: The input file names.
        :param save_format: The save format.
        :param merge_format_mode: Specifies how to merge formatting that clashes."""
        ...
    
    @overload
    @staticmethod
    def merge(output_file: str, input_files: List[str], save_options: aspose.words.saving.SaveOptions, merge_format_mode: aspose.words.lowcode.MergeFormatMode) -> None:
        """Merges the given input documents into a single output document using specified input output file names and save options.
        
        :param output_file: The output file name.
        :param input_files: The input file names.
        :param save_options: The save options.
        :param merge_format_mode: Specifies how to merge formatting that clashes."""
        ...
    
    @overload
    @staticmethod
    def merge(output_file: str, input_files: List[str], load_options: List[aspose.words.loading.LoadOptions], save_options: aspose.words.saving.SaveOptions, merge_format_mode: aspose.words.lowcode.MergeFormatMode) -> None:
        """Merges the given input documents into a single output document using specified input output file names and save options.
        
        :param output_file: The output file name.
        :param input_files: The input file names.
        :param load_options: Load options for the input files.
        :param save_options: The save options.
        :param merge_format_mode: Specifies how to merge formatting that clashes."""
        ...
    
    @overload
    @staticmethod
    def merge(input_files: List[str], merge_format_mode: aspose.words.lowcode.MergeFormatMode) -> aspose.words.Document:
        """Merges the given input documents into a single document and returns :class:`aspose.words.Document` instance of the final document.
        
        :param input_files: The input file names.
        :param merge_format_mode: Specifies how to merge formatting that clashes."""
        ...
    
    @overload
    @staticmethod
    def merge(input_files: List[str], load_options: List[aspose.words.loading.LoadOptions], merge_format_mode: aspose.words.lowcode.MergeFormatMode) -> aspose.words.Document:
        """Merges the given input documents into a single document and returns :class:`aspose.words.Document` instance of the final document.
        
        :param input_files: The input file names.
        :param load_options: Load options for the input files.
        :param merge_format_mode: Specifies how to merge formatting that clashes."""
        ...
    
    @overload
    @staticmethod
    def merge_stream(output_stream: io.BytesIO, input_streams: List[io.BytesIO], save_format: aspose.words.SaveFormat) -> None:
        """Merges the given input documents into a single output document using specified input output streams and the final document format.
        
        :param output_stream: The output stream.
        :param input_streams: The input streams.
        :param save_format: The save format."""
        ...
    
    @overload
    @staticmethod
    def merge_stream(output_stream: io.BytesIO, input_streams: List[io.BytesIO], save_options: aspose.words.saving.SaveOptions, merge_format_mode: aspose.words.lowcode.MergeFormatMode) -> None:
        """Merges the given input documents into a single output document using specified input output streams and save options.
        
        :param output_stream: The output stream.
        :param input_streams: The input streams.
        :param save_options: The save options.
        :param merge_format_mode: Specifies how to merge formatting that clashes."""
        ...
    
    @overload
    @staticmethod
    def merge_stream(input_streams: List[io.BytesIO], merge_format_mode: aspose.words.lowcode.MergeFormatMode) -> aspose.words.Document:
        """Merges the given input documents into a single document and returns :class:`aspose.words.Document` instance of the final document.
        
        :param input_streams: The input streams.
        :param merge_format_mode: Specifies how to merge formatting that clashes."""
        ...
    
    @staticmethod
    def merge_docs(input_documents: List[aspose.words.Document], merge_format_mode: aspose.words.lowcode.MergeFormatMode) -> aspose.words.Document:
        """Merges the given input documents into a single document and returns :class:`aspose.words.Document` instance of the final document.
        
        :param input_documents: The input documents.
        :param merge_format_mode: Specifies how to merge formatting that clashes."""
        ...
    
    ...

class Replacer:
    """Provides methods intended to find and replace text in the document."""
    
    @overload
    @staticmethod
    def replace(input_file_name: str, output_file_name: str, pattern: str, replacement: str) -> int:
        """Replaces all occurrences of a specified character string pattern with a replacement string.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name.
        :param pattern: A string to be replaced.
        :param replacement: A string to replace all occurrences of pattern.
        :returns: The number of replacements made."""
        ...
    
    @overload
    @staticmethod
    def replace(input_file_name: str, output_file_name: str, save_format: aspose.words.SaveFormat, pattern: str, replacement: str) -> int:
        """Replaces all occurrences of a specified character string pattern with a replacement string.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name.
        :param save_format: The save format.
        :param pattern: A string to be replaced.
        :param replacement: A string to replace all occurrences of pattern.
        :returns: The number of replacements made."""
        ...
    
    @overload
    @staticmethod
    def replace(input_file_name: str, output_file_name: str, save_format: aspose.words.SaveFormat, pattern: str, replacement: str, options: aspose.words.replacing.FindReplaceOptions) -> int:
        """Replaces all occurrences of a specified character string pattern with a replacement string.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name.
        :param save_format: The save format.
        :param pattern: A string to be replaced.
        :param replacement: A string to replace all occurrences of pattern.
        :param options: :class:`aspose.words.replacing.FindReplaceOptions` object to specify additional options.
        :returns: The number of replacements made."""
        ...
    
    @overload
    @staticmethod
    def replace(input_stream: io.BytesIO, output_stream: io.BytesIO, save_format: aspose.words.SaveFormat, pattern: str, replacement: str) -> int:
        """Replaces all occurrences of a specified character string pattern with a replacement string.
        
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        :param save_format: The save format.
        :param pattern: A string to be replaced.
        :param replacement: A string to replace all occurrences of pattern.
        :returns: The number of replacements made."""
        ...
    
    @overload
    @staticmethod
    def replace(input_stream: io.BytesIO, output_stream: io.BytesIO, save_format: aspose.words.SaveFormat, pattern: str, replacement: str, options: aspose.words.replacing.FindReplaceOptions) -> int:
        """Replaces all occurrences of a specified character string pattern with a replacement string.
        
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        :param save_format: The save format.
        :param pattern: A string to be replaced.
        :param replacement: A string to replace all occurrences of pattern.
        :param options: :class:`aspose.words.replacing.FindReplaceOptions` object to specify additional options.
        :returns: The number of replacements made."""
        ...
    
    ...

class ReportBuilder:
    """Provides methods intended to fill template with data using LINQ Reporting Engine."""
    
    @overload
    @staticmethod
    def build_report(input_file_name: str, output_file_name: str, data: object) -> None:
        """Populates the specified template document with data from the specified source making it a ready report.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name.
        :param data: A data source object."""
        ...
    
    @overload
    @staticmethod
    def build_report(input_file_name: str, output_file_name: str, data: object, report_builder_options: aspose.words.lowcode.reporting.ReportBuilderOptions) -> None:
        """Populates the specified template document with data from the specified source making it a ready report.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name.
        :param data: A data source object.
        :param report_builder_options: Additional report build options."""
        ...
    
    @overload
    @staticmethod
    def build_report(input_file_name: str, output_file_name: str, save_format: aspose.words.SaveFormat, data: object) -> None:
        """Populates the specified template document with data from the specified source making it a ready report.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name.
        :param save_format: The output's save format.
        :param data: A data source object."""
        ...
    
    @overload
    @staticmethod
    def build_report(input_file_name: str, output_file_name: str, save_format: aspose.words.SaveFormat, data: object, report_builder_options: aspose.words.lowcode.reporting.ReportBuilderOptions) -> None:
        """Populates the specified template document with data from the specified source making it a ready report.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name.
        :param save_format: The output's save format.
        :param data: A data source object.
        :param report_builder_options: Additional report build options."""
        ...
    
    @overload
    @staticmethod
    def build_report(input_stream: io.BytesIO, output_stream: io.BytesIO, save_format: aspose.words.SaveFormat, data: object) -> None:
        """Populates the specified template document with data from the specified source making it a ready report.
        
        :param input_stream: The input file stream.
        :param output_stream: The output file stream.
        :param save_format: The output's save format.
        :param data: A data source object."""
        ...
    
    @overload
    @staticmethod
    def build_report(input_stream: io.BytesIO, output_stream: io.BytesIO, save_format: aspose.words.SaveFormat, data: object, report_builder_options: aspose.words.lowcode.reporting.ReportBuilderOptions) -> None:
        """Populates the specified template document with data from the specified source making it a ready report.
        
        :param input_stream: The input file stream.
        :param output_stream: The output file stream.
        :param save_format: The output's save format.
        :param data: A data source object.
        :param report_builder_options: Additional report build options."""
        ...
    
    @overload
    @staticmethod
    def build_report(input_file_name: str, output_file_name: str, data: object, data_source_name: str) -> None:
        """Populates the specified template document with data from the specified source making it a ready report.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name.
        :param data: A data source object.
        :param data_source_name: A name to reference the data source object in the template."""
        ...
    
    @overload
    @staticmethod
    def build_report(input_file_name: str, output_file_name: str, data: object, data_source_name: str, report_builder_options: aspose.words.lowcode.reporting.ReportBuilderOptions) -> None:
        """Populates the specified template document with data from the specified source making it a ready report.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name.
        :param data: A data source object.
        :param data_source_name: A name to reference the data source object in the template.
        :param report_builder_options: Additional report build options."""
        ...
    
    @overload
    @staticmethod
    def build_report(input_file_name: str, output_file_name: str, save_format: aspose.words.SaveFormat, data: object, data_source_name: str) -> None:
        """Populates the specified template document with data from the specified source making it a ready report.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name.
        :param save_format: The output's save format.
        :param data: A data source object.
        :param data_source_name: A name to reference the data source object in the template."""
        ...
    
    @overload
    @staticmethod
    def build_report(input_file_name: str, output_file_name: str, save_format: aspose.words.SaveFormat, data: object, data_source_name: str, report_builder_options: aspose.words.lowcode.reporting.ReportBuilderOptions) -> None:
        """Populates the specified template document with data from the specified source making it a ready report.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name.
        :param save_format: The output's save format.
        :param data: A data source object.
        :param data_source_name: A name to reference the data source object in the template.
        :param report_builder_options: Additional report build options."""
        ...
    
    @overload
    @staticmethod
    def build_report(input_stream: io.BytesIO, output_stream: io.BytesIO, save_format: aspose.words.SaveFormat, data: object, data_source_name: str) -> None:
        """Populates the specified template document with data from the specified source making it a ready report.
        
        :param input_stream: The input file stream.
        :param output_stream: The output file stream.
        :param save_format: The output's save format.
        :param data: A data source object.
        :param data_source_name: A name to reference the data source object in the template."""
        ...
    
    @overload
    @staticmethod
    def build_report(input_stream: io.BytesIO, output_stream: io.BytesIO, save_format: aspose.words.SaveFormat, data: object, data_source_name: str, report_builder_options: aspose.words.lowcode.reporting.ReportBuilderOptions) -> None:
        """Populates the specified template document with data from the specified source making it a ready report.
        
        :param input_stream: The input file stream.
        :param output_stream: The output file stream.
        :param save_format: The output's save format.
        :param data: A data source object.
        :param data_source_name: A name to reference the data source object in the template.
        :param report_builder_options: Additional report build options."""
        ...
    
    @overload
    @staticmethod
    def build_report(input_file_name: str, output_file_name: str, data: List[object], data_source_names: List[str]) -> None:
        """Populates the specified template document with data from the specified sources making it a ready report.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name.
        :param data: An array of data source objects.
        :param data_source_names: An array of names to reference the data source objects within the template."""
        ...
    
    @overload
    @staticmethod
    def build_report(input_file_name: str, output_file_name: str, data: List[object], data_source_names: List[str], report_builder_options: aspose.words.lowcode.reporting.ReportBuilderOptions) -> None:
        """Populates the specified template document with data from the specified sources making it a ready report.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name.
        :param data: An array of data source objects.
        :param data_source_names: An array of names to reference the data source objects within the template.
        :param report_builder_options: Additional report build options."""
        ...
    
    @overload
    @staticmethod
    def build_report(input_file_name: str, output_file_name: str, save_format: aspose.words.SaveFormat, data: List[object], data_source_names: List[str]) -> None:
        """Populates the specified template document with data from the specified sources making it a ready report.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name.
        :param save_format: The output's save format.
        :param data: An array of data source objects.
        :param data_source_names: An array of names to reference the data source objects within the template."""
        ...
    
    @overload
    @staticmethod
    def build_report(input_file_name: str, output_file_name: str, save_format: aspose.words.SaveFormat, data: List[object], data_source_names: List[str], report_builder_options: aspose.words.lowcode.reporting.ReportBuilderOptions) -> None:
        """Populates the specified template document with data from the specified sources making it a ready report.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name.
        :param save_format: The output's save format.
        :param data: An array of data source objects.
        :param data_source_names: An array of names to reference the data source objects within the template.
        :param report_builder_options: Additional report build options."""
        ...
    
    @overload
    @staticmethod
    def build_report(input_stream: io.BytesIO, output_stream: io.BytesIO, save_format: aspose.words.SaveFormat, data: List[object], data_source_names: List[str]) -> None:
        """Populates the specified template document with data from the specified sources making it a ready report.
        
        :param input_stream: The input file stream.
        :param output_stream: The output file stream.
        :param save_format: The output's save format.
        :param data: An array of data source objects.
        :param data_source_names: An array of names to reference the data source objects within the template."""
        ...
    
    @overload
    @staticmethod
    def build_report(input_stream: io.BytesIO, output_stream: io.BytesIO, save_format: aspose.words.SaveFormat, data: List[object], data_source_names: List[str], report_builder_options: aspose.words.lowcode.reporting.ReportBuilderOptions) -> None:
        """Populates the specified template document with data from the specified sources making it a ready report.
        
        :param input_stream: The input file stream.
        :param output_stream: The output file stream.
        :param save_format: The output's save format.
        :param data: An array of data source objects.
        :param data_source_names: An array of names to reference the data source objects within the template.
        :param report_builder_options: Additional report build options."""
        ...
    
    ...

class Splitter:
    """Provides methods intended to split the documents into parts using different criteria."""
    
    @overload
    @staticmethod
    def remove_blank_pages(input_file_name: str, output_file_name: str) -> None:
        """Removes empty pages from the document and saves the output. Returns a list of page numbers that were removed.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name.
        :returns: List of page numbers has been considered as blank and removed."""
        ...
    
    @overload
    @staticmethod
    def remove_blank_pages(input_file_name: str, output_file_name: str, save_format: aspose.words.SaveFormat) -> None:
        """Removes empty pages from the document and saves the output in the specified format. Returns a list of page numbers that were removed.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name.
        :param save_format: The save format.
        :returns: List of page numbers has been considered as blank and removed."""
        ...
    
    @overload
    @staticmethod
    def remove_blank_pages(input_stream: io.BytesIO, output_stream: io.BytesIO, save_format: aspose.words.SaveFormat) -> None:
        """Removes blank pages from a document provided in an input stream and saves the updated document
        to an output stream in the specified save format. Returns a list of page numbers that were removed.
        
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        :param save_format: The save format.
        :returns: List of page numbers has been considered as blank and removed."""
        ...
    
    @overload
    @staticmethod
    def extract_pages(input_file_name: str, output_file_name: str, start_page_index: int, page_count: int) -> None:
        """Extracts a specified range of pages from a document file and saves the extracted pages
        to a new file. The output file format is determined by the extension of the output file name.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name.
        :param start_page_index: The zero-based index of the first page to extract.
        :param page_count: Number of pages to be extracted."""
        ...
    
    @overload
    @staticmethod
    def extract_pages(input_file_name: str, output_file_name: str, save_format: aspose.words.SaveFormat, start_page_index: int, page_count: int) -> None:
        """Extracts a specified range of pages from a document file and saves the extracted pages
        to a new file using the specified save format.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name.
        :param save_format: The save format.
        :param start_page_index: The zero-based index of the first page to extract.
        :param page_count: Number of pages to be extracted."""
        ...
    
    @overload
    @staticmethod
    def extract_pages(input_stream: io.BytesIO, output_stream: io.BytesIO, save_format: aspose.words.SaveFormat, start_page_index: int, page_count: int) -> None:
        """Extracts a specified range of pages from a document stream and saves the extracted pages
        to an output stream using the specified save format.
        
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        :param save_format: The save format.
        :param start_page_index: The zero-based index of the first page to extract.
        :param page_count: Number of pages to be extracted."""
        ...
    
    @overload
    @staticmethod
    def split(input_file_name: str, output_file_name: str, options: aspose.words.lowcode.splitting.SplitOptions) -> None:
        """Splits a document into multiple parts based on the specified split options and saves
        the resulting parts to files. The output file format is determined by the extension of the output file name.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name used to generate file name for document parts using rule "outputFile_partIndex.extension"
        :param options: Document split options."""
        ...
    
    @overload
    @staticmethod
    def split(input_file_name: str, output_file_name: str, save_format: aspose.words.SaveFormat, options: aspose.words.lowcode.splitting.SplitOptions) -> None:
        """Splits a document into multiple parts based on the specified split options and saves
        the resulting parts to files in the specified save format.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name used to generate file name for document parts using rule "outputFile_partIndex.extension"
        :param save_format: The save format.
        :param options: Document split options."""
        ...
    
    @overload
    @staticmethod
    def split(input_stream: io.BytesIO, save_format: aspose.words.SaveFormat, options: aspose.words.lowcode.splitting.SplitOptions) -> List[io.BytesIO]:
        """Splits a document from an input stream into multiple parts based on the specified split options and
        returns the resulting parts as an array of streams in the specified save format.
        
        :param input_stream: The input stream.
        :param save_format: The save format.
        :param options: Document split options."""
        ...
    
    ...

class Watermarker:
    """Provides methods intended to insert watermarks into the documents."""
    
    @overload
    @staticmethod
    def set_text(input_file_name: str, output_file_name: str, watermark_text: str) -> None:
        """Adds Text watermark into the document.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name.
        :param watermark_text: Text that is displayed as a watermark."""
        ...
    
    @overload
    @staticmethod
    def set_text(input_file_name: str, output_file_name: str, save_format: aspose.words.SaveFormat, watermark_text: str) -> None:
        """Adds Text watermark into the document.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name.
        :param save_format: The save format.
        :param watermark_text: Text that is displayed as a watermark."""
        ...
    
    @overload
    @staticmethod
    def set_text(input_stream: io.BytesIO, output_stream: io.BytesIO, save_format: aspose.words.SaveFormat, watermark_text: str) -> None:
        """Adds Text watermark into the document.
        
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        :param save_format: The save format.
        :param watermark_text: Text that is displayed as a watermark."""
        ...
    
    @overload
    @staticmethod
    def set_text(input_file_name: str, output_file_name: str, watermark_text: str, options: aspose.words.TextWatermarkOptions) -> None:
        """Adds Text watermark into the document.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name.
        :param watermark_text: Text that is displayed as a watermark.
        :param options: Defines additional options for the text watermark."""
        ...
    
    @overload
    @staticmethod
    def set_text(input_file_name: str, output_file_name: str, save_format: aspose.words.SaveFormat, watermark_text: str, options: aspose.words.TextWatermarkOptions) -> None:
        """Adds Text watermark into the document.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name.
        :param save_format: The save format.
        :param watermark_text: Text that is displayed as a watermark.
        :param options: Defines additional options for the text watermark."""
        ...
    
    @overload
    @staticmethod
    def set_text(input_stream: io.BytesIO, output_stream: io.BytesIO, save_format: aspose.words.SaveFormat, watermark_text: str, options: aspose.words.TextWatermarkOptions) -> None:
        """Adds Text watermark into the document.
        
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        :param save_format: The save format.
        :param watermark_text: Text that is displayed as a watermark.
        :param options: Defines additional options for the text watermark."""
        ...
    
    @overload
    @staticmethod
    def set_image(input_file_name: str, output_file_name: str, watermark_image_file_name: str) -> None:
        """Adds Image watermark into the document.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name.
        :param watermark_image_file_name: Image that is displayed as a watermark."""
        ...
    
    @overload
    @staticmethod
    def set_image(input_file_name: str, output_file_name: str, save_format: aspose.words.SaveFormat, watermark_image_file_name: str) -> None:
        """Adds Image watermark into the document.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name.
        :param save_format: The save format.
        :param watermark_image_file_name: Image that is displayed as a watermark."""
        ...
    
    @overload
    @staticmethod
    def set_image(input_file_name: str, output_file_name: str, watermark_image_file_name: str, options: aspose.words.ImageWatermarkOptions) -> None:
        """Adds Image watermark into the document.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name.
        :param watermark_image_file_name: Image that is displayed as a watermark.
        :param options: Defines additional options for the image watermark."""
        ...
    
    @overload
    @staticmethod
    def set_image(input_file_name: str, output_file_name: str, save_format: aspose.words.SaveFormat, watermark_image_file_name: str, options: aspose.words.ImageWatermarkOptions) -> None:
        """Adds Image watermark into the document.
        
        :param input_file_name: The input file name.
        :param output_file_name: The output file name.
        :param save_format: The save format.
        :param watermark_image_file_name: Image that is displayed as a watermark.
        :param options: Defines additional options for the image watermark."""
        ...
    
    ...

class MergeFormatMode(Enum):
    """Specifies how formatting is merged when combining multiple documents."""
    
    """Combine the formatting of the merged documents.
    
    By using this option, Aspose.Words adapts the formatting of the first document to match the structure and
    appearance of the second document, but keeps some of the original formatting intact.
    This option is useful when you want to maintain the overall look and feel of the destination document
    but still retain certain formatting aspects from the original document.
    
    This option does not have any affect when the input and the output formats are PDF."""
    MERGE_FORMATTING: int
    
    """Means that the source document will retain its original formatting,
    such as font styles, sizes, colors, indents, and any other formatting elements applied to its content.
    
    By using this option, you ensure that the copied content appears as it did in the original source,
    regardless of the formatting settings of the first document in merge queue.
    
    This option does not have any affect when the input and the output formats are PDF."""
    KEEP_SOURCE_FORMATTING: int
    
    """Preserve the layout of the original documents in the final document.
    
    In general, it looks like you print out the original documents and manually adhere them together using glue."""
    KEEP_SOURCE_LAYOUT: int
    

