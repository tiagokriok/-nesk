from __future__ import annotations

import json
import urllib.request
from typing import Any
from typing import Dict
from typing import MutableMapping
from typing import Optional
from typing import Union

from nesk.core.NeskError import HTTPError
from nesk.core.NeskError import JSONDecodeError
from nesk.core.NeskError import NeskException
from nesk.core.NeskError import URLError


class Nesk:

    def __init__(
        self,
        base_url: Optional[str] = None,
        headers: Optional[MutableMapping[str, str]] = None
    ) -> None:
        self.base_url = base_url or ""
        self.headers = headers or {
            "Content-Type": "application/json"
        }

    def __request(
        self,
        method: str,
        url: str,
        headers: Optional[MutableMapping[str, str]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Union[Dict[str, Any], Dict]:
        try:
            if self.base_url.endswith("/"):
                base_url = self.base_url + url.lstrip("/")
            else:
                base_url = self.base_url + "/" + url.lstrip("/")

            new_headers: MutableMapping[str, str] = dict(
                self.headers)

            if headers:
                new_headers.update(headers)

            request = urllib.request.Request(
                base_url,
                method=method,
                headers=new_headers,
                data=json.dumps(data).encode("utf-8") if data else None
            )

            with urllib.request.urlopen(request) as response:
                response_data = response.read().decode("utf-8")
                return json.loads(response_data) if response_data else dict()

        except urllib.error.HTTPError as e:
            raise HTTPError(e.code, e.reason)

        except urllib.error.URLError as e:
            raise URLError(str(e.reason))

        except json.JSONDecodeError as e:
            raise JSONDecodeError(e)

        except Exception as e:
            raise NeskException(str(e))

    def get(
        self,
        url: str,
        headers: Optional[MutableMapping[str, str]] = None
    ) -> Union[Dict[str, Any], Dict]:
        return self.__request("GET", url, headers)

    def post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[MutableMapping[str, str]] = None
    ) -> Union[Dict[str, Any], Dict]:
        return self.__request("POST", url, headers, data)

    def put(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[MutableMapping[str, str]] = None
    ) -> Union[Dict[str, Any], Dict]:
        return self.__request("PUT", url, headers, data)

    def patch(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[MutableMapping[str, str]] = None
    ) -> Union[Dict[str, Any], Dict]:
        return self.__request("PATCH", url, headers, data)

    def delete(
        self,
        url: str,
        headers: Optional[MutableMapping[str, str]] = None
    ) -> Union[Dict[str, Any], Dict]:
        return self.__request("DELETE", url, headers)

    def head(
        self,
        url: str,
        headers: Optional[MutableMapping[str, str]] = None
    ) -> Union[Dict[str, Any], Dict]:
        return self.__request("HEAD", url, headers)

    def options(
        self,
        url: str,
        headers: Optional[MutableMapping[str, str]] = None
    ) -> Union[Dict[str, Any], Dict]:
        return self.__request("OPTIONS", url, headers)
