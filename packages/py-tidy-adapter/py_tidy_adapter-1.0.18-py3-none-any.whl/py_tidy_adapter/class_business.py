from lxml import etree
from py_tidy_adapter.bsc_elements import encoding,Query, Validator, Updater, Key, Schematron, Xslt, Component
from py_tidy_adapter.exception import TidyException
from py_tidy_adapter.document  import Document


class ClassBusiness:
    """
       Classe da utilizzare per rappresentare una classe di business.
       """

    def __init__(self):
        self.adapter  = None
        self.name = None
        self.description = None
        self.owner = None
        self.version = 0
        self.labelVersion = None
        self.update = 0
        self.creationDate = None
        self.aree = []
        self.preview = None
        self.sortEnabled = False
        self.viewQuery = None
        self.metainfPolicy = None
        self.keys = []  # keyDefinition
        self.extension = None
        self.components = []
        self.classQueries = []
        self.classAlterQueries = []
        self.validators = []
        self.xmlSchema = None
        self.xmlSchemaScope = "INHERIT"
        self.schematrons = []
        self.mapNameXslt = {}
        self.updaters = []
        self.metainf = None
        self.linkedBusiness = []
        self.isAbstract = False

    @staticmethod
    def from_xml(xml: 'str'):
        """
        Restituisce un oggetto ClassBusiness effettuando il parsing di un xml.
        :param xml: str  Rappresentazione xml del updater.
        :rtype: Restituisce un oggetto di tipo ClassBusiness che rappresenta l'xml fornito in input
        """
        return ClassBusiness.__from_element_tree(etree.fromstring(xml))

    def to_xml(self):
        """
        Esporta la classe di business in formato xml.
        :rtype: xml
        """
        return etree.tostring(self.__to_element_tree(), encoding=encoding)

    def __to_element_tree(self):
        """
        Esporta la classe di business in formato elementTree.
        :rtype: Element
        """
        definition = etree.Element('definition')
        references = etree.SubElement(definition, 'references', {})
        etree.SubElement(references, 'name', {}).text = self.name
        if self.description is not None: etree.SubElement(references, 'description', {}).text = self.description
        if self.owner is not None: etree.SubElement(references, 'owner', {}).text = self.owner
        if self.version is not None: etree.SubElement(references, 'version', {}).text = self.version
        if self.labelVersion is not None: etree.SubElement(references, 'labelVersion', {}).text = self.labelVersion
        if self.update is not None: etree.SubElement(references, 'update', {}).text = self.update
        if self.creationDate is not None: etree.SubElement(references, 'creationDate', {}).text = self.creationDate
        if len(self.aree) > 0:
            aree = etree.SubElement(references, 'aree', {})
            for a in self.aree:
                etree.SubElement(aree, 'area', {}).text = a
        if len(self.linkedBusiness) > 0:
            linked_business = etree.SubElement(references, 'linkedBusiness', {})
            for l in self.linkedBusiness:
                etree.SubElement(linked_business, 'link', {}).text = l

        if self.preview is not None: etree.SubElement(references, 'preview', {}).text = self.preview
        if self.sortEnabled is not None: etree.SubElement(references, 'sortEnabled', {}).text = self.sortEnabled
        if self.isAbstract is not None: etree.SubElement(references, 'abstract', {}).text = self.isAbstract
        if self.viewQuery is not None: etree.SubElement(references, 'viewQuery', {}).text = self.viewQuery
        if self.metainfPolicy is not None: etree.SubElement(references, 'metainfPolicy', {}).text = self.metainfPolicy

        keys = etree.SubElement(definition, 'keys', {})
        for k in self.keys:  keys.append(k.__to_element_tree())

        connections = etree.SubElement(definition, 'connections', {})
        if len(self.components) > 0:
            components = etree.SubElement(connections, 'components', {})
            for c in self.components: components.append(c.__to_element_tree())
            etree.SubElement(connections, 'extension', {}).text = self.extension

        if len(self.classQueries) + len(self.classAlterQueries) + len(self.mapNameXslt.keys()) > 0:
            queries = etree.SubElement(definition, 'queries', {})
            if len(self.classQueries) > 0:
                class_queries = etree.SubElement(queries, 'classQueries', {})
                for q in self.classQueries: class_queries.append(q.__to_element_tree())
            if len(self.classAlterQueries) > 0:
                class_alter_queries = etree.SubElement(queries, 'classAlterQueries', {})
                for q in self.classAlterQueries: class_alter_queries.append(q.__to_element_tree())
            if len(self.mapNameXslt.keys()) > 0:
                xslts = etree.SubElement(queries, 'xslts', {})
                for q in self.mapNameXslt.values(): xslts.append(q.__to_element_tree())

        validations = etree.SubElement(definition, 'validations', {})
        if self.xmlSchema is not None:
            xml_schema = etree.SubElement(validations, 'xmlSchema',
                                       {'scope': self.xmlSchemaScope if self.xmlSchemaScope is not None else 'inherit'})
            xml_schema.append(etree.fromstring(self.xmlSchema))
        if len(self.validators) > 0:
            validators = etree.SubElement(validations, 'validators', {})
            for v in self.validators: validators.append(v.__to_element_tree())
        if len(self.schematrons) > 0:
            schematrons = etree.SubElement(validations, 'schematrons', {})
            for s in self.schematrons: schematrons.append(s.__to_element_tree())

        if len(self.updaters) > 0:
            modificators = etree.SubElement(definition, 'modificators', {})
            updaters = etree.SubElement(modificators, 'updaters', {})
            for u in self.updaters: updaters.append(u.__to_element_tree())

        if self.metainf is not None:
            metainf = etree.SubElement(definition, 'metainf', {})
            metainf.append(etree.fromstring(self.metainf))

        return definition

    @staticmethod
    def __from_element_tree(root):
        """
        Restituisce un oggetto ClassBusiness effettuando il parsing di un xml.
        :param root:
        :rtype: Restituisce un oggetto di tipo ClassBusiness che rappresenta l'xml fornito in input
        """
        bsc = ClassBusiness()
        for child in root:
            if child.tag == 'references':
                for r in child:
                    if r.tag == 'name':
                        bsc.name = r.text
                    elif r.tag == 'description':
                        bsc.description = r.text
                    elif r.tag == 'owner':
                        bsc.owner = r.text
                    elif r.tag == 'version':
                        bsc.version = r.text
                    elif r.tag == 'labelVersion':
                        bsc.labelVersion = r.text
                    elif r.tag == 'update':
                        bsc.update = r.text
                    elif r.tag == 'creationDate':
                        bsc.creationDate = r.text
                    elif r.tag == 'preview':
                        bsc.preview = r.text
                    elif r.tag == 'sortEnabled':
                        bsc.sortEnabled = r.text
                    elif r.tag == 'abstract':
                        bsc.isAbstract = r.text
                    elif r.tag == 'viewQuery':
                        bsc.viewQuery = r.text
                    elif r.tag == 'metainfPolicy':
                        bsc.metainfPolicy = r.text
                    elif r.tag == 'aree':
                        for a in r:
                            bsc.aree.append(a.text)
                    elif r.tag == 'linkedBusiness':
                        for l in r:
                            bsc.linkedBusiness.append(l.text)
            elif child.tag == 'keys':
                for k in child:
                    bsc.keys.append(Key.from_element_tree(k))
            elif child.tag == 'connections':
                for con in child:
                    if con.tag == 'components':
                        for c in con:
                            bsc.components.append(Component.from_element_tree(c))
                    if con.tag == 'extension':
                        bsc.extension = con.text
            elif child.tag == 'queries':
                for que in child:
                    if que.tag == 'classQueries':
                        for q in que:
                            bsc.classQueries.append(Query.from_element_tree(q))
                    if que.tag == 'classAlterQueries':
                        for q in que:
                            bsc.classAlterQueries.append(Query.from_element_tree(q))
                    if que.tag == 'xslts':
                        for x in que:
                            xslt = Xslt.from_element_tree(x)
                            bsc.mapNameXslt[xslt.name] = xslt
            elif child.tag == 'validations':
                for val in child:
                    if val.tag == 'xmlSchema':
                        bsc.xmlSchema = etree.tostring(val[0], encoding=encoding) if len(val)>0 else None
                        if 'scope' in val.attrib:
                            bsc.xmlSchemaScope = val.attrib['scope']
                    if val.tag == 'validators':
                        for v in val:
                            bsc.validators.append(Validator.from_element_tree(v))
                    if val.tag == 'schematrons':
                        for s in val:
                            bsc.schematrons.append(Schematron.from_element_tree(s))
            elif child.tag == 'modificators':
                for mod in child:
                    if mod.tag == 'updaters':
                        for u in mod:
                            bsc.updaters.append(Updater.from_element_tree(u))
            elif child.tag == 'metainf':
                bsc.metainf = etree.tostring(child, encoding=encoding)

        return bsc

    def get_document(self,keys:'[]'=[],filter:'str'=None):
        if self.adapter is None: raise TidyException("variabile adapter non impostata")
        k=f"""({','.join([f"'{k}'" for k in keys])})""" if keys is not None else ''
        v=f":v({filter})" if filter is not None else ''
        q=f"!!{self.name}{k}{v}:r($references,$keys,$metainf)!!"
        s,sr=self.adapter.query(query=q)
        if sr.code != '0': raise TidyException(sr)
        list=[]
        for v in sr.xml:
            d=Document.from_element_tree(v, True)
            d.adapter=self.adapter
            d.class_business=self
            list.append(d)
        return list
