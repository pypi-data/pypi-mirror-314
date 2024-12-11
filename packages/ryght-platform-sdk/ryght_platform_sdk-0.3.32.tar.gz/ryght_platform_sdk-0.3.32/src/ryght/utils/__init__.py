# <---| * Module Information |--->
# ==================================================================================================================== #
"""
    :param FileName     :   utils/__init__.py
    :param Author       :   Sudo
    :param Date         :   2/06/2024
    :param Copyright    :   Copyright (c) 2024 Ryght, Inc. All Rights Reserved.
    :param License      :   # TODO
    :param Description  :   # TODO
"""
__author__ = 'Data engineering team'
__copyright__ = 'Copyright (c) 2024 Ryght, Inc. All Rights Reserved.'

# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Import section |--->
# -------------------------------------------------------------------------------------------------------------------- #
import os
import uuid
import enum
import logging

# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Logger Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #
logger = logging.getLogger(__name__)


# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Class Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #
class RequestMethods(enum.Enum):
    GET = 'GET'
    PUT = 'PUT'
    POST = 'POST'
    PATCH = 'PATCH'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'


# -------------------------------------------------------------------------------------------------------------------- #

class FlowTypes(enum.Enum):
    SEARCH = 'SEARCH'
    REASON = 'REASON'
    DOCUMENT_REASON = 'DOCUMENT_REASON'
    SEARCH_AND_REASON = 'SEARCH_AND_REASON'
    MULTIPLE_DOCUMENT_REASON = 'MULTIPLE_DOCUMENT_REASON'
    REASON_SEARCH_AND_REASON = 'REASON_SEARCH_AND_REASON'   
    SEARCH_AND_REASON_CITATION = 'SEARCH_AND_REASON_CITATION'    


# -------------------------------------------------------------------------------------------------------------------- #
class ModelOperation(enum.StrEnum):
    QA = "QA"
    EMBEDDING = "EMBEDDING"
    FILL_MASK = "FILL_MASK"
    COMPLETION = "COMPLETION"
    TRANSLATION = "TRANSLATION"
    SUMMARIZATION = "SUMMARIZATION"
    TEXT_GENERATION = "TEXT_GENERATION"


# -------------------------------------------------------------------------------------------------------------------- #
class QnARating(enum.StrEnum):
    THUMBS_UP = "THUMBS_UP"
    THUMBS_DOWN = "THUMBS_DOWN"


# -------------------------------------------------------------------------------------------------------------------- #
def set_logging_format(new_format):
    for handler in logging.root.handlers:
        handler.setFormatter(logging.Formatter(new_format))


# -------------------------------------------------------------------------------------------------------------------- #

def initialize_logging(file_path: str = './playground.logs', log_level: int = logging.INFO):
    """


    :param file_path: str
        Provide log file path with file name
    :param log_level:
    :return:
    """
    default_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    new_run_format = '%(message)s'

    if not os.path.isfile(file_path):
        open(file_path, 'x').close()

    logging.basicConfig(
        level=log_level,
        format=default_format,
        filename=file_path
    )
    run_id = uuid.uuid4()

    set_logging_format(new_run_format)
    logging.info('\n\n# -------------------------------------------------------------------------------------- #')
    logging.info(f'# -------------> | NEW RUN >> ID: {run_id} | < ------------- #')
    logging.info('# -------------------------------------------------------------------------------------- #\n\n')
    set_logging_format(default_format)
    return logging.getLogger(__name__)
# -------------------------------------------------------------------------------------------------------------------- #
