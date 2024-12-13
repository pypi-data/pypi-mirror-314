import functools
import json
from io import BytesIO
from typing import Any, Callable

import falcon
import flask
import numpy as np


class StaticJSONResource:
    """Any JSON serializable object, representing a "static" resource (i.e. a
    resource that does not depend on request parameters).

    The object will be represented as a plain JSON string, when a GET request is
    invoked."""

    def __init__(self, obj: Any):
        """
        Parameters
        ----------
        obj : Any
            A JSON serializable object, i.e. is should be compatible with
            `json.dumps`.
        """
        self._obj = obj

    def on_get(self, _, resp: falcon.Response):
        resp.text = json.dumps(self._obj)


def apply_or_abort(
    condition: bool,
    error_code: int = 500,
    error_msg: str | None = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """A decorator with arguments, which will decorate a function to execute
    only of `condition` is true. Otherwise, abort (using `flask.abort`) with
    `error_code` and `error_msg`.

    Parameters
    ----------
    condition : bool
        The condition to check for.
    error_code : int, optional
        HTTP error code to use for aborting, by default 500.
    error_msg : str | None, optional
        The error message to print, by default `None`.

    Returns
    -------
    functional : Callable[[Callable[..., Any]], Callable[..., Any]]
        The actual decorator.
    """

    def decorator(fun):
        @functools.wraps(fun)
        def wrapper_fun(*args, **kwargs):
            if condition:
                return fun(*args, **kwargs)
            else:
                flask.abort(error_code, error_msg)

        return wrapper_fun

    return decorator


def try_or_abort(
    error_code: int = 500,
    error_msg: str | None = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """A decorator with arguments, which will try to execute the decorated
    function. If any exception occurs, catch it but abort using `flask.abort`.

    Parameters
    ----------
    error_code : int, optional
        HTTP error code to use for aborting, by default 500.
    error_msg : str | None, optional
        The error message to print, if not `None`. Otherwise print the
        exception's error message. By default `None`.

    Returns
    -------
    functional: Callable[[Callable[..., Any]], Callable[..., Any]]
        The actual decorator.
    """

    def decorator(fun):
        @functools.wraps(fun)
        def wrapper_fun(*args, **kwargs):
            try:
                return fun(*args, **kwargs)
            except Exception as e:
                flask.abort(
                    error_code, error_msg if error_msg is not None else e.args[0]
                )

        return wrapper_fun

    return decorator


def named_ndarrays_to_bytes(named_arrays: dict[str, np.ndarray]) -> bytes:
    """Convert named NumPy arrays to a compressed bytes sequence.

    Use this for example as payload data in a POST request.

    Parameters
    ----------
    named_arrays : dict[str, np.ndarray]
        The named NumPy arrays.

    Returns
    -------
    bytes
        A compressed bytes sequence.

    Notes
    -----
    This is the inverse to `bytes_to_named_ndarrays`.
    """
    compressed_arrays = BytesIO()
    np.savez_compressed(compressed_arrays, **named_arrays)
    return compressed_arrays.getvalue()


def bytes_to_named_ndarrays(data: bytes) -> dict[str, np.ndarray]:
    """Convert a bytes sequence of named (and compressed) NumPy arrays back to
    arrays.

    Use this for example to retrieve NumPy arrays from an HTTP response.

    Parameters
    ----------
    data : bytes
        The bytes representation of a (compressed)

    Returns
    -------
    dict[str, np.ndarray]
        The named arrays.

    Raises
    ------
    OSError
        If the input file does not exist or cannot be read.
    ValueError
        If the file contains an object array.


    Notes
    -----
    This in the inverse to `named_ndarrays_to_bytes`.
    """
    arrays = np.load(BytesIO(data))
    return {name: arrays[name] for name in arrays.files}
