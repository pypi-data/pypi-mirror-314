import hashlib
import os
import tempfile
from functools import cached_property
from typing import Any, Callable, Type
import logging
import traceback

from pydantic import BaseModel


def secret_hint(secret: str, reveal: int = 5) -> str:
    if not secret:
        return '<!!! EMPTY SECRET !!!>'

    # Calculate the SHA-256 hash of the secret
    secret_hash = hashlib.sha256(secret.encode()).hexdigest()

    # Determine the maximum number of characters to reveal
    max_reveal = len(secret) // 4
    reveal = min(reveal, max_reveal) // 2

    # Extract the revealed parts of the secret
    start_reveal = secret[:reveal]
    end_reveal = secret[-reveal:] if reveal else ''
    sep = '[...]' if start_reveal and end_reveal else '...'

    return f'<{secret_hash} ({start_reveal}{sep}{end_reveal}) Len: {len(secret)}>'


def exception_info(exception, msg: str = '') -> str:
    if msg:
        msg = f'\n{msg}'
    return f'({type(exception).__name__}) {str(exception)}{msg}'


def log_exception(exception: Exception, msg: str = '', stacktrace: bool = False) -> None:
    """
    Logs the exception in a better way.

    Args:
    - exception (Exception): The exception to be logged.
    """

    # Log the exception with informative details
    info = exception_info(exception, msg)
    logging.error(info)
    if stacktrace:
        logging.warning(traceback.format_exc())
    # from ..observability import exception_event
    # exception_event(type(exception).__name__, info)


def cleanup_temp_files(*file_paths: str) -> None:
    for file_path in file_paths:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)


# pool_size = (get_memory_max_in_mb() - 55.7) / 1.342424242
def get_memory_max_in_mb() -> float | None:
    """
    Read Kubernetes set memory limit for the current pod in MB.
    """
    try:
        with open('/sys/fs/cgroup/memory.max', 'r') as file:
            memory_limit_bytes = int(file.read().strip())
            return memory_limit_bytes / (1024 ** 2)  # Convert bytes to MB
    except Exception as e:
        print(f"Error reading memory limit: {e}")
        return None


def read_last_characters(file_obj, last_char_count: int = 100):
    if last_char_count == 0:
        file_obj.seek(0)  # Seek to the beginning
    else:
        file_obj.seek(-last_char_count, 2)  # Seek to the end of the file - 100 characters
    # Read the last characters
    return file_obj.read().decode('utf-8', 'replace')


def save_sbom_to_tempfile(file):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file.save(temp_file.name)
        return temp_file.name


def safe_getattr(obj, *attrs):
    for attr in attrs:
        if obj is not None and hasattr(obj, attr):
            obj = getattr(obj, attr)
        else:
            return None
    return obj


def get_properties(obj: Any) -> set[str]:
    cls = obj if isinstance(obj, type) else type(obj)
    return {name for name, attr in cls.__dict__.items() if isinstance(attr, (property, cached_property))}


def clone_common_fields(
        src: Any,
        target_class: Type[BaseModel],
        skip_fields=None,
        target2src_key_transformer: Callable[[str], str] | None = None
) -> dict[str, Any]:
    if skip_fields is None:
        skip_fields = {}
    if target2src_key_transformer is None:
        target2src_key_transformer = None if isinstance(src, dict) else lambda src_key: src_key.replace('-', '_')
    src_fields = src.keys() if isinstance(src, dict) else set(s for s in dir(src) if not s.startswith('_'))
    target_fields = [v.alias or k for k, v in target_class.model_fields.items()]
    src_getter = (lambda key: src.get(key, None)) if isinstance(src, dict) else lambda key2: getattr(src, key2)
    return {
        key: src_getter(target2src_key_transformer(key) if target2src_key_transformer else key)
        for key in target_fields
        if key not in skip_fields and (
            target2src_key_transformer(key) if target2src_key_transformer else key
        ) in src_fields
    }
