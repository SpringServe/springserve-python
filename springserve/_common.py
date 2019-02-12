
from . import _VDAPIService, _VDAPIResponse, _VDAPISingleResponse

class _DomainListResponse(_VDAPISingleResponse):
    """
    Override to give you access to the actual domains
    """

    def get_domains(self, **kwargs):
        """
        Get the list of domains that are in this domain list

            d = springserve.domain_list.get(id)
            domains = d.get_domains()

            for domain in domains:
                print domain.name

        """
        return self._service.get("{}/domains".format(self.id), **kwargs)
    
    def _to_list(self, input_list):
        """
        The api needs a list, and you can't serialize sets, or Series
        """
        if isinstance(input_list, list):
            return input_list

        return [x for x in input_list]

    def add_domains(self, domains):
        """
        Add a list of domains to this domain list

            d = springserve.domain_list.get(id)
            d.add_domains(['blah.com', 'blah2.com'])

        domains: List of domains you would like to add 
        """
        payload = {'names':self._to_list(domains)}
        resp = self._service.post(payload,
                                  path_param='{}/domains/bulk_create'.format(self.id)
                                 )
        return resp

    def remove_domains(self, domains):
        """
        Add a list of domains to this domain list

            d = springserve.domain_list.get(id)
            d.remove_domains(['blah.com', 'blah2.com'])

        domains: List of domains you would like to add 
        """
        payload = {'names':self._to_list(domains)}
        resp = self._service.bulk_delete(payload,
                                  path_param='{}/domains/bulk_delete'.format(self.id)
                                 )
        return resp


class _DomainListAPI(_VDAPIService):

    __API__ = "domain_lists"
    __RESPONSE_OBJECT__ = _DomainListResponse


class _AppBundleListResponse(_VDAPISingleResponse):
    """
    Override to give you access to the actual domains
    """

    def get_bundles(self, **kwargs):
        """
        Get the list of domains that are in this domain list

            d = springserve.domain_list.get(id)
            domains = d.get_domains()

            for domain in domains:
                print domain.name

        """
        return self._service.get("{}/app_bundles".format(self.id), **kwargs)
    
    def _to_list(self, input_list):
        """
        The api needs a list, and you can't serialize sets, or Series
        """
        if isinstance(input_list, list):
            return input_list

        return [x for x in input_list]

    def add_bundles(self, bundles):
        """
        Add a list of domains to this domain list

            d = springserve.domain_list.get(id)
            d.add_domains(['blah.com', 'blah2.com'])

        domains: List of domains you would like to add 
        """
        payload = {'app_bundles':self._to_list(bundles)}
        resp = self._service.post(payload,
                                  path_param='{}/app_bundles/bulk_create'.format(self.id)
                                 )
        return resp

    def remove_bundles(self, domains):
        """
        Add a list of domains to this domain list

            d = springserve.domain_list.get(id)
            d.remove_domains(['blah.com', 'blah2.com'])

        domains: List of domains you would like to add 
        """
        payload = {'app_bundles':self._to_list(domains)}
        resp = self._service.bulk_delete(payload,
                                  path_param='{}/app_bundles/bulk_delete'.format(self.id)
                                 )
        return resp


class _AppBundleListAPI(_VDAPIService):

    __API__ = "app_bundle_lists"
    __RESPONSE_OBJECT__ = _AppBundleListResponse

class _AppNameListResponse(_VDAPISingleResponse):
    """
    Override to give you access to the actual domains
    """

    def get_names(self, **kwargs):
        """
        Get the list of domains that are in this domain list

            d = springserve.domain_list.get(id)
            domains = d.get_domains()

            for domain in domains:
                print domain.name

        """
        return self._service.get("{}/app_names".format(self.id), **kwargs)
    
    def _to_list(self, input_list):
        """
        The api needs a list, and you can't serialize sets, or Series
        """
        if isinstance(input_list, list):
            return input_list

        return [x for x in input_list]

    def add_names(self, names):
        """
        Add a list of domains to this domain list

            d = springserve.domain_list.get(id)
            d.add_domains(['blah.com', 'blah2.com'])

        domains: List of domains you would like to add 
        """
        payload = {'app_names':self._to_list(names)}
        resp = self._service.post(payload,
                                  path_param='{}/app_names/bulk_create'.format(self.id)
                                 )
        return resp

    def remove_names(self, domains):
        """
        Add a list of domains to this domain list

            d = springserve.domain_list.get(id)
            d.remove_domains(['blah.com', 'blah2.com'])

        domains: List of domains you would like to add 
        """
        payload = {'app_names':self._to_list(domains)}
        resp = self._service.bulk_delete(payload,
                                  path_param='{}/app_names/bulk_delete'.format(self.id)
                                 )
        return resp


class _AppNameListAPI(_VDAPIService):

    __API__ = "app_name_lists"
    __RESPONSE_OBJECT__ = _AppNameListResponse


class _DeviceIdListResponse(_VDAPISingleResponse):
    """
    Override to give you access to the actual device ids
    """

    def get_device_ids(self, **kwargs):
        """
        Get the list of device ids that are in this device id list

            d = springserve.device_id_list.get(id)
            device_ids = d.get_device_ids()

            for id in device_ids:
                print id.device_id

        """
        return self._service.get("{}/device_ids".format(self.id), **kwargs)

    def _to_list(self, input_list):
        """
        The api needs a list, and you can't serialize sets, or Series
        """
        if isinstance(input_list, list):
            return input_list

        return [x for x in input_list]

    def add_device_ids(self, device_ids):
        """
        Add a list of device ids to this device id list

            d = springserve.device_id_lists.get(id)
            d.add_device_ids(['123', '124'])

        device_ids: List of device ids you would like to add
        """
        payload = {'device_ids':self._to_list(device_ids)}
        resp = self._service.post(payload,
                                  path_param='{}/device_ids/bulk_create'.format(self.id)
                                 )
        return resp

    def remove_device_ids(self, device_ids):
        """
        Remove a list of device ids from this device id list

            d = springserve.device_id_lists.get(id)
            d.remove_device_ids(['123', '124'])

        device_ids: List of device ids you would like to remove
        """
        payload = {'device_ids':self._to_list(device_ids)}
        resp = self._service.bulk_delete(payload,
                                  path_param='{}/device_ids/bulk_delete'.format(self.id)
                                 )
        return resp


class _DeviceIdListAPI(_VDAPIService):

    __API__ = "device_id_lists"
    __RESPONSE_OBJECT__ = _DeviceIdListResponse


class _IpListResponse(_VDAPISingleResponse):
    """
    Override to give you access to the actual ips
    """

    def get_ips(self, **kwargs):
        """
        Get the list of ips that are in this ip list

            d = springserve.ip_lists.get(id)
            ips = d.get_ips()

            for i in ips:
                print i.ip

        """
        return self._service.get("{}/ips".format(self.id), **kwargs)

    def _to_list(self, input_list):
        """
        The api needs a list, and you can't serialize sets, or Series
        """
        if isinstance(input_list, list):
            return input_list

        return [x for x in input_list]

    def add_ips(self, ips):
        """
        Add a list of ips to this ip list

            d = springserve.ip_lists.get(id)
            d.add_ips(['123', '124'])

        ips: List of ips you would like to add
        """
        payload = {'ips':self._to_list(ips)}
        resp = self._service.post(payload,
                                  path_param='{}/ips/bulk_create'.format(self.id)
                                 )
        return resp

    def remove_ips(self, ips):
        """
        Remove a list of ips from this ip list

            d = springserve.ip_lists.get(id)
            d.remove_ips(['123', '124'])

        ips: List of ips you would like to remove
        """
        payload = {'ips':self._to_list(ips)}
        resp = self._service.bulk_delete(payload,
                                  path_param='{}/ips/bulk_delete'.format(self.id)
                                 )
        return resp


class _IpListAPI(_VDAPIService):

    __API__ = "ip_lists"
    __RESPONSE_OBJECT__ = _IpListResponse


class _BillItemAPI(_VDAPIService):

    __API__ = "bill_items"

    def __init__(self, bill_id):
        super(_BillItemAPI, self).__init__()
        self.bill_id = bill_id

    @property
    def endpoint(self):
        """
        The api endpoint that is used for this service.  For example:: 
            
            In [1]: import springserve

            In [2]: springserve.supply_tags.endpoint
            Out[2]: '/supply_tags'

        """
        return "/bills/{}/bill_items".format(self.bill_id)


class _BillResponse(_VDAPISingleResponse):
    
    def get_bill_items(self):
        # Need to make a new one per bill
        return _BillItemAPI(self.id).get()

    def _add_bill_item(self, data, **kwargs):
        return _BillItemAPI(self.id).post(data, **kwargs)


class _BillAPI(_VDAPIService):

    __API__ = "bills"
    __RESPONSE_OBJECT__ = _BillResponse

    def bulk_sync(self, ids, reauth=False, **query_params):
        query_params['ids'] = ','.join(str(x) for x in ids)

        return self.get('bulk_sync', reauth, **query_params)

class _ValueAPI(_VDAPIService):

    __API__ = "values"

    def __init__(self, key):
        super(_ValueAPI, self).__init__()
        self.key_id = key.id
        self.account_id = key.account_id 

    @property
    def endpoint(self):
       return "/keys/{}/values".format(self.key_id)


class _KeyResponse(_VDAPISingleResponse):

    def get_values(self):
        return _ValueAPI(self).get()

    def add_value(self, data, **kwargs):
        return _ValueAPI(self).post(data, **kwargs)
 
class _KeyAPI(_VDAPIService):

    __API__ = "keys"
    __RESPONSE_OBJECT__ = _KeyResponse

