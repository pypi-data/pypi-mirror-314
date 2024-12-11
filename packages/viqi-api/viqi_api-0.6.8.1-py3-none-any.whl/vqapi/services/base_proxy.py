# import functools
import copy
import hashlib
import io
import logging
import os
import shutil
import tarfile
import tempfile
import time
import urllib
import urllib.parse

import requests
from bq.metadoc.formats import Metadoc

from vqapi.exception import BQApiError, code_to_exception, http_code_future_not_ready
from vqapi.util import custom_json_loads, custom_json_dumps

# from vqapi.util import is_uniq_code, normalize_unicode

log = logging.getLogger("vqapi.services")


class ResponseFile(io.IOBase):
    """
    IO byte stream to return single file responses. Can be used as context manager.
    """

    def __init__(self, response):
        if isinstance(response, str):
            # file path
            self.stream = open(response, "rb")
            self.response = None
            self.fpath = response
        else:
            response.raw.decode_content = True  # in case of compression
            self.stream = response.raw
            self.response = response
            self.fpath = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stream.close()

    def read(self, size: int = -1) -> bytes:
        """
        Read some bytes from stream.

        Args:
            size: number of bytes to read

        Returns:
            bytes read
        """
        return self.stream.read(size)

    def readall(self) -> bytes:
        """
        Read all bytes from stream.

        Returns:
            bytes read
        """
        return self.stream.read()

    def readinto(self, b):
        raise io.UnsupportedOperation("no readinto in reponse stream")

    def close(self):
        """
        Close stream.
        """
        self.stream.close()

    def write(self, b):
        raise io.UnsupportedOperation("no write in reponse stream")

    def copy_into(self, localpath: str, full_path: bool = True) -> str:
        """
        Copy this file into localpath/ and return its path.

        Args:
            localpath: local path where to write bytes to
            full_path: if True, localpath includes the filename; otherwise, localpath is a folder

        Returns:
            path of generated file
        """
        if self.fpath is not None:
            outname = os.path.join(localpath, os.path.basename(self.fpath))
            shutil.copyfile(self.fpath, outname)
        else:
            outname = os.path.join(localpath, "responsefile") if not full_path else localpath
            with open(outname, "wb") as fout:
                for block in self.response.iter_content(chunk_size=16 * 1024 * 1024):  # 16MB
                    fout.write(block)
                fout.flush()
        return outname

    def force_to_filepath(self) -> str:
        """
        Force this file into a locally accessible file and return its path.

        Returns:
            path of generated file
        """
        if self.fpath is not None:
            return self.fpath
        else:
            with tempfile.NamedTemporaryFile(mode="w+b", prefix="viqicomm", delete=False) as fout:  # who deletes this?
                for block in self.response.iter_content(chunk_size=16 * 1024 * 1024):  # 16MB
                    fout.write(block)
                fout.flush()
                return fout.name


class ResponseFolder:
    """
    Class to return folder structure. Can be used as context manager.
    """

    def __init__(self, response):
        if isinstance(response, str):
            # folder path
            self.stream = response
        else:
            # http response => interpret as tarfile
            # self.stream = tarfile.open(fileobj=response.raw, mode='r|')  # this does not work because tarfile needs seeks
            self.stream = tarfile.open(
                fileobj=io.BytesIO(response.content), mode="r|"
            )  # TODO: may lead to out of memory

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not isinstance(self.stream, str):
            self.stream.close()

    def copy_into(
        self,
        localpath: str,
        full_path: bool = True,  # pylint: disable=unused-argument
    ) -> str:
        """
        Copy this folder structure into localpath/ and return its path.

        Args:
            localpath: local path where to write bytes to
            full_path: ignored (just to mirror ResponseFile)

        Returns:
            path of generated file
        """
        if isinstance(self.stream, str):
            outname = os.path.join(localpath, os.path.basename(self.stream))
            shutil.copytree(self.stream, outname)
        else:
            self.stream.extractall(localpath)
            # localpath should now contain a single folder with subfolders/files
            outname = next(
                os.path.abspath(os.path.join(localpath, name))
                for name in os.listdir(localpath)
                if os.path.isdir(os.path.join(localpath, name))
            )
        return outname

    def force_to_filepath(self) -> str:
        """
        Force this folder structure into a locally accessible (tar) file and return its path.

        Returns:
            path of generated file
        """
        with tempfile.NamedTemporaryFile(
            mode="w+b", prefix="viqicomm", suffix=".tar", delete=False
        ) as fout:  # who deletes this?
            if isinstance(self.stream, str):
                # folder path => package it as single tar file
                with tarfile.open(fileobj=fout, mode="w") as tout:  # TODO: could compress here
                    tout.add(self.stream, os.path.basename(self.stream), recursive=True)
            else:
                # is alread tarfile obj => copy to actual file
                shutil.copyfileobj(self.stream.fileobj, fout)
        return fout.name


class FutureResponse:
    def __init__(self, status_code: int, doc: Metadoc):
        self.status_code = status_code
        self._doc = doc

    def doc(self):
        return self._doc

    @property
    def text(self):
        # TODO: hack... return json directly from future service instead one day
        return custom_json_dumps(self._doc.to_json())


####
#### KGK
#### Still working on filling this out
#### would be cool to have service definition language to make these.
#### TODO more service, renders etc.


class BaseServiceProxy:
    # DEFAULT_TIMEOUT=None
    DEFAULT_TIMEOUT = 60 * 60  # 1 hour
    timeout = DEFAULT_TIMEOUT
    headers = None
    render = None

    def __init__(self, session, service_url):  # noqa
        self.session = session
        self.service_url = service_url  # if isinstance(service_url, str) else service_url.service_url

    def __str__(self):
        return self.service_url

    def construct(self, path, params=None):
        url = self.service_url
        if params:
            path = f"{path}?{urllib.parse.urlencode(params)}"
        if path:
            url = urllib.parse.urljoin(str(url), str(path))
        return url

    def __call__(self, timeout=DEFAULT_TIMEOUT, headers=None, render=None):
        """Allows service global overrides.. used for sub services

        Example:
           meta = session.service("meta")
           meta_fast = meta(timeout=1).get( "/00-XXX")

           meta_special = meta(headers  = { 'my-header' : 'my-value'} )
           meta_special.get( .. )

        """
        svc = copy.copy(self)
        svc.timeout = timeout
        svc.headers = headers
        svc.render = render
        return svc

    # =================== TODO: get rid of render param ============
    # =================== TODO: move parts of formats.py into api section =========================

    def request(
        self, path: str | None = None, params: dict | None = None, method: str = "get", render: str | None = None, **kw
    ):
        """
        Generic REST-type request to the service (should not be called, use service specific functions instead).

        Args:
            path: a path relative to service (maybe a string or list)
            params: a dictionary of value to encode as params
            method: request type (get, put, post, etc)
            render: 'doc'/'etree'/'xml' to request doc response, 'json' for JSON response

        Returns:
            a request.response (INDEPENDENT OF render!)
        """
        if isinstance(path, list):
            path = "/".join(path)

        if path and path[0] == "/":
            path = path[1:]
        if path:
            path = urllib.parse.urljoin(str(self.service_url), str(path))
        else:
            path = str(self.service_url)

        # no longer in session https://github.com/requests/requests/issues/3341
        timeout = kw.pop("timeout", self.timeout)
        headers = kw.pop("headers", self.headers or {})
        render = render or self.render
        data = kw.get("data")
        if isinstance(data, str):  # hacky way to guess content type
            data = data.lstrip()
            if data[0] == "<":
                headers["Content-Type"] = "text/xml"  # TODO: -------------- use formatters on kw['data']!!!!
            elif data[0] in ("{", "["):
                headers["Content-Type"] = "application/json"  # TODO: -------------- use formatters on kw['data']!!!!
        #         if render in ("xml", "etree", "doc"):
        #             headers["Accept"] = "text/xml"
        if render in ("json",):
            headers["Accept"] = "application/json"
        else:
            headers["Accept"] = "text/xml"  # default xml transmission
        # ignore any format request because it is handled via render and headers
        # not all params are dics, they may be a list of tuples for ordered params
        if params is not None and isinstance(params, dict):
            params.pop("format", None)

        response = self.session.c.request(
            url=path,
            params=params,
            method=method,
            timeout=timeout,
            headers=headers,
            **kw,
        )
        return response

    def fetch(self, path=None, params=None, render=None, **kw):
        return self.request(path=path, params=params, render=render, **kw)

    def get(self, path=None, params=None, render=None, **kw):
        return self.request(path=path, params=params, render=render, **kw)

    def post(self, path=None, params=None, render=None, **kw):
        return self.request(path=path, params=params, render=render, method="post", **kw)

    def put(self, path=None, params=None, render=None, **kw):
        return self.request(path=path, params=params, render=render, method="put", **kw)

    def patch(self, path=None, params=None, render=None, **kw):
        return self.request(path=path, params=params, render=render, method="patch", **kw)

    def delete(self, path=None, params=None, render=None, **kw):
        return self.request(path=path, params=params, render=render, method="delete", **kw)

    def fetch_file(self, path=None, params=None, render=None, localpath=None, **kw):
        with self.fetch(path=path, params=params, render=render, stream=True, **kw) as response:
            if response.status_code != requests.codes.ok:  # pylint: disable=no-member
                raise BQApiError(response)

            # OK response download
            original_length = content_left = response.headers.get("content-length")
            # log.debug('content-length: %s', original_length)
            content_md5 = response.headers.get("x-content-md5")
            content_left = content_left is not None and int(content_left)
            if content_md5 is not None:
                content_hasher = hashlib.md5()
                log.debug("x-content-md5: %s", content_md5)

            with open(localpath, "wb") as fb:
                # for block in response.iter_content(chunk_size = 16 * 1024 * 1024): #16MB
                while True:
                    block = response.raw.read(16 * 1024 * 1024, decode_content=True)
                    if block:
                        if content_left is not None:
                            content_left -= 16 * 1024 * 1024
                        if content_md5:
                            content_hasher.update(block)
                        fb.write(block)
                    else:
                        break
                fb.flush()
        # content-left can be < 0 when accept-encoding is a compressed type: gzip, deflate
        if original_length is not None and content_left > 0:
            raise BQApiError(response)
        if content_md5 is not None and content_md5 != content_hasher.hexdigest():
            raise BQApiError(response)

        return response


class FuturizedServiceProxy(BaseServiceProxy):
    future_wait = True

    def __call__(self, future_wait=True):
        svc = super().__call__()
        svc.future_wait = future_wait
        return svc

    def _wait_for_future(self, future_id: str, retry_time: int = 5) -> Metadoc:
        future_service = self.session.service("futures")
        try:
            future_state = "PENDING"
            while future_state in ("PENDING", "PROCESSING"):
                time.sleep(retry_time)
                future_state = future_service.get_state(future_id)
                log.debug("Future wait %ss", retry_time)
            return future_service.get_result(future_id)
        finally:  # because get_result could throw an exception!
            # try:
            #    future_service.delete(future_id)
            # except FutureNotFoundError:
            # already deleted
            pass

    def _reraise_exception(self, response):
        exc = response.headers.get("x-viqi-exception")
        if exc is not None:
            # exception was returned... re-raise it
            code_to_exception(response)

    def _ensure_future_result(self, response, method="get", render=None, **kw):
        fut = response.headers.get("x-viqi-future")
        if fut is not None:
            # future was returned => wait for result
            retry_time = int(response.headers.get("Retry-After", 5))
            res = self._wait_for_future(fut, retry_time)
            # replace the original future response with a new response with OK code and result doc
            # TODO: how to do this properly?
            response = FutureResponse(200, res)

        else:
            while response.status_code == http_code_future_not_ready:  # could also be one of the retry-futures (321)
                retry_time = int(response.headers.get("Retry-After", 5))
                retry_url_toks = urllib.parse.urlparse(response.headers.get("Location"))
                time.sleep(retry_time)
                path_without_service = "/".join(retry_url_toks.path.strip("/").split("/")[1:])  # assume same service
                response = self.request(
                    path=path_without_service,
                    params=dict(urllib.parse.parse_qsl(retry_url_toks.query, keep_blank_values=True)),
                    method=method,
                    render=render,
                    future_wait=False,
                    **kw,
                )

        return response

    def _render_response(self, res: requests.Response, render: str | None = None) -> Metadoc | requests.Response | str:
        """Render results as requested
        Args:
          res: A Response object
          render: doc|json|None
        Returns:
          a metadoc or
        """

        if res is None:
            return res
        if render == "doc":
            return res.doc()
        elif render == "etree":
            log.warn("use of render=etree deprecated")
            return Metadoc.convert_back(res.doc())
        elif render == "json":
            return custom_json_loads(res.text)
        else:
            return res

    def request(
        self,
        path: str = None,
        params: dict = None,
        method: str = "get",
        render: str = None,
        future_wait: bool | None = None,
        **kw,
    ):
        """
        Generic future-handling REST-type request to the service (should not be called, use service specific functions instead).

        Args:
            path: a path relative to service (maybe a string or list)
            params: a dictionary of value to encode as params
            method: request type (get, put, post, etc)
            render: 'doc'/'etree'/'xml' to request doc response, 'json' for JSON response
            future_wait: if true, wait for result in case future came back; if false, return even if future doc

        Returns:
            a request.response (INDEPENDENT OF render!)
        """
        # enable redirects again; futures use code 321 which is not affected by requests redirect handling
        #         kw["allow_redirects"] = kw.get(
        #             "allow_redirects", False
        #         )  # turn off redirects by default as it will interfere with future handling
        response = super().request(path=path, params=params, method=method, render=render, **kw)

        # handle two special cases: (1) exception came back, (2) future came back
        self._reraise_exception(response)

        if future_wait is None:
            future_wait = self.future_wait
        if future_wait:
            response = self._ensure_future_result(response, method=method, render=render, **kw)

        return response
