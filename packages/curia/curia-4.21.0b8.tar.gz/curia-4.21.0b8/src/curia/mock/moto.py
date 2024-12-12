import functools
import json
import os
import time
import traceback
from base64 import b64encode
from datetime import datetime
from multiprocessing import Pipe
from multiprocessing.context import Process
from typing import Dict, Optional
from urllib.parse import urlparse

import moto.s3.responses
from curia.mock.s3 import _create_seed_s3_data
from moto.server import DomainDispatcherApplication, create_backend_app
from werkzeug import run_simple

from curia.utils.s3 import AWSIoContext


class MotoServerFailedException(Exception):
    pass


class ExceptionSafeProcess(Process):
    """
    A process subclass that catches exceptions and stores them in a property.
    """
    def __init__(self, *args, **kwargs):
        Process.__init__(self, *args, **kwargs)
        self._pconn, self._cconn = Pipe()
        self._exception = None

    def run(self):
        try:
            Process.run(self)
            self._cconn.send(None)
        except Exception as e:
            tb = traceback.format_exc()
            self._cconn.send((str(e), tb))

    @property
    def exception(self):
        if self._pconn.poll():
            self._exception = self._pconn.recv()
        return self._exception


def _wrap_subdomain_based_buckets(subdomain_based_buckets):
    """
    Decorator that enables moto3 to correctly identify host.docker.internal as being a path similar to localhost.
    This is necessary because the requests coming from a docker container are not recognized as localhost.
    """
    @functools.wraps(subdomain_based_buckets)
    def wrapper(self, request):
        host = request.headers.get("host", request.headers.get("Host"))
        if not host:
            host = urlparse(request.url).netloc
        if host.startswith("host.docker.internal"):
            return False
        return subdomain_based_buckets(self, request)

    return wrapper


# patch moto with decorator
moto.s3.responses.S3Response.subdomain_based_buckets = \
    _wrap_subdomain_based_buckets(moto.s3.responses.S3Response.subdomain_based_buckets)


def _patch_ecr_docker_creds(mock_ecr_docker_registry_credentials: Dict[str, str]):
    def wrapper_fn(fn):
        @functools.wraps(fn)
        def patch_fn(*args, **kwargs): # pylint: disable=unused-argument
            token_text = (f'{mock_ecr_docker_registry_credentials["username"]}:'
                          f'{mock_ecr_docker_registry_credentials["password"]}')
            return json.dumps({"authorizationData": [{
                'authorizationToken': b64encode(
                    token_text.encode("ascii")
                ).decode(),
                'expiresAt': time.mktime(datetime(2015, 1, 1).timetuple()),
                "proxyEndpoint": f"https://{mock_ecr_docker_registry_credentials['host']}",
            }]})
        return patch_fn
    return wrapper_fn


def run_moto_server(port=5000, ecr_docker_registry_credentials: Optional[Dict[str, str]] = None):
    """
    Run a moto server in a separate process.
    """
    if ecr_docker_registry_credentials:
        import moto.ecr.responses  # pylint: disable=import-outside-toplevel,redefined-outer-name
        moto.ecr.responses.ECRResponse.get_authorization_token = (
            _patch_ecr_docker_creds(ecr_docker_registry_credentials)(moto.ecr.responses.ECRResponse.get_authorization_token)
        )
    # EK:
    # Python has a notorious unsolved bug when spinning up a process that uses UrlLib in another thread. In particular,
    # system frameworks using UrlLib make calls to libdispatch to query the system configuration for network proxies.
    # libdispatch is not thread-safe, so this leads to a segfault when used in a separate process.
    # Since this is a test server that does not need any network proxies, we disable it here.
    # See these two python bug threads for more info: https://bugs.python.org/issue30385
    # https://bugs.python.org/issue39853
    os.environ["no_proxy"] = "*"
    main_app = DomainDispatcherApplication(create_backend_app)
    main_app.debug = False
    run_simple(
        hostname="127.0.0.1",
        port=port,
        application=main_app,
        threaded=False,
        use_reloader=False,
        ssl_context=None
    )


def using_moto_server(port=5000,
                      seed_s3_data: Dict[str, dict] = None,
                      ecr_docker_registry_credentials: Dict[str, str] = None) -> callable:
    """
    Decorator that starts a moto server in a separate process and kills it after the decorated function has finished.
    """
    def wrap(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            moto_kwargs = {'port': port}
            if ecr_docker_registry_credentials:
                moto_kwargs['ecr_docker_registry_credentials'] = ecr_docker_registry_credentials
            server = ExceptionSafeProcess(
                target=run_moto_server,
                kwargs=moto_kwargs,
                daemon=True
            )
            server.start()
            try:
                with AWSIoContext(
                    aws_access_key_id="dummy",
                    aws_secret_access_key="dummy",
                    aws_region="us-east-1",
                    aws_endpoint_url=f"http://localhost:{port}/",
                ):
                    if seed_s3_data:
                        _create_seed_s3_data(seed_s3_data)
                    res = fn(*args, **kwargs)
            finally:
                exception = server.exception
                server.terminate()
                server.join()
                if exception:
                    error, tb = exception
                    raise MotoServerFailedException(
                        f"Moto server failed to start with: {error}.\n Traceback: \n#####{tb}\n#####\n\n"
                    )
            return res

        return wrapper

    return wrap


if __name__ == "__main__":
    run_moto_server()