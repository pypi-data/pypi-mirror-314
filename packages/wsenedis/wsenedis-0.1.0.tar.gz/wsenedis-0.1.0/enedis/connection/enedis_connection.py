import logging
import os
import re
from threading import Lock
from typing import Tuple, Any

from django.conf import settings
from lxml import etree
from requests import Session
from zeep import Settings, Client, Plugin
from zeep.proxy import OperationProxy
from zeep.transports import Transport

from enedis.utils.wsdl import wsdl

logger = logging.getLogger(__name__)

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class FixMalformedDatesPlugin(Plugin):
    def ingress(self, envelope, http_headers, operation):
        # Convert the lxml tree to a string for manipulation
        xml_string = etree.tostring(envelope, encoding="unicode")
        # Fix the malformed date
        fixed_xml = re.sub(r'(\d{4}-\d{2}-\d{2})\+00:00', r'\1', xml_string)
        # Return the modified XML as an lxml element
        envelope = etree.fromstring(fixed_xml)
        return envelope, http_headers


class EnedisConnection(metaclass=SingletonMeta):

    def __init__(self, enedis_url: str, login: str, contract_id: str, path_public_cert=None, path_private_cert=None):
        self.__session = None
        self.__transport = None
        self.__is_initialized = False
        self.__lock = Lock()
        self.settings = Settings(strict=True, xml_huge_tree=True)

        # Enedis informations
        self.enedis_url = enedis_url
        self.login = login
        self.contract_id = contract_id
        self.path_public_cert = path_public_cert
        self.path_private_cert = path_private_cert

        # Initialize the connection
        self._initialize_connection()

    def _initialize_connection(self):
        with self.__lock:
            if self.__is_initialized:
                return

            logger.info("Initializing connection...")
            self.__session = Session()

            self.__session.cert = (self.path_public_cert, self.path_private_cert)
            try:
                self.__transport = Transport(session=self.__session)
                self.__is_initialized = True
                logger.info("Connection initialized successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize connection: {e}")
                self._cleanup_resources()
                raise

    def _cleanup_resources(self):
        """
        Cleans up temporary files and session resources.
        """
        logger.info("Cleaning up resources...")
        if self.__session:
            self.__session.close()

        self.__is_initialized = False

    def get_transport(self):
        """
        Returns the transport object. Reinitializes the connection if necessary.
        """
        if not self.__is_initialized:
            logger.warning("Connection was closed or uninitialized. Reinitializing...")
            self._initialize_connection()
        return self.__transport

    def close_connection(self):
        """
        Closes the connection and cleans up resources.
        """
        with self.__lock:
            if self.__is_initialized:
                logger.info("Closing connection...")
                self._cleanup_resources()
                self.__transport = None
                self.__session = None
                self.enedis_url = None
                self.login = None
                self.contract_id = None
                self.path_public_cert = None
                self.path_private_cert = None
                logger.info("Connection closed successfully.")

    def soap_service(self, name: str, ns: str, port_binding: str, service_path: str, tn_binding: str = None) -> Tuple[OperationProxy, Any, Client]:
        """
        Creates a SOAP service proxy for interacting with Enedis API.

        Args:
            name (str): The WSDL name.
            ns (str): Namespace used in the type factory.
            port_binding (str): Port binding name.
            service_path (str): Path to the SOAP service endpoint.
            tn_binding (str, optional): Target namespace binding. Defaults to None.

        Returns:
            Tuple[OperationProxy, DynamicTypeFactory, Client]: A tuple containing:
                - The service proxy to perform operations.
                - The factory to create new data types.
                - The Client object for further use.
        """

        client = Client(wsdl=wsdl(name), transport=self.get_transport(), settings=self.settings,
                        plugins=[FixMalformedDatesPlugin()])

        service_proxy = client.create_service(f'{{{tn_binding}}}{port_binding}', os.path.join(self.enedis_url, service_path))
        print(ns)
        factory = client.type_factory(ns)

        return service_proxy, factory, client

    def __del__(self):
        self.close_connection()
