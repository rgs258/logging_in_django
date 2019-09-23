import atexit
import json
import logging
from io import TextIOBase
from socket import gethostname

from django.core.serializers.json import DjangoJSONEncoder


def extra_data(extra_data, jsonify=False):
    """
    Formats any input such that it will appear in the args[] section of a message in rollbar. The return value should
    be passed to the logger as the value of the extra param. This assumes that the python logging facility has a
    RollbarHandler.
    :param extra_data: anything you want to send to rollbar, but honestly it should probably be a string or a
    simple collection
    :return: a dict that can be sent to the extra param of a logger.
    """
    return {'extra_data': {'args': json.dumps(extra_data, cls=DjangoJSONEncoder) if jsonify else extra_data}}


class HostnameAddingFormatter(logging.Formatter):
    """
    HostnameAddingFormatter adds a hostname, whe it can find one, to the record. The hostname is then available for
    use int he format string when using this formatter class.
    """

    def __init__(self, fmt=None, datefmt=None, style='%'):
        super().__init__(fmt, datefmt, style)

    def format(self, record):
        # Try to add a hostname attribute to every log record
        try:
            record.__dict__['hostname'] = gethostname()
        except:
            record.__dict__['hostname'] = 'exception-getting-hostname'
        return super().format(record)


class ExtendedFormatter(HostnameAddingFormatter):
    """
    ExtendedFormatter extends logging.Formatter to provide an extra formatting step whenever extra_data is present on
    the
    record. This allows for the developer to send additional logging information to the console by passing the result
    of a call to extra_data to the logger as the extra param.

    """

    def __init__(self, fmt=None, datefmt=None, style='%'):
        super().__init__(fmt, datefmt, style)

    def format(self, record):
        """
        Formats the LogRecord, making use of extra_data, fir the console.
        :param record:
        :return: a string of formatted log data
        """
        try:
            # Try to add a hostname attribute to every log record that'll be formatted by the ExtendedFormatter :)
            record.__dict__['hostname'] = gethostname()
        except:
            # Don't let gethostname get in the way of processing the LogRecorc
            record.__dict__['hostname'] = 'exception-getting-hostname'

        # Format using the parent formatter first
        s = super().format(record)
        try:
            # Try to add additional formatting
            extra_data_string = str(record.extra_data)
            try:
                # Try to treat the extra_data as json
                extra_data_string = json.dumps(record.extra_data, sort_keys=True, indent=4)
            except:
                # Accept that this might not be json data and move on
                pass
            string_with_extra_info = s
            string_with_extra_info += "\n *** BEGIN extra_data ****"
            string_with_extra_info += "\n" + extra_data_string
            string_with_extra_info += "\n *** END extra_data ****"
            string_with_extra_info += "\n\n"
            s = string_with_extra_info
        except:
            # Don't let failures in adding additional formatting get in the way of processing the LogRecorc
            pass
        return s


class StreamToLogger(TextIOBase):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """

    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.line_buffer = ''
        atexit.register(self.write, '\n')

    def flush(self):
        self.logger.log(self.log_level, self.line_buffer)
        self.line_buffer = ''

    def write(self, buf):
        char_count = 0
        for line in buf.splitlines():
            char_count += len(line)
            to_write = line
            self.line_buffer = self.line_buffer + to_write
        if buf.endswith('\n'):
            self.flush()
        return char_count


class SomethingFilter(logging.Filter):
    def filter(self, record):
        """
        Filters out log records having the word 'something' in them.
        :param record: any LogRecord
        :return: False if the record.message has the word 'something' in it, else True
        """
        return False if 'something' in record.message else True
