
from __future__ import absolute_import

import six

if six.PY3:
    from builtins import input
    from builtins import object


__version__ = '0.7.0' #TODO: This is duplicated in the build.  Need to figure how to set this once 

import sys as _sys
import json as _json
import getpass

_msg = None

try:
    from link import lnk as _lnk
    _msg = _lnk.msg
except:
    print("problem loading link, this is ok on the install")

from ._decorators import raw_response_retry

_API = None
_ACCOUNT = None
_DEFAULT_BASE_URL = "https://video.springserve.com/api/v0"


def setup_config():
    """
    This is used the first time you run it to set up your configuration if
    you want to do that over the command prompt
    """
    current_file = _lnk.config_file()
    current_config = _lnk.config() or {}

    if current_config.get('springserve'):
        print("already configured, remove or edit springserve section from {}".format(current_file))

        confirm = input('Would you like overwrite[Y/n] ')
        if not confirm or confirm.upper() != 'Y':
            print("thanks")
            return

    user = input('Enter a user name: ')
    password = getpass.getpass('Enter password: ')

    current_config['springserve'] = {
        '__default__': {
            'base_url': _DEFAULT_BASE_URL,
            'user': user,
            'password': password,
            'wrapper': "SpringServeAPI"
        }
    }

    confirm = input('Would you like write[Y/n] ')
    if not confirm or confirm.upper() != 'Y':
        print("thanks")
        return

    print("writing config to: {}".format(current_file))
    with open(current_file, 'w') as f:
        f.write(_json.dumps(current_config, indent=4))

    print("done: refreshing config")
    _lnk.fresh()


def API(reauth=False):
    """
    Get the raw API object.  This is rarely used directly by a client of this
    library, but it used as an internal function
    """
    global _API, _ACCOUNT

    if _API is None or reauth:
        _msg.debug("authenticating to springserve")
        try:
            if _ACCOUNT:
                _API = _lnk("springserve.{}".format(_ACCOUNT))
            else:
                try:
                    _API = _lnk("springserve.{}".format("__default__"))
                except:
                    # this is to keep backwards compatiblity
                    _API = _lnk.springserve
            _API.headers.update({'springserve-sdk': __version__})
        except Exception as e:
            raise Exception("""Error authenticating: check your link.config to
                            make sure your username, password and url are
                            correct""")
    return _API


def switch_account(account_name="__default__"):
    global _ACCOUNT
    _ACCOUNT = account_name
    API(True)


class _TabComplete(object):
    """
    this class exists to make any other class
    have a tab completion function that is already
    hooked into ipython
    """
    def _tab_completions(self):
        return []


class _VDAPIResponse(_TabComplete):

    def __init__(self, service, api_response_data, path_params, query_params,
                 ok, payload='', injected_account_id=None):
        super(_VDAPIResponse, self).__init__()
        self._service = service
        self._raw_response = api_response_data
        self._path_params = path_params
        self._query_params = query_params or {}
        self._ok = ok
        self._payload = payload
        self._injected_account_id = injected_account_id

    @property
    def ok(self):
        """
        Tells you if the api response was "ok"

        meaning that it responded with a 200.  If there was an error, this will
        return false

        """
        return self._ok

    @property
    def raw(self):
        """
        Gives you the raw json response from the api.  Usually you do not need
        to call this
        """
        return self._raw_response

    def __getitem__(self, key):

        if isinstance(key, str):
            return self.raw[key]
        elif isinstance(key, int):
            return self.raw[key]

    def __getattr__(self, key):
        """
        This is where the magic happens that allows you to treat this as an
        object that has all of the fields that the api returns.  I seperate all
        of the returned data in self._data
        """
        # if it's not there then try to get it as an attribute
        try:
            return self.__getattribute__(key)
        except AttributeError as e:
            # makes unpickling work?
            if key.startswith("__"):
                raise e
            return self._raw_response[key]

    def _tab_completions(self):

        if not self.raw:
            return []

        return list(self.raw.keys())


class _VDAPISingleResponse(_VDAPIResponse):

    def __init__(self, service, api_response_data, path_params, query_params,
                 ok, payload='', injected_account_id=None):
        self._dirty = {}
        super(_VDAPISingleResponse, self).__init__(service, api_response_data,
                                                   path_params, query_params,
                                                   ok, payload,
                                                   injected_account_id)

    def set_dirty(self, field):
        """
        you need this for nested fields that you have changed
        but didn't actually set
        """
        self._dirty[field] = self._raw_response[field]

    def save(self, dirty_only=False, **kwargs):
        """
        Save this object back to the api after making changes.  As an example::

            tag = springserve.supply_tags.get(1)
            tag.name = "This is my new name"
            # this will print if the save went through correctly
            print tag.save().ok

        Returns:

            An API response object
        """
        # if they have dirty fields only send those

        payload = self.raw

        if dirty_only:
            payload = self._dirty

        try:
            account_id = self.account_id
        except Exception as e:
            if self._injected_account_id:
                account_id = self._injected_account_id
            else:
                raise e

        return self._service.put(self.id, payload, account_id=account_id, **kwargs)

    def duplicate(self, **kwargs):

        payload = self.raw.copy()
        payload.update(kwargs)
        return self._service.new(payload, account_id=self.account_id)

    def __setattr__(self, attr, value):
        """
        If it's a property that was already defined when the class
        was initialized that let it exist.  If it's new than let's slap it into
        _data.  This allows us to set new attributes and save it back to the api
        """
        # allows you to add any private field in the init
        # I could do something else here but I think it makes
        # sense to enforce private variables in the ConsoleObject
        if attr.startswith('_'):
            self.__dict__[attr] = value

        if attr in self.__dict__:
            self.__dict__[attr] = value
        else:
            # TODO - this is the only place where appnexus object fields get changed?
            self._raw_response[attr] = value
            self._dirty[attr] = value


class _VDAPIMultiResponse(_VDAPIResponse):

    def __init__(self, service, api_response_data, path_params, query_params,
                 response_object, ok, payload='', injected_account_id=None):

        super(_VDAPIMultiResponse, self).__init__(service, api_response_data,
                                                  path_params, query_params, ok, payload)
        self._payload = payload
        self._object_cache = []
        self._current_page = 1
        self._all_pages_gotten = False
        self._injected_account_id = injected_account_id
        self.response_object = response_object
        # build out the initial set of objects
        self._build_cache(self.raw)

    def _build_cache(self, objects):
        self._object_cache.extend([self._build_response_object(x) for x in
                                   objects])

    def _is_last_page(self, resp):
        return (not resp or not resp.json)

    def _get_next_page(self):

        if self._all_pages_gotten:
            return

        params = self._query_params.copy()
        params['page'] = self._current_page+1
        resp = self._service.get_raw(self._path_params, **params)

        # this means we are donesky, we don't know
        # how many items there will be, only that we hit the last page
        if self._is_last_page(resp):
            self._all_pages_gotten = True
            return

        self._build_cache(resp.json)
        self._current_page += 1

    def _build_response_object(self, data):
        return self.response_object(self._service, data,
                                    self._path_params,
                                    self._query_params,
                                    True,
                                    payload='',
                                    injected_account_id=self._injected_account_id)

    def __getitem__(self, key):

        if not isinstance(key, int):
            raise Exception("Must be an index ")
        if key >= len(self._object_cache):
            if self._all_pages_gotten:
                raise IndexError("All pages gotten, no such object")
            self._get_next_page()
            return self[key]
        return self._object_cache[key]

    def __iter__(self):
        """
        this will automatically take care of pagination for us.
        """
        idx = 0
        while True:
            # not sure I love this method, but it's the best
            # one I can think of right now
            try:
                yield self[idx]
                idx += 1
            except IndexError as e:
                break

    def __len__(self):
        return len([x for x in self])


def _format_url(endpoint, path_param):

    _url = endpoint

    if path_param:
        _url += "/{}".format(path_param)

    return _url


def _format_params(params):

    _params = {}

    for key, value in params.items():
        if isinstance(value, list):
            # make sure any list has the [] on it
            key = "{}[]".format(key.lstrip("[]"))
        _params[key] = value

    return _params


class _VDDuplicateableResponse(_VDAPISingleResponse):

    def duplicate(self, **kwargs):
        return self._service.get("{}/duplicate".format(self.id), account_id=self.account_id)


class VDAuthError(Exception):
    pass


class _VDAPIService(object):

    __API__ = None
    __RESPONSE_OBJECT__ = _VDAPISingleResponse
    __RESPONSES_OBJECT__ = _VDAPIMultiResponse

    def __init__(self):
        self.account_id = None

    @property
    def endpoint(self):
        """
        The api endpoint that is used for this service.  For example::

            In [1]: import springserve

            In [2]: springserve.supply_tags.endpoint
            Out[2]: '/supply_tags'

        """
        return "/" + self.__API__

    def build_response(self, api_response, path_params, query_params, payload=''):
        is_ok = api_response.ok

        if not is_ok and api_response.status_code == 401:
            raise VDAuthError("Need to Re-Auth")

        if api_response.status_code == 204:  # this means empty
            resp_json = {}
        else:
            try: 
                resp_json = api_response.json
            except:
                resp_json = {"error": "error parsing json response"} 

        if isinstance(resp_json, list):
            # wrap it in a multi container
            return self.__RESPONSES_OBJECT__(self, resp_json, path_params,
                                             query_params, self.__RESPONSE_OBJECT__,
                                             is_ok, payload, self.account_id)

        return self.__RESPONSE_OBJECT__(self, resp_json, path_params,
                                        query_params, is_ok, payload,
                                        self.account_id)

    @raw_response_retry
    def get_raw(self, path_param=None, reauth=False, **query_params):
        """
        Get the raw http response for this object.  This is rarely used by a
        client unless they want to inspect the raw http fields
        """
        params = _format_params(query_params)
        return API(reauth=reauth).get(_format_url(self.endpoint, path_param),
                                      params=params)

    def get(self, path_param=None, reauth=False, **query_params):
        """
        Make a get request to this api service.  Allows you to pass in arbitrary
        query paramaters.

        Examples::

            # get all supply_tags
            tags = springserve.supply_tags.get()

            for tag in tags:
                print tag.id, tag.name

            # get one supply tag
            tag = springserve.supply_tag.get(1)
            print tag.id, tag.name

            # get by many ids
            tags = springserve.supply_tags.get(ids=[1,2,3])

            # get users that are account_contacts (ie, using query string # params)
            users = springserve.users.get(account_contact=True)

        """
        global API
        try:
            return self.build_response(
                self.get_raw(path_param, reauth=reauth, **query_params),
                path_param,
                query_params
            )
        except VDAuthError as e:
            # we only retry if we are redo'n on an auto reauth
            if not reauth:
                _msg.info("Reauthing and then retry")
                return self.get(path_param, reauth=True, **query_params)
            raise e

    @raw_response_retry
    def _put_raw(self, path_param, data, reauth=False, **query_params):
        params = _format_params(query_params)
        return API(reauth=reauth).put(
                    _format_url(self.endpoint, path_param),
                    params=params,
                    data=_json.dumps(data)
                    )

    def put(self, path_param, data, reauth=False, **query_params):
        global API

        try:
            return self.build_response(
                    self._put_raw(path_param, data, reauth=reauth, **query_params),
                    path_param,
                    query_params,
                    payload=data
            )
        except VDAuthError as e:
            # we only retry if we are redo'n on an auto reauth
            if not reauth:
                _msg.info("Reauthing and then retry")
                return self.put(path_param, data, reauth=True, **query_params)
            raise e

    @raw_response_retry
    def _post_raw(self, data, path_param="", reauth=False, **query_params):
        params = _format_params(query_params)
        return API(reauth=reauth).post(
                _format_url(self.endpoint, path_param),
                params=params,
                data=_json.dumps(data)
                )

    def post(self, data, path_param="", reauth=False, **query_params):
        global API
        try:
            return self.build_response(
                self._post_raw(data, path_param, reauth=reauth, **query_params),
                path_param,
                query_params,
                payload=data
            )
        except VDAuthError as e:
            # we only retry if we are redo'n on an auto reauth
            if not reauth:
                _msg.info("Reauthing and then retry")
                return self.new(data, path_param, reauth=True, **query_params)
            # means that we had already tried a reauth and it failed
            raise e

    def delete(self, path_param="", reauth=False, **query_params):
        global API
        try:
            params = _format_params(query_params)
            return self.build_response(
                    API(reauth=reauth).delete(
                        _format_url(self.endpoint, path_param),
                        params=params,
                        ),
                    path_param,
                    query_params
            )
        except VDAuthError as e:
            # we only retry if we are redo'n on an auto reauth
            if not reauth:
                _msg.info("Reauthing and then retry")
                return self.delete(path_param, reauth=True, **query_params)
            # means that we had already tried a reauth and it failed
            raise e

    def bulk_delete(self, data, path_param="", reauth=False, **query_params):
        """
        Delete an object.
        """
        global API
        try:
            params = _format_params(query_params)
            return self.build_response(
                    API(reauth=reauth).delete(
                        _format_url(self.endpoint, path_param),
                        params=params,
                        data=_json.dumps(data)
                        ),
                    path_param,
                    query_params
            )
        except VDAuthError as e:
            # we only retry if we are redo'n on an auto reauth
            if not reauth:
                _msg.info("Reauthing and then retry")
                return self.delete(data, path_param, reauth=True, **query_params)
            # means that we had already tried a reauth and it failed
            raise e

    def new(self, data, path_param="", reauth=False, **query_params):
        """
        Create a new object.  You need to pass in the required fields as a
        dictionary.  For instance::

            resp = springserve.domain_lists.new({'name':'My Domain List'})
            print resp.ok
        """
        return self.post(data, path_param, reauth, **query_params)


from ._supply import _SupplyTagAPI, _SupplyPartnerAPI, _SupplyLabelAPI, _ConnectedSupplyAPI
from ._demand import _DemandTagAPI, _DemandPartnerAPI, _DemandLabelAPI, _ConnectedDemandAPI, _CampaignAPI
from ._common import _DomainListAPI, _BillAPI, _KeyAPI, _AppBundleListAPI, _AppNameListAPI, _DeviceIdListAPI, _IpListAPI
from ._reporting import _ReportingAPI, _TrafficQualityReport
from ._account import _AccountAPI, _UserAPI
from ._direct_connect import _DirectConnectionAPI
from ._object_change_messages import _ObjectChangeMessagesAPI

accounts = _AccountAPI()
app_bundles = _AppBundleListAPI()
app_names = _AppNameListAPI()
device_id_lists = _DeviceIdListAPI()
ip_lists = _IpListAPI()

bills = _BillAPI()

campaigns = _CampaignAPI()
connected_demand = _ConnectedDemandAPI()
connected_supply = _ConnectedSupplyAPI()

demand_labels = _DemandLabelAPI()
demand_tags = _DemandTagAPI()
demand_partners = _DemandPartnerAPI()
direct_connections = _DirectConnectionAPI()

domain_lists = _DomainListAPI()

keys = _KeyAPI()

_object_change_messages = _ObjectChangeMessagesAPI()

reports = _ReportingAPI()
quality_reports = _TrafficQualityReport()

supply_labels = _SupplyLabelAPI()
supply_tags = _SupplyTagAPI()
supply_partners = _SupplyPartnerAPI()

users = _UserAPI()


def raw_get(path_param, **query_params):
    global API
    params = _format_params(query_params)
    return API().get(_format_url("", path_param), params=params).json


def _install_ipython_completers():  # pragma: no cover

    from IPython.utils.generics import complete_object

    @complete_object.when_type(_TabComplete)
    def complete_report_object(obj, prev_completions):
        """
        Add in all the methods of the _wrapped object so its
        visible in iPython as well
        """
        prev_completions += obj._tab_completions()
        return prev_completions


# Importing IPython brings in about 200 modules, so we want to avoid it unless
# we're in IPython (when those modules are loaded anyway).
# Code attributed to Pandas, Thanks Wes
if "IPython" in _sys.modules:  # pragma: no cover
    try:
        _install_ipython_completers()
    except Exception:
        _msg.debug("Error loading tab completers")
        pass
