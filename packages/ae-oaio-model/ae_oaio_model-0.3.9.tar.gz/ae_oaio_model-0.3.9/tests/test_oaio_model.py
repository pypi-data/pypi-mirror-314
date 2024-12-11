""" oaio client unit and integration tests.

"""
import datetime

from ae.base import defuse
from ae.oaio_model import (                             # type: ignore
    HTTP_HEADER_APP_ID, HTTP_HEADER_DVC_ID, HTTP_HEADER_USR_ID, NAME_VALUES_KEY,
    OLDEST_SYNC_STAMP, FILES_VALUES_KEY, ROOT_VALUES_KEY, STAMP_FORMAT,
    OaiObject, extra_headers, now_stamp, object_dict, object_id, stamp_diff)


class TestHelpers:
    def test_extra_headers(self):
        hdr = extra_headers('u_nam', 'device_i', 'id_of_app')
        assert HTTP_HEADER_USR_ID in hdr
        assert hdr[HTTP_HEADER_USR_ID] == 'u_nam'
        assert HTTP_HEADER_DVC_ID in hdr
        assert hdr[HTTP_HEADER_DVC_ID] == 'device_i'
        assert HTTP_HEADER_APP_ID in hdr
        assert hdr[HTTP_HEADER_APP_ID] == 'id_of_app'

    def test_object_dict(self):
        oai_obj = OaiObject("my_id")
        oaio_dict = object_dict(oai_obj)
        assert 'oaio_id' in oaio_dict
        assert oaio_dict['oaio_id'] == "my_id"

    def test_object_id_main_ids(self):
        assert 'uid' in object_id('uid', 'did', 'aid', 'sid', {})
        assert 'did' in object_id('uid', 'did', 'aid', 'sid', {})
        assert 'aid' in object_id('uid', 'did', 'aid', 'sid', {})
        assert 'sid' in object_id('uid', 'did', 'aid', 'sid', {})

    def test_object_id_values_name(self):
        name = 'name_id'
        values = {NAME_VALUES_KEY: name}
        assert name in object_id('uid', 'did', 'aid', 'sid', values)

    def test_object_id_values_name_with_defused_char(self):
        name = 'test name of the object'
        values = {NAME_VALUES_KEY: name}
        assert defuse(name) in object_id('uid', 'did', 'aid', 'sid', values)

    def test_object_id_values_root_path(self):
        root_path = 'root_path'
        values = {ROOT_VALUES_KEY: root_path + "/"}
        assert root_path in object_id('uid', 'did', 'aid', 'sid', values)

    def test_object_id_values_single_file_name(self):
        file_name = 'file_one.xyz'

        values = {FILES_VALUES_KEY: [file_name]}
        assert defuse(file_name) in object_id('uid', 'did', 'aid', 'sid', values)

        values = {FILES_VALUES_KEY: [file_name, 'anyOtherFile.name']}
        assert file_name not in object_id('uid', 'did', 'aid', 'sid', values)

    def test_object_id_values_single_file_name_with_defused_char(self):
        file_name = 'file one{with_var}.xyz'

        values = {FILES_VALUES_KEY: [file_name]}
        assert defuse(file_name) in object_id('uid', 'did', 'aid', 'sid', values)

    def test_stamp_diff_zero(self):
        stamp = now_stamp()
        assert stamp_diff(stamp, stamp) == 0.0

    def test_stamp_diff(self):
        d1 = datetime.datetime(year=2022, month=3, day=12, hour=9, minute=42, second=24, microsecond=33)
        d2 = datetime.datetime(year=2022, month=3, day=12, hour=9, minute=42, second=36, microsecond=69)
        assert d2 - d1 == datetime.timedelta(seconds=12, microseconds=36)

        s1 = d1.strftime(STAMP_FORMAT)
        s2 = d2.strftime(STAMP_FORMAT)
        assert stamp_diff(s1, s2) == datetime.timedelta(seconds=12, microseconds=36).total_seconds()
        assert stamp_diff(s1, s2) == 12.000036

    def test_stamp_oldest_and_defaults(self):
        assert OLDEST_SYNC_STAMP < now_stamp()
        assert "" < OLDEST_SYNC_STAMP           # "" is default for OaiObject.client_stamp and .server_stamp fields
        assert "" < now_stamp()


class TestOaiObject:
    def test_instantiation(self):
        oai_obj = OaiObject(oaio_id='id', csh_id='cid', client_stamp='stamp')
        assert oai_obj
        assert oai_obj.oaio_id == 'id'
        assert oai_obj.csh_id == 'cid'
        assert oai_obj.client_stamp == 'stamp'
