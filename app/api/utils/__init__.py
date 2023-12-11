from typing import Callable
import os
import json
import time
import hashlib
import pandas as pd


def hash(*args, **kwargs):
    args_str = json.dumps(args, default=str)  # Serialize *args
    kwargs_str = json.dumps(
        kwargs, default=str, sort_keys=True
    )  # Serialize **kwargs with sorted keys
    combined_str = f"{args_str}{kwargs_str}"
    hash_value = hashlib.sha256(combined_str.encode("utf-8")).hexdigest()
    return hash_value


def delete_file(filepath: str) -> bool:
    try:
        os.remove(filepath)
        print(f"File '{filepath}' deleted successfully.")
        return True
    except FileNotFoundError:
        print(f"File '{filepath}' not found.")
    except PermissionError:
        print(f"Permission error: Unable to delete file '{filepath}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return False


def get_file_created_time(filepath) -> float:
    return os.path.getctime(filepath)


def is_file_created_within_24_hours(filepath) -> bool:
    file_creation_time = get_file_created_time(filepath=filepath)
    # Get the current time
    current_time = time.time()

    # Calculate the time difference in seconds
    time_difference = current_time - file_creation_time

    # Check if the file was created within the last 24 hours (86400 seconds)
    return time_difference <= 86400


class JsonCacher:
    dirname = "cache/api"

    def __init__(self, filename: str, check_time: bool = False) -> None:
        self.filename = filename
        self.check_time = check_time

    def __call__(self, method: Callable, extension: str = ".json") -> Callable:
        def wrapper(instance, *args, **kwargs):
            dirname = getattr(instance, "dirname", None)
            return_type = method.__annotations__.get("return")

            if not dirname:
                raise ValueError("Instance must have 'dirname' attribute")
            hashed = hash(*args, **kwargs)
            filename = self.filename + hashed + extension
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            filepath = os.path.join(dirname, filename)

            if os.path.exists(filepath):
                if self.check_time and not is_file_created_within_24_hours(
                    filepath=filepath
                ):
                    delete_file(filepath=filepath)
                else:
                    result = pd.read_json(filepath)
                    if return_type is not None:
                        if isinstance(result, pd.DataFrame) and issubclass(
                            return_type, pd.Series
                        ):
                            result = result.squeeze()
                    if not result.empty:
                        return result
            result = method(instance, *args, **kwargs)

            if return_type is not None:
                if not isinstance(result, return_type):
                    raise TypeError(
                        f"Function return type does not match the annotation {return_type}"
                    )
            if isinstance(result, pd.Series):
                result = result.to_frame()
            if isinstance(result, pd.DataFrame):
                result.to_json(filepath, date_format="iso")
                return result
            raise NotImplementedError(f"Return type not implemented.")

        return wrapper


class Cache:
    dirname = "cache/api"
    disable = False

    folderpath = "cache/api"

    def __init__(self, ttl: int = -1) -> None:
        self.ttl = ttl

    def __call__(self, method: Callable, extension: str = ".json") -> Callable:
        def wrapper(instance, *args, **kwargs) -> ...:
            dirname = os.path.join(self.dirname, *repr(instance).split("."))
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            filename = os.path.join(dirname, method.__name__ + extension)
            if not os.path.exists(filename):
                result = method(instance, *args, **kwargs)
                if self.disable:
                    return result
                if isinstance(result, pd.Series):
                    result = result.to_frame()
                result.to_json(filename, date_format="iso")
            out = pd.read_json(filename)
            return_type = method.__annotations__.get("return")
            if return_type is not None:
                if isinstance(out, pd.DataFrame) and issubclass(return_type, pd.Series):
                    return out.squeeze()
            return out

        return wrapper
