import json
import logging
import os
import pickle
import tempfile
from pathlib import Path

from pyjsonq import JsonQ


data_path = "/data/data.json"


def get_qe():
    r = JsonQ()
    r._json_data = json.loads(Path(data_path).read_text())
    return r

def update_qe(qe: JsonQ):
    qe._json_data = json.loads(Path(data_path).read_text())

class MoonlinkPacket:
    def __str__(self):
        return f"<{self.__class__}>"

    def dump(self):
        return pickle.dumps(self, fix_imports=False)


class MoonlinkRequest(MoonlinkPacket):
    pass


class MoonlinkPingRequest(MoonlinkRequest):
    data = None

    def __init__(self, _data=None):
        self.data = _data.strip() if _data else None

    def __str__(self):
        return f"<MoonlinkRequest [PING]: {self.data or 'None'}>"

    def process(self):
        return MoonlinkPingResponse(self.data)


class MoonlinkAuthenticateRequest(MoonlinkRequest):
    username = None
    password = None

    def __init__(self, _username, _password):
        self.username = _username
        self.password = _password

    def __str__(self):
        return f"<MoonlinkRequest [AUTHENTICATE]: {self.username}>"

    def process(self):
        return MoonlinkAuthenticateResponse(self.username, self.password)


class MoonlinkUserRequest(MoonlinkRequest):
    token = None
    name = None
    query = None
    path = "users"

    def __init__(self, _name, _token):
        self.name = _name
        self.token = _token
        self.query = JsonQ().where('name', '=', _name)

    def __str__(self):
        return f"<MoonlinkRequest [USER]: {self.name} token: {self.token}>"

    def process(self):
        return MoonlinkUserResponse(token=self.token, path=self.path, qe=self.query)


class MoonlinkSatelliteRequest(MoonlinkRequest):
    path = "status"

    def __str__(self):
        return f"<MoonlinkRequest [SATELLITE]>"

    def process(self):
        return MoonlinkSatelliteResponse(path=self.path)



class MoonlinkStatusRequest(MoonlinkRequest):
    token = None
    name = None
    query = None
    path = "status"

    def __init__(self, _name, _token):
        self.name = _name
        self.token = _token
        self.query = JsonQ().where('name', '=', _name)

    def __str__(self):
        return f"<MoonlinkRequest [STATUS]: {self.name} token: {self.token}>"

    def process(self):
        return MoonlinkStatusResponse(token=self.token, path=self.path, qe=self.query)


class MoonlinkExportRequest(MoonlinkRequest):
    key = None
    op = None
    threshold = None
    field = None

    def __init__(self, _key, _op, _threshold):
        self.key = _key
        self.op = _op
        self.threshold = _threshold


class MoonlinkUserExportRequest(MoonlinkExportRequest):
    field = "name"

    def __str__(self):
        return f"<MoonlinkUserRequest [USER EXPORT]: {self.key} {self.op} {self.threshold}>"

    def process(self):
        return MoonlinkUserExportResponse(key=self.key, op=self.op, threshold=self.threshold, field=self.field).process()


class MoonlinkSatelliteExportRequest(MoonlinkExportRequest):
    key = None
    op = None
    threshold = None
    field = "name"

    def __str__(self):
        return f"<MoonlinkUserRequest [SATELLITE EXPORT]: {self.key} {self.op} {self.threshold}>"

    def process(self):
        return MoonlinkSatelliteExportResponse(key=self.key, op=self.op, threshold=self.threshold, field=self.field).process()


class MoonlinkFetchExportRequest(MoonlinkRequest):
    file_path = None

    def __init__(self, _file_path):
        self.file_path = _file_path

    def __str__(self):
        return f"<MoonlinkUserRequest [FETCH EXPORT]: {self.file_path}>"

    def process(self):
        return MoonlinkFetchExportResponse(file_path=self.file_path)


class MoonlinkResponse(MoonlinkPacket):
    pass


class MoonlinkAuthenticatedResponse(MoonlinkPacket):
    def check_token(self, token):
        username = b''
        for i, c in enumerate(token):
            username += (c + username[i-1] % 10).to_bytes(1, 'big') if i else c.to_bytes(1, 'big')
        username = username.decode()[32:][::-1]
        return username

    def __init__(self, *args, token=None, **kwargs):
        if not token:
            raise ValueError("No auth token given")
        try:
            username = self.check_token(token)
        except Exception:
            raise ValueError("Authentication failed")

        qe = get_qe()
        if qe.at("management").where("username", "=", username).get():
            logging.debug(f"User {username} request authenticated")
        else:
            raise ValueError("Authentication failed")


class MoonlinkPingResponse(MoonlinkResponse):
    data = None

    def __init__(self, _data=None):
        self.data = _data

    def __str__(self):
        return f"<MoonlinkResponse [PONG]: {self.data}>"


class MoonlinkAuthenticateResponse(MoonlinkResponse):
    state_ok = 'OK'
    state_failure = 'FAILURE'

    status = state_failure
    token = None

    def __init__(self, username, password):
        qe = get_qe()
        if qe.at("management").where("username", "=", username).where("password", "=", password).get():
            self.status = self.state_ok
            token = f"Q2OqwwFOlZmkFrqNx0vmnK1HU5kqt9ri{username[::-1]}".encode()
            self.token = bytes([c - token[i - 1] % 10 if i else c for i, c in enumerate(token)])

    def __str__(self):
        if self.token:
            return f"<MoonlinkResponse [AUTHENTICATE]: {self.status}, token: {self.token}>"
        return f"<MoonlinkResponse [AUTHENTICATE]: {self.status}>"


class MoonlinkUserResponse(MoonlinkAuthenticatedResponse):
    user_data = None

    def __init__(self, token, path, qe: JsonQ):
        super().__init__(token=token)

        update_qe(qe)
        try:
            self.user_data = qe.at(path).get()
        except Exception:
            pass

    def __str__(self):
        return f"<MoonlinkResponse [USER]: {self.user_data}>"


class MoonlinkSatelliteResponse(MoonlinkResponse):
    sat_list = None

    def __init__(self, path):
        qe = get_qe()
        self.sat_list = sorted([s['name'] for s in qe.at(path).get()])

    def __str__(self):
        return "<MoonlinkResponse [SATELLITE]: {}>".format('\n'.join(self.sat_list))


class MoonlinkStatusResponse(MoonlinkAuthenticatedResponse):
    sat_data = None

    def __init__(self, token, path, qe):
        authenticated = False
        try:
            self.check_token(token)
            authenticated = True
        except Exception:  # noqa
            pass

        update_qe(qe)
        try:
            self.sat_data = qe.at(path).get()

            if authenticated:
                qe = get_qe()
                user_data = qe.at("users").where("satellite", "=", self.sat_data[0]['id']).get()
                self.sat_data[0]['users'] = sorted([u['name'] for u in user_data])
        except Exception:
            pass

    def __str__(self):
        return f"<MoonlinkResponse [STATUS]: {self.sat_data}>"


class MoonlinkExportResponse(MoonlinkResponse):
    export_path = None
    data_set = None
    key = None
    op = None
    threshold = None
    field = None

    def __init__(self, key, op, threshold, field):
        self.key = key
        self.op = op
        self.threshold = threshold
        self.field = field

    def process(self):
        qe = get_qe()
        try:
            result = qe.at(self.data_set).where(self.key, self.op, int(self.threshold)).get()
            result = sorted([o[self.field] for o in result])
        except Exception:
            pass
        else:
            with tempfile.NamedTemporaryFile(delete=False, dir='/tmp/moonlink/') as f:
                f.write(', '.join(result).encode('utf-8'))
                self.export_path = os.path.basename(f.name)
                logging.info(f"{len(result)} {self.data_set} exported to {f.name}")

        return self


class MoonlinkUserExportResponse(MoonlinkExportResponse):
    data_set = 'users'
    export_path = None
    allowed_keys = ['id', 'accuracy', 'satellite']

    def __str__(self):
        if not self.export_path:
            return f"<MoonlinResponse [USER EXPORT]: FAILED>"
        return f"<MoonlinResponse [USER EXPORT]: {self.export_path}'>"


class MoonlinkSatelliteExportResponse(MoonlinkExportResponse):
    data_set = 'status'
    export_path = None
    allowed_keys = ['id', 'APO', 'PER', 'ANG', 'VEL', 'ALT', 'LAT', 'LON']

    def __str__(self):
        if not self.export_path:
            return f"<MoonlinResponse [SATELLITE EXPORT]: FAILED>"
        return f"<MoonlinResponse [SATELLITE EXPORT]: {self.export_path}'>"


class MoonlinkFetchExportResponse(MoonlinkResponse):
    file = None
    file_path = None

    def __init__(self, file_path):
        # Do not allow the user to fetch files outside our tmp dir.
        # Dion: path traversal error was here
        base_dir = '/tmp/moonlink/'
        abs_base_dir = os.path.abspath(base_dir)
        full_path = os.path.abspath(os.path.join(base_dir, file_path))
        
        if not full_path.startswith(abs_base_dir):
            raise ValueError("Invalid file path")

        self.file_path = full_path

        # self.file_path = os.path.normpath(os.path.join('/tmp/moonlink/', file_path))
        try:
            with open(self.file_path, mode='r') as f:
                self.file = f.read()
        except Exception:
            pass

    def __str__(self):
        if not self.file:
            return f"<MoonlinResponse [FETCH EXPORT]: FAILED>"
        return f"<MoonlinResponse [FETCH EXPORT]: {self.file_path}'>"
