#!/usr/bin/python
# coding: utf-8

import logging
import paho.mqtt.client as mqtt
import requests
import ssl


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class PyDoritaLocal(object):
    def __init__(self, hostname, username, password, port=8883):
        def on_connect(client, userdata, flags, rc):
            logger.debug('ON CONNECT')
            logger.info('Connected with result code {}'.format(rc))

        def on_message(client, userdata, msg):
            logger.debug('Message received: {}'.format(msg))

        self._client = mqtt.Client(client_id=username)

        # Disable SSL cert check
        # self._client.tls_set(
        #     ca_certs='/etc/ssl/certs/ca-certificates.crt',
        #     cert_reqs=ssl.CERT_NONE
        # )
        self._client.tls_set(
            '/etc/ssl/certs/ca-certificates.crt',
            None,
            None,
            cert_reqs=ssl.CERT_NONE,
            tls_version=ssl.PROTOCOL_TLSv1,
            ciphers=None
        )
        self._client.tls_insecure_set(True)

        # Setup callbacks and connect
        self._client.on_connect = on_connect
        self._client.on_message = on_message
        self._client.connect(hostname, port, keepalive=60)
        self._client.username_pw_set(username, password)

        self._client.loop_start()

    def disconnect(self):
        self._client.disconnect()
        return self._client.loop_stop()


class PyDoritaClient(object):
    def __init__(self, hostname, port=3000, username=None, password=None,
                 local=True, tls=False, verify=True):
        self.hostname = hostname
        self.port = port
        self.local = local
        self.auth = (username, password) if any([username, password]) else None
        self.tls = tls
        self.verify = verify
        self.API_URL = '{}://{}:{}/api/{}'.format(
            'https' if tls else 'http',
            hostname,
            port,
            'local' if local else 'cloud'
        )

    def __rq(self, method, url):
        r = requests.request(method=method, url=url, auth=self.auth,
                             verify=self.verify)
        r.raise_for_status()
        return r.json()


    # Info
    def info(self, endpoint):
        url = self.API_URL + '/info/{}'.format(endpoint)
        return self.__rq('GET', url)

    @property
    def mission(self):
        return self.info('mission')

    @property
    def phase(self):
        return self.mission['cleanMissionStatus'].get('phase', None)

    @property
    def battery(self):
        return self.mission.get('batPct', None)

    @property
    def position(self):
        from collections import namedtuple
        pos_tuple = namedtuple('Position', ['x', 'y', 'theta'])
        pos = self.mission.get('pose', None)
        assert pos, 'Failed to determine position'
        x = pos['point'].get('x', None)
        y = pos['point'].get('y', None)
        theta = pos.get('theta', None)
        return pos_tuple(x, y, theta)

    @property
    def error(self):
        return self.mission['cleanMissionStatus'].get('error', None)

    @property
    def wireless(self):
        return self.info('wireless')

    @property
    def lastwireless(self):
        return self.info('lastwireless')

    @property
    def sys(self):
        return self.info('sys')

    @property
    def sku(self):
        return self.info('sku')

    @property
    def state(self):
        return self.info('state')


    # Config
    def config(self, endpoint):
        url = self.API_URL + '/config/{}'.format(endpoint)
        return self.__rq('GET', url)

    @property
    def ptime(self):
        return self.config('ptime')

    @property
    def bbrun(self):
        return self.config('bbrun')

    @property
    def cloud(self):
        return self.config('cloud')

    @property
    def langs(self):
        return self.config('langs')

    @property
    def week(self):
        return self.config('week')

    @property
    def time(self):
        return self.config('time')

    @property
    def preferences(self):
        return self.config('preferences')


    # Actions
    def action(self, endpoint):
        url = self.API_URL + '/action/{}'.format(endpoint)
        return self.__rq('GET', url)

    def start(self):
        return self.action('start')

    def clean(self):
        # Alias for start
        return self.start()

    def stop(self):
        return self.action('stop')

    def pause(self):
        return self.action('pause')

    def resume(self):
        return self.action('resume')

    def dock(self):
        return self.action('dock')

    def stop_and_dock(self):
        res_stop = self.stop()
        res_dock = self.dock()
        return (res_stop, res_dock)

