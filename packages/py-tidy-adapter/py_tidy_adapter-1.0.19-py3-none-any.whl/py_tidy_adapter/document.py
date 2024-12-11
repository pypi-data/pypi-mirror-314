from io import StringIO

from lxml import etree
from pandas import DataFrame

from py_tidy_adapter.exception import TidyException

import pandas as pd

encoding = 'unicode'


class Document:
    """
       Classe da utilizzare per rappresentare una classe di business.
       """

    def __init__(self):
        self.adapter = None
        self.class_business = None
        self.__root = None
        self.name = None
        self.owner = None
        self.lastUpdateOwner = None
        self.group = None
        self.nameApplication = None
        self.creationDate = None
        self.lastUpdateDate = None
        self.note = None
        self.revision = None
        self.version = None
        self.labelVersion = None
        self.update = None
        self.workspace = None
        self.keys = {}
        self.metainf = None

    @staticmethod
    def from_xml(xml: 'str', is_wrapped: 'bool' = False):
        """
        Restituisce un oggetto Document effettuando il parsing di un xml.
        :param xml: str  Rappresentazione xml del documento.
        :param is_wrapped: Se True considero il documento decorato con una sovrastruttura che comprende anche i references, le chiavi e le metainf
        :rtype: Restituisce un oggetto di tipo Document che rappresenta l'xml fornito in input
        """
        return Document.from_element_tree(etree.fromstring(xml), is_wrapped)

    def to_xml(self, with_reference: 'bool' = False):
        """
        Esporta il documento.
        :param with_reference: se True racchiude il documento in una sovrastruttura contenente i references, le chiavi e le metainf
        :rtype: xml
        """
        return etree.tostring(self.__to_element_tree(with_reference), encoding=encoding)

    def __to_element_tree(self, with_reference=False):
        """
        Esporta il documento in formato elementTree.
        :param with_reference: se True racchiude il documento in una sovrastruttura contenente i references, le chiavi e le metainf
        :rtype: Element
        """

        if with_reference:
            if self.class_business is None: raise TidyException("variabile class_business non impostata")
            value = etree.Element('value')
            references = etree.SubElement(value, 'references', {})
            if self.name is not None: etree.SubElement(references, 'name', {}).text = self.name
            if self.owner is not None: etree.SubElement(references, 'owner', {}).text = self.owner
            if self.lastUpdateOwner is not None: etree.SubElement(references, 'lastUpdateOwner',
                                                                  {}).text = self.lastUpdateOwner
            if self.group is not None: etree.SubElement(references, 'group', {}).text = self.group
            if self.nameApplication is not None: etree.SubElement(references, 'nameApplication',
                                                                  {}).text = self.nameApplication
            if self.creationDate is not None: etree.SubElement(references, 'creationDate', {}).text = self.creationDate
            if self.lastUpdateDate is not None: etree.SubElement(references, 'lastUpdateDate',
                                                                 {}).text = self.lastUpdateDate
            if self.note is not None: etree.SubElement(references, 'note', {}).text = self.note
            if self.revision is not None: etree.SubElement(references, 'revision', {}).text = self.revision
            if self.version is not None: etree.SubElement(references, 'version', {}).text = self.version
            if self.labelVersion is not None: etree.SubElement(references, 'labelVersion', {}).text = self.labelVersion
            if self.update is not None: etree.SubElement(references, 'update', {}).text = self.update
            if self.workspace is not None: etree.SubElement(references, 'workspace', {}).text = self.workspace
            keys = etree.SubElement(value, 'keys', {})
            for k in self.class_business.keys:
                etree.SubElement(keys, 'key', {'name': k.name}).text = self.keys[k.name]
            value.append(self.__root)
            if self.metainf is not None: etree.SubElement(value, 'metainf', {}).text = etree.tostring(self.metainf,
                                                                                                      encoding=encoding)

            return value
        else:
            return self.__root

    @staticmethod
    def from_element_tree(document, is_wrapped: 'bool' = False):
        """
        Restituisce un oggetto Document effettuando il parsing di un xml.
        :param document:
        :param is_wrapped: Se True considero il documento decorato con una sovrastruttura che comprende anche i references, le chiavi e le metainf
        :rtype: Restituisce un oggetto di tipo Document che rappresenta l'xml fornito in input
        """
        doc = Document()
        if is_wrapped:
            for child in document:
                if child.tag == 'references':
                    for r in child:
                        if r.tag == 'name':
                            doc.name = r.text
                        elif r.tag == 'lastUpdateOwner':
                            doc.lastUpdateOwner = r.text
                        elif r.tag == 'owner':
                            doc.owner = r.text
                        elif r.tag == 'group':
                            doc.group = r.text
                        elif r.tag == 'nameApplication':
                            doc.nameApplication = r.text
                        elif r.tag == 'update':
                            doc.update = r.text
                        elif r.tag == 'creationDate':
                            doc.creationDate = r.text
                        elif r.tag == 'lastUpdateDate':
                            doc.lastUpdateDate = r.text
                        elif r.tag == 'note':
                            doc.note = r.text
                        elif r.tag == 'revision':
                            doc.revision = r.text
                        elif r.tag == 'labelVersion':
                            doc.labelVersion = r.text
                        elif r.tag == 'update':
                            doc.update = r.text
                        elif r.tag == 'workspace':
                            doc.workspace = r.text
                elif child.tag == 'keys':
                    for k in child:
                        doc.keys[k.attrib['name']] = k.text
                elif child.tag == 'metainf':
                    doc.metainf = child
                elif child.tag == 'xmlValue':
                    doc.__root = child[0]
        else:
            doc.__root = document

        return doc

    def get_doc(self):
        """
        Restituisce il documento
        :rtype: lxml
        """
        return self.__root

    def get(self, xpath: 'str' = '', wrapped: 'bool' = False):
        """
        Restituisce il valore presente al xpath indicato.
        :param xpath: xpath da eseguire
        :param wrapped: se True restituisce anche l'elemento
        :rtype: str
        """
        p = self.__root.xpath(xpath)
        return p[0].text if not wrapped and len(p) == 1 and p[0].text is not None else ''.join(
            etree.tostring(child, encoding=encoding) for child in p)

    def get_table(self, xpath: 'str' = ''):
        """
        Restituisce il valore presente al xpath indicato in forma tabellare.
        se all'xpath non è presente una tabella è generata un eccezione
        E' restituito un dataFrame
        :param xpath: xpath da eseguire
        :rtype: str
        """
        try:
            return pd.read_xml(StringIO(self.get(xpath=xpath, wrapped=True)))
        except:
            raise TidyException('Impossibile recuperare una DataFrame')

    def replace_value(self, xpath: 'str' = '', new_value: 'str' = ''):
        """
        Sostituisce  il valore presente al xpath indicato con il contenuto di newValue.
        :param xpath: xpath da eseguire
        :param new_value: nuovo valore
        :rtype: Document
        """
        p = self.__root.xpath(xpath)
        if p is not None:
            for child in p: child.text = new_value

        return self

    def replace_node(self, xpath: 'str' = '', new_xml: 'str' = ''):
        """
        Sostituisce  il valore presente al xpath indicato con il contenuto di newValue.
        :param xpath: xpath da eseguire
        :param new_xml: nuovo xml
        :rtype: Document
        """
        p = self.__root.xpath(xpath)
        if p is not None:
            for child in p:
                child.getparent().replace(child, etree.fromstring(new_xml))
        return self

    def replace_table(self, xpath: 'str' = '', df: 'DataFrame' = None):
        """
        Sostituisce  il valore presente al xpath indicato con il contenuto di newValue.
        :param xpath: xpath da eseguire
        :param new_xml: nuovo xml
        :rtype: Document
        """
        if df is not None:
            self.replace_node(xpath, df.to_xml(xml_declaration=False, root_name=xpath.split('/')[-1], index=False))

        return self

    def publish(self, is_revision: 'bool' = True):
        if self.adapter is None: raise TidyException("Variabile adapter non impostata")
        self.adapter.publish(name=self.name, action=1 if is_revision else 0, note='from python adapter',
                             docs=[self.to_xml(with_reference=True)])
