import base64
import gzip
import os
from datetime import datetime

import requests
from lxml import etree

# from tensorflow import keras
from zeep import Client

from py_tidy_adapter.exception import TidyException
from py_tidy_adapter.class_business import ClassBusiness

TF_MODEL = 'tfModel'


class ServiceResponse(object):
    pass


class Adapter:
    """
    Classe da utilizzare per interfacciarsi al server tidy
    E' obbligatorio fornire l'endpoint a cui connettersi
    E' possibile fornire un idSessione di default utilizzato in ogni successiva chiamata,
    in alternativa ad ogni metodo è possibile fornire un idSessione specifico.
    """

    def __init__(self, endpoint: 'str', default_id_session: 'str' = None):
        """
                :param endpoint: str . Endpoint del server Tidy
                :param default_id_session: str=None  Id sessione utilizzata come default se non specificata nel singolo metodo
                """

        self.endpoint = endpoint
        self.default_id_session = default_id_session
        self.client = Client(wsdl=self.endpoint)
        self.service = self.client.create_service('{it.itchange.bcr.basvi}basvi2SOAP', self.endpoint)

    def set_default_id_session(self, default_id_session: 'str' = None):
        """    Imposta l'id sessione di default, sovrascrive l'eventuale valore fornito nel costruttore.
                :param default_id_session: str=None  Id sessione utilizzata come default se non specificata nel singolo metodo
        """

        self.default_id_session = default_id_session

    def getsystemconfiguration(self) -> 'ws, app, properties, ServiceResponse':
        """
        Esegue l'action GetSystemConfiguration del server Tidy che restituisce la lista degli workspace e la lista dei parametri di configurazione.
        Questo metodo non necessità di un Id Sessione
        :rtype: list of workspaces, list of name application, dictionary of properties, Serviceresponse
        """
        input_type = self.client.get_type('ns0:GetSystemConfigurationInput')
        r = self.service.GetSystemConfiguration(input_type(1, 1))
        return ([el.text for el in r.xml[0].xpath('workspaces/workspace')]
                , [el.text for el in r.xml[0].xpath('applications/application')]
                , [{el.xpath('key')[0].text: el.xpath('value')[0].text} for el in r.xml[0].xpath('properties/entry')]
                , r)

    def login(self, user: 'str', password: 'str', workspace: 'str', name_application: 'str', type: 'str' = 'NORMAL',
              as_user: 'str' = None) -> 'ServiceResponse':
        """
        Effettua la login al server Tidy
        :param user: str  Nome utente
        :param password: str  Password dell'utente
        :param workspace: str   Workspace per cui si effettua la login
        :param name_application: str   Application per cui si effettua la login
        :param type: str   Tipo di login. può essere: NORMAL, PERMANENT, ONE_SHOT. il valore di default è NORMAL
        :param as_user: str  Nome utente usato per la connessione "as user"
        :rtype:   ServiceResponse
        """
        input_type = self.client.get_type('ns0:LoginInput')
        return self.service.Login(input_type(user, as_user, password, workspace, name_application, type, 1, 1))

    def logout(self, id_session: 'str' = None, background: 'boolean' = False) -> 'ServiceResponse':
        """
        Effettua il logout della sessione
        :param id_session: str Id sessione per cui si effettua il logout, se vale None è utilizzata la sessione di default
        :param background: boolean Flag utilizzato per specificare la modalità di esecuzione
        :rtype:  Serviceresponse
        """
        if id_session is None and self.default_id_session is None: raise TidyException('Id Sessione non specificato')
        input_type = self.client.get_type('ns0:LogoutInput')
        return self.service.Logout(
            input_type(id_session if id_session is not None else self.default_id_session, background, 1, 1))

    def nameClasses(self, id_session: 'str' = None, background: 'boolean' = False) -> 'str[] , ServiceResponse':
        """
        Restituisce il nome di tutte le classi
        :param id_session: str Id sessione per cui si effettua il logout, se vale None è utilizzata la sessione di default
        :param background: boolean Flag utilizzato per specificare la modalità di esecuzione
        :rtype:  str[],Serviceresponse
        """
        if id_session is None and self.default_id_session is None: raise TidyException('Id Sessione non specificato')
        request = f"""
                 <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:it="it.itchange.bcr.basvi">
                   <soapenv:Header/>
                   <soapenv:Body>
                      <it:GetInfoLogin>
                         <GetInfoLoginRequest >
                            <idSession>{id_session if id_session is not None else self.default_id_session}</idSession>
                            <lastVersion>true</lastVersion>
                            <bsc>true</bsc>
                            <abstracts>true</abstracts>
                            <views>true</views>
                            <components>false</components>
                            <onlyName>true</onlyName>
                            <background>{background}</background>
                         </GetInfoLoginRequest>
                      </it:GetInfoLogin>
                   </soapenv:Body>
                </soapenv:Envelope>       
        """
        response = requests.post(self.endpoint, request)
        doc = Adapter.__to_element__(response.text)

        sr = ServiceResponse()
        for child in doc[0][0][0]:
            setattr(sr, child.tag, etree.tostring(child[0]) if len(child) > 0 else child.text)
        list = []
        for n in Adapter.__to_element__(sr.xml):
            list.append(n.text)
        return list, sr

    def get_class_business(self, id_session: 'str' = None, name: 'str' = '',
                           background: 'boolean' = False) -> 'ClassBusiness,ServiceResponse':
        """
        Restituisce la classe di business specificata
        :param id_session: str Id sessione per cui si effettua il logout, se vale None è utilizzata la sessione di default
        :param id_session: str name Nome della classe di business
        :param background: boolean Flag utilizzato per specificare la modalità di esecuzione
        :rtype:  ClassBusiness,Serviceresponse
        """
        if id_session is None and self.default_id_session is None: raise TidyException('Id Sessione non specificato')
        request = f"""
                <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:it="it.itchange.bcr.basvi">
                   <soapenv:Header/>
                   <soapenv:Body>
                      <it:GetClassBusiness>
                         <GetClassBusinessRequest priority="?" id="?">
                            <idSession>{id_session if id_session is not None else self.default_id_session}</idSession>
                            <nameClassBusiness>{name}</nameClassBusiness>
                            <background>{background}</background>
                         </GetClassBusinessRequest>
                      </it:GetClassBusiness>
                   </soapenv:Body>
                </soapenv:Envelope>      
        """
        response = requests.post(self.endpoint, request)
        doc = Adapter.__to_element__(response.text)

        sr = ServiceResponse()
        for child in doc[0][0][0]:
            setattr(sr, child.tag, etree.tostring(child[0]) if len(child) > 0 else child.text)
        c=ClassBusiness.from_xml(sr.xml) if sr.code=='0' else None
        if c is not None: c.adapter=self
        return c, sr

    def query(self, id_session: 'str' = None, query: 'str' = '"no query" ', param_list=None,
              background: 'boolean' = False) -> 'str , ServiceResponse':
        """
        Esegui una generic query con eventuali parametri
        :param id_session: str Id sessione per cui si effettua il logout, se vale None è utilizzata la sessione di default
        :param query: str Query
        :param param_list: list Lista di parametri associati alla query
         :param background: boolean Flag utilizzato per specificare la modalità di esecuzione
        :rtype:  xml,ServiceResponse xml: Restituisce la stringa di risposta se la query termina correttamente oppure None; ServiceResponse
        """
        if id_session is None and self.default_id_session is None: raise TidyException('Id Sessione non specificato')
        if param_list is None:
            param_list = []
        input_type = self.client.get_type('ns0:ExecuteGenericQueryInput')
        param_type = self.client.get_type('ns0:paramListType')
        sr = self.service.ExecuteGenericQuery(
            input_type(id_session if id_session is not None else self.default_id_session, query, param_type(param_list),
                       None, True, background, 1, 1))
        if sr.code == '0' or sr.code == '-1':
            try:
                if sr.xml is not None:
                    if isinstance(sr.xml, list):
                        str_list = []
                        for x in sr.xml:
                            str_list.append(etree.tostring(x).decode())
                        return ''.join(str_list), sr
                    else:
                        return etree.tostring(sr.xml).decode(), sr
            except:
                return sr.xml, sr
            else:
                return None, sr
        else:
            raise TidyException(sr)

    def alterQuery(self, id_session: 'str' = None, name_class: 'str' = None, version: 'str' = '0',
                   keys: 'dict' = None, query: 'str' = 'generic', param_list=[], action: 'str' = '1',
                   background: 'boolean' = False) -> 'str , ServiceResponse':
        """
        Esegui una alter query con eventuali parametri
        :param id_session: str Id sessione per cui si effettua il logout, se vale None è utilizzata la sessione di default
        :param name_class: str nome della classe
        :param version: str Version della classe
        :param keys: Dict Dizionario con le chiavi
        :param query: str Query
        :param param_list: list Lista di parametri associati alla query
        :param action: '1'->revisione, 2->sovrascrittura
        :param background: boolean Flag utilizzato per specificare la modalità di esecuzione
        :rtype:  message,ServiceResponse xml: eventuale messaggio di errore; ServiceResponse
        """
        if id_session is None and self.default_id_session is None: raise TidyException('Id Sessione non specificato')
        request = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:it ="it.itchange.bcr.basvi" >'
        request += '<soapenv:Body>'
        request += '<it:ExecuteClassAlterQuery>'
        request += '<ExecuteClassAlterQueryRequest>'
        request += '<idSession>{}</idSession>'.format(
            id_session if id_session is not None else self.default_id_session)
        request += '<selection>'
        request += '<selector>'
        request += '<nameClassBusiness>{}</nameClassBusiness>'.format(name_class)
        request += '<version>{}</version>'.format(version)
        request += '<keys>'
        for k, v in keys.items():
            request += '<key name="{}">{}</key>'.format(k, v)
        request += '</keys>'
        request += '</selector>'
        request += '<paramList>'
        for v in param_list:
            request += '<value>{}</value>'.format(v)
        request += '</paramList>'
        request += '</selection>'
        request += '<nameQuery>{}</nameQuery>'.format(query)
        request += '<action>{}</action>'.format(action)
        request += '<background>{}</background>'.format('true' if background else 'false')
        request += '</ExecuteClassAlterQueryRequest>'
        request += '</it:ExecuteClassAlterQuery>'
        request += '</soapenv:Body>'
        request += '</soapenv:Envelope>'
        response = requests.post(self.endpoint, request)
        doc = Adapter.__to_element__(response.text)

        sr = ServiceResponse()
        for child in doc[0][0][0]:
            setattr(sr, child.tag, etree.tostring(child[0]) if len(child) > 0 else child.text)

        return sr.message, sr

    def addAttachment(self, id_session: 'str' = None, name_class: 'str' = None, version: 'str' = '0',
                      keys: 'dict' = None, name_attach: 'str' = 'att1', data: 'str' = ' ',
                      background: 'boolean' = False) -> 'str , ServiceResponse':
        """
        Esegui una alter query con eventuali parametri
        :param id_session: str Id sessione per cui si effettua il logout, se vale None è utilizzata la sessione di default
        :param name_class: str nome della classe
        :param version: str Version della classe
        :param keys: Dict Dizionario con le chiavi
        :param query: str Query
        :param param_list: list Lista di parametri associati alla query
        :param action: '1'->revisione, 2->sovrascrittura
        :param background: boolean Flag utilizzato per specificare la modalità di esecuzione
        :rtype:  message,ServiceResponse xml: eventuale messaggio di errore; ServiceResponse
        """
        if id_session is None and self.default_id_session is None: raise TidyException('Id Sessione non specificato')
        request = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:it = "it.itchange.bcr.basvi" > '
        request += '<soapenv:Body>'
        request += '<it:AddAttachments>'
        request += '<AddAttachmentsRequest>'
        request += '<idSession>{}</idSession>'.format(id_session if id_session is not None else self.default_id_session)
        request += '<attachments>'
        request += '<attachmentsDoc>'
        request += '<selector>'
        request += '<nameClassBusiness>{}</nameClassBusiness>'.format(name_class)
        request += '<version>{}</version>'.format(version)
        request += '<keys>'
        for k, v in keys.items():
            request += '<key name="{}">{}</key>'.format(k, v)
        request += '</keys>'
        request += '</selector>'
        request += '<items>'
        request += '<item>'
        request += '<name>{}</name>'.format(name_attach)
        request += '<data>{}</data>'.format(data)
        request += '</item>'
        request += '</items>'
        request += '</attachmentsDoc>'
        request += '</attachments>'
        request += '<background>{}</background>'.format('true' if background else 'false')
        request += '</AddAttachmentsRequest>'
        request += '</it:AddAttachments>'
        request += '</soapenv:Body>'
        request += '</soapenv:Envelope>'

        response = requests.post(self.endpoint, request)
        doc = Adapter.__to_element__(response.text)

        sr = ServiceResponse()
        for child in doc[0][0][0]:
            setattr(sr, child.tag, etree.tostring(child[0]) if len(child) > 0 else child.text)

        return sr.message, sr

    def publish(self, id_session: 'str' = None, name_class: 'str' = None, version: str = '0',
                component_update_type: str = None, action: 'int' = 1, note: 'str' = None,
                docs: 'list' = None) -> 'str , ServiceResponse':
        """
        Pubblica una lista di documenti
        :param id_session: str Id sessione per cui si effettua il logout, se vale None è utilizzata la sessione di default
        :param name_class: str Nome della classe
        :param version: str Versione della classe, il valore di default è 0 (ultima versione)
        :param component_update_type: str Modalità di update. Da utilizzare nelle pubblicazioni parziali
        :param component_update_type: str Modalità di update. Da utilizzare nelle pubblicazioni parziali
        :param action: int Modalità di pubblicazione: 0:update, 1:revisione,  2:warning if exist
        :param docs: list Lista di stringhe xml
        :rtype:  message,ServiceResponse message:  ServiceResponse.message; ServiceResponse
        """
        if id_session is None and self.default_id_session is None: raise TidyException('Id Sessione non specificato')
        request = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:it = ' \
                  '"it.itchange.bcr.basvi" > '
        request += '<soapenv:Body>'
        request += '<it:BulkLoad>'
        request += '<BulkLoadRequest>'
        request += '<idSession>{}</idSession>'.format(id_session if id_session is not None else self.default_id_session)
        request += '<nameClassBusiness>{}</nameClassBusiness>'.format(name_class)
        request += '<action>{}</action>'.format(action if action is not None else '1')
        request += '<componentUpdateType>{}</componentUpdateType>'.format(
            component_update_type if component_update_type is not None else '1')
        request += '<note>{}</note>'.format(note if note is not None else '')
        request += '<background>false</background>'
        request += '<values>'
        for v in docs:
            request += v
        request += '</values>'
        request += '</BulkLoadRequest>'
        request += '</it:BulkLoad>'
        request += '</soapenv:Body>'
        request += '</soapenv:Envelope>'

        headers = {"Content-Type": "application/xml", "Content-Encoding": "gzip"}
        response = requests.post(self.endpoint, data=gzip.compress(str.encode(request)), headers=headers)
        doc = Adapter.__to_element__(response.text)

        sr = ServiceResponse()
        for child in doc[0][0][0]:
            setattr(sr, child.tag, etree.tostring(child[0]) if len(child) > 0 else child.text)

        return sr.message, sr

    def add_attachment(self, id_session: 'str' = None, name_class: 'str' = None, version: str = '0',
                       keys: 'dict' = None, name_att: 'str' = None, data_att: str = None) -> 'str , ServiceResponse':
        """
        Aggiunge un allegato, fornito come stringa codificata in base64, ad uno specifico documento di una classe
        :param id_session: str Id sessione per cui si effettua il logout, se vale None è utilizzata la sessione di default
        :param name_class: str Nome della classe
        :param version: str Versione della classe, il valore di default è 0 (ultima versione)
        :param keys: dict Dictionary che specifica le chiavi del docuemento
        :param name_att: str Nome da assegnare all'allegato
        :param data_att: str Stringa codificata in base64 dell'allegato
        :rtype:  message,ServiceResponse message:ServiceResponse.message; ServiceResponse
        """
        if id_session is None and self.default_id_session is None: raise TidyException('Id Sessione non specificato')
        request = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:it = ' \
                  '"it.itchange.bcr.basvi" > '
        request += '<soapenv:Body>'
        request += '<it:AddAttachments>'
        request += '<AddAttachmentsRequest>'
        request += '<idSession>{}</idSession>'.format(id_session if id_session is not None else self.default_id_session)
        request += '<attachments>'
        request += '<attachmentsDoc>'
        request += '<selector>'
        request += '<nameClassBusiness>{}</nameClassBusiness>'.format(name_class)
        request += '<version>{}</version>'.format(version)
        request += '<keys>'
        for k, v in keys.items():
            request += '<key name="{}">{}</key>'.format(k, v)
        request += '</keys>'
        request += '</selector>'
        request += '<items>'
        request += '<item>'
        request += '<name>{}</name>'.format(name_att)
        request += '<data>{}</data>'.format(data_att.decode('utf8') if isinstance(data_att, bytes) else data_att)
        request += '<documentRevision>0</documentRevision>'
        request += '</item>'
        request += '</items>'
        request += '</attachmentsDoc>'
        request += '</attachments>'
        request += '<background>false</background>'
        request += '</AddAttachmentsRequest>'
        request += '</it:AddAttachments>'
        request += '</soapenv:Body>'
        request += '</soapenv:Envelope>'
        response = requests.post(self.endpoint, request)
        doc = Adapter.__to_element__(response.text)

        sr = ServiceResponse()
        for child in doc[0][0][0]:
            setattr(sr, child.tag, etree.tostring(child[0]) if len(child) > 0 else child.text)

        return sr.message, sr

    def read_attachment(self, id_session: 'str' = None, name_class: 'str' = None, version: str = '0',
                        keys: 'dict' = None, name_att: 'str' = None, revision: 'int' = 0) -> 'str , ServiceResponse':
        """
        Legge un allegato da uno specifico documento di una classe
        :param id_session: str Id sessione per cui si effettua il logout, se vale None è utilizzata la sessione di default
        :param name_class: str Nome della classe
        :param version: str Versione della classe, il valore di default è 0 (ultima versione)
        :param keys: dict Dictionary che specifica le chiavi del docuemento
        :param name_att: str Nome dell'allegato da recuperare
        :param revision: int Revisione del documento, il default è 0 (ultima revisione)
        :rtype:  data,ServiceResponse data:Codifica base64 dell'allegato; ServiceResponse
        """
        if id_session is None and self.default_id_session is None: raise TidyException('Id Sessione non specificato')
        request = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:it = ' \
                  '"it.itchange.bcr.basvi" > '
        request += '<soapenv:Body>'
        request += '<it:GetAttachments>'
        request += '<GetAttachmentsRequest>'
        request += '<idSession>{}</idSession>'.format(id_session if id_session is not None else self.default_id_session)
        request += '<attachments>'
        request += '<attachmentsDoc>'
        request += '<selector>'
        request += '<nameClassBusiness>{}</nameClassBusiness>'.format(name_class)
        request += '<version>{}</version>'.format(version)
        request += '<keys>'
        for k, v in keys.items():
            request += '<key name="{}">{}</key>'.format(k, v)
        request += '</keys>'
        request += '</selector>'
        request += '<items>'
        request += '<item>'
        request += '<name>{}</name>'.format(name_att)
        request += '<documentRevision>{}</documentRevision>'.format(revision)
        request += '</item>'
        request += '</items>'
        request += '</attachmentsDoc>'
        request += '</attachments>'
        request += '<background>false</background>'
        request += '</GetAttachmentsRequest>'
        request += '</it:GetAttachments>'
        request += '</soapenv:Body>'
        request += '</soapenv:Envelope>'
        response = requests.post(self.endpoint, request)
        doc = Adapter.__to_element__(response.text)

        sr = ServiceResponse()
        for child in doc[0][0][0]:
            setattr(sr, child.tag, etree.tostring(child[0]) if len(child) > 0 else child.text)

        try:
            data = doc.xpath('//xml/attachments/attachment[1]/items/item[1]/data')[0].text
        except Exception:
            raise ValueError('no attachment found')
        return data, sr

    def event_trigger(self, id_session: 'str' = None, name_event: 'str' = 'event', message_event: str = '',
                      parameters: 'dict' = None) -> 'ServiceResponse':
        """
        Genera un evento di tipo BasviEvent con messaggio ed eventuali parametri
        :param id_session: str Id sessione per cui si effettua il logout, se vale None è utilizzata la sessione di default
        :param name_event: str Nome dell'evento
        :param message_event: str Messaggio dell'evento
        :param parameters: dict Dictionary con i parametri dell'evento
        :rtype:  ServiceResponse ServiceResponse
        """
        if id_session is None and self.default_id_session is None: raise TidyException('Id Sessione non specificato')
        request = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:it = ' \
                  '"it.itchange.bcr.basvi" > '
        request += '<soapenv:Body>'
        request += '<it:EventTrigger>'
        request += '<EventTriggerRequest>'
        request += '<idSession>{}</idSession>'.format(id_session if id_session is not None else self.default_id_session)
        request += '<name>{}</name>'.format(name_event)
        request += '<message>{}</message>'.format(message_event)
        request += '<parameters>'
        if parameters is not None:
            for k, v in parameters.items():
                request += '<parameter name="{}">{}</parameter>'.format(k, v)
        request += '</parameters>'
        request += '<background>false</background>'
        request += "</EventTriggerRequest>"
        request += '</it:EventTrigger>'
        request += '</soapenv:Body>'
        request += '</soapenv:Envelope>'

        response = requests.post(self.endpoint, request.encode("utf-8"))
        doc = Adapter.__to_element__(response.text)

        sr = ServiceResponse()
        for child in doc[0][0][0]:
            setattr(sr, child.tag, etree.tostring(child[0]) if len(child) > 0 else child.text)

        return sr

    @staticmethod
    def __to_element__(xml):
        if isinstance(xml, etree._Element):
            doc = xml
        else:
            doc = etree.fromstring(xml)
        return doc

    @staticmethod
    def to_list(xml: 'str or etree._Element', col_name: 'str' = '*') -> 'list':
        """
        Estrae una lista partendo dall'xml fornito in input
        Esempi: adapter.to_list('<a><b>1</b><b>2</b></a>','b') -> [1,2]
                adapter.to_list('<a><c><b>1</b><b>2</b></c></a>','c/b') -> [1,2]
        :param xml: str or etree._Element,
        :param col_name: str, nome del tag xml oppure espressione xpath da utilizzare per determinare come estrarre la lista
        :rtype:  list Lista d valori estratti dall'xml
        """

        list = []
        for child in Adapter.__to_element__(xml).xpath(col_name):
            list.append(child.text)
        return list

    @staticmethod
    def to_matrix(xml, row_name: 'str' = None, col_name: 'str' = '*') -> 'matrix':
        """
        Estrae una matrice partendo dall'xml fornito in input
        Esempi: adapter.to_matrix('<a><row>
                                      <b>1</b>
                                      <b>2</b>
                                    </row>
                                    <row>
                                       <b>3</b>
                                       <b>4</b>
                                    </row>
                                </a>','row','b') -> [[1,2]  ,[3,4]]
                adapter.to_matrix('<a><c>
                                    <row>
                                      <b1>1</b>
                                      <b2>2</b>
                                    </row>
                                    <row>
                                       <b1>3</b>
                                       <b2>4</b>
                                    </row>
                               </c> </a>','c/row','*') -> [[1,2]  ,[3,4]]
        :param xml: str or etree._Element,
        :param row_name: str, nome del tag xml oppure espressione xpath da utilizzare per determinare le righe della matrice
        :param col_name: str, nome del tag xml oppure espressione xpath da utilizzare per determinare le colonne della matrice
        :rtype:  matrix Matrice d valori estratti dall'xml
        """

        matrix = []
        for row in Adapter.__to_element__(xml).xpath(row_name):
            r = []
            for child in row.xpath(col_name):
                r.append(child.text)
            matrix.append(r)

        return matrix

    @staticmethod
    def to_matrix_number(xml, row_name: 'str' = None, col_name: 'str' = '*') -> 'matrix':
        """
        Estrae una matrice partendo dall'xml fornito in input
        Esempi: adapter.to_matrix('<a><row>
                                      <b>1</b>
                                      <b>2</b>
                                    </row>
                                    <row>
                                       <b>3</b>
                                       <b>4</b>
                                    </row>
                                </a>','row','b') -> [[1,2]  ,[3,4]]
                adapter.to_matrix('<a><c>
                                    <row>
                                      <b1>1</b>
                                      <b2>2</b>
                                    </row>
                                    <row>
                                       <b1>3</b>
                                       <b2>4</b>
                                    </row>
                               </c> </a>','c/row','*') -> [[1,2]  ,[3,4]]
        :param xml: str or etree._Element,
        :param row_name: str, nome del tag xml oppure espressione xpath da utilizzare per determinare le righe della matrice
        :param col_name: str, nome del tag xml oppure espressione xpath da utilizzare per determinare le colonne della matrice
        :rtype:  matrix Matrice d valori estratti dall'xml
        """

        matrix = []
        for row in Adapter.__to_element__(xml).xpath(row_name):
            r = []
            for child in row.xpath(col_name):
                r.append(float(child.text))
            matrix.append(r)

        return matrix

    @staticmethod
    def matrix_to_xml(matrix, root_name: 'str', row_name: 'str', col_name: 'str') -> 'str':
        """
         Ricostruisce un xml utilizzando la matrice fornita in input
         Esempio:
            adapter.matrix_to_xml([[1,2],[3,4],'root','row','col') ->
                                      <root>
                                         <row>
                                            <col>1</col>
                                            <col>2</col>
                                         </row>
                                         <row>
                                            <col>3</col>
                                            <col>4</col>
                                         </row>
                                      </root>
         :param matrix: matrix  ,
         :param root_name: str, root dell'xml
         :param row_name: str, nome dell'elemento separatore delle righe
         :param col_name: str, nome dell'elemento separatore delle colonne
         :rtype:  str xml rappresentante la matrice
        """

        # noinspection PyListCreation
        str_list = []
        str_list.append('<{}>'.format(root_name))
        for row in matrix:
            str_list.append('<{}>'.format(row_name))
            i = 0;
            for col in row:
                nn = col_name if isinstance(col_name, str) else col_name[i]
                str_list.append('<{}>'.format(nn))
                str_list.append(str(col))
                str_list.append('</{}>'.format(nn))
                i += 1
            str_list.append('</{}>'.format(row_name))
        str_list.append('</{}>'.format(root_name))
        return ''.join(str_list)

    def save_tf_model(self, id_session: 'str', name, model, scope_metrics: dict = None, model_description: 'str' = '',
                      revision_detail: 'str' = '', parameters: 'list' = []) -> 'str, ServiceResponse':
        """
        Salva sulla classe di business tfModel un modello tensorflow con i relativi pesi, eventuali parametri aggiuntivi e metriche per la valutazione
        Il modello tensorflow è salvato come attachment della classe
        :param id_session: str Id sessione per cui si effettua il logout, se vale None è utilizzata la sessione di default
        :param name: Nome del modello
        :param model: Modello tensorflow
        :param scope_metrics: Dictionary in cui si forniscono differenti set di input-output utilizzati per la validazione del modello.
                              Le metriche utilizzate sono quelle definite sul modello tensorflow
                              Esempio {'training': ([x_train], [y_train]), 'validation': ([x_val], [y_val])}
        :param model_description: Descrizione generale del modello
        :param revision_detail: Descrizione della revisione del modello
        :param parameters: Eventuali parametri aggiuntivi utilizzati per generare l'output e necessari nella fase di predict. Ad esempio i parametri utilizzati per normalizzare i dati di input
        :return:  message,ServiceResponse message:ServiceResponse.message; ServiceResponse
        """
        # noinspection PyListCreation

        str_list = []
        str_list.append('<value>')
        str_list.append('<keys>')
        str_list.append('<key name="name">{}</key>'.format(name))
        str_list.append('</keys>')
        str_list.append('<xmlValue>')
        str_list.append('<tfModel>')
        str_list.append('<name>{}</name>'.format(name))
        str_list.append('<modelDescription>{}</modelDescription>'.format(model_description))
        str_list.append('<revisionDetail>{}</revisionDetail>'.format(revision_detail))
        str_list.append('<type>{}</type>'.format(model.name))
        str_list.append('<summary><![CDATA[{}]]></summary>'.format(model.summary))
        str_list.append('<json><![CDATA[{}]]></json>'.format(model.to_json()))
        str_list.append('<metrics>')
        if scope_metrics is not None:
            for scope in scope_metrics:
                inp = scope_metrics.get(scope)
                metrics = model.evaluate(inp[0], inp[1], verbose=0)
                if not isinstance(metrics, list):
                    metrics = [metrics]
                for i in range(len(metrics)):
                    str_list.append('<metric>')
                    str_list.append('<scope>{}</scope>'.format(scope))
                    str_list.append('<type>{}</type>'.format(model.metrics_names[i]))
                    str_list.append('<value>{}</value>'.format(metrics[i]))
                    str_list.append('</metric>')
        str_list.append('</metrics>')
        str_list.append('<parameters>')
        for param in parameters:
            str_list.append('<par>')
            str_list.append('<key>{}</key>'.format(param['key']))
            str_list.append('<value>{}</value>'.format(param['value']))
            str_list.append('</par>')
        str_list.append('</parameters>')
        str_list.append('</tfModel>')
        str_list.append('</xmlValue>')
        str_list.append('</value>')

        value = ''.join(str_list)

        message, sr = self.publish(id_session, TF_MODEL, '0', None, 1, 'from python client', [value])
        if sr.code == '0':
            name_temp_file = 'temp_' + str(datetime.timestamp(datetime.now())).replace('.', '_') + '.h5'
            model.save(name_temp_file)
            try:
                with open(name_temp_file, "rb") as h5:
                    encoded_string = base64.b64encode(h5.read()).decode('utf-8')
                    message, sr1 = self.add_attachment(id_session, TF_MODEL, '0', {'name': name}, 'model_h5',
                                                       encoded_string)
                    if sr1.code == '0':
                        return 'model saved correctly', sr1
                    else:
                        raise TidyException(sr1)
            finally:
                os.remove(name_temp_file)
        else:
            raise TidyException(sr)

    def read_tf_model(self, id_session: 'str', name: 'str', revision: 'int' = 0) -> 'tensorflow model':
        data, sr = self.query(id_session, "!!{}('{}'):f($xml/parameters)!!".format(TF_MODEL, name))
        """
        Legge dalla classe di business tfModel un modello tensorflow con i relativi pesi, eventuali parametri aggiuntivi e metriche per la valutazione
        :param id_session: str Id sessione per cui si effettua il logout, se vale None è utilizzata la sessione di default
        :param name: Nome del modello
        :param revision: Revisione del modello. Il valore di default è 0 (ultima revisione)        
        :return:  tensorflow model utilizzabile
        """

        if sr.code == '0':
            if data is None: raise TidyException('Il modello [{}] non è stato addestrato.'.format(name))
            params = {}
            for child in Adapter.__to_element__(data):
                params[child.xpath('key')[0].text] = child.xpath('value')[0].text

            data, sr = self.read_attachment(id_session, TF_MODEL, '0', {'name': name}, 'model_h5', revision)
            if sr.code == '0':
                name_temp_file = 'temp_' + str(datetime.timestamp(datetime.now())).replace('.', '_') + '.h5'
                try:
                    with open(name_temp_file, "wb") as h5:
                        h5.write(base64.b64decode(bytearray(data, 'utf-8')))
                # model = keras.models.load_model(name_temp_file)
                finally:
                    os.remove(name_temp_file)
                # return model, params
                return params
            else:
                raise TidyException(sr)


adapter = Adapter('https://it-change.it/tidy/ml/?wsdl/N58dMzn82Mxbx8Mznsw2mmQa5xoMsycLoanc1Pixc4Froc', None);
idSession = adapter.login('federico', 'Gen2024!', 'mathmarket', 'excel').xml;
adapter.set_default_id_session(idSession)
#list_classes,_=adapter.nameClasses()
#for nc in list_classes:
#    print(f"read {nc}...")
#    c,sr=adapter.get_class_business(name=nc)
#    print(f"ok {c.name if c is not None else 'no'}")
c, sr = adapter.get_class_business(name='Temperature')
for d in c.get_document([1]):
   df = d.get_table('temp')

   df=df.rename(columns = {'data':'ggggg'})
   d.replace_table('temp',df)
   print(d.to_xml())

