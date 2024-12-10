# -*- coding: utf-8 -*-
import heimdall
import os as _os
import re as _re
from sys import version_info as _py
from urllib.parse import urlparse
from lxml import etree
from ..decorators import get_database, create_database
_python_version = (_py.major, _py.minor) >= (3, 8)
try:
    from mysql.connector import connect
    _installed = True
except ModuleNotFoundError:  # pragma: no cover
    _installed = False
except SyntaxError:  # pragma: no cover
    _python_version = False
LENGTH_PREFIX = 'len:'


def check_available():
    if not _python_version:
        version = '.'.join(str(n) for n in _py[:3])
        message = f"Python 3.8 or later required (found: {version})."
        raise ModuleNotFoundError(message)
    if not _installed:
        message = "Module 'mysql-connector-python' required."
        raise ModuleNotFoundError(message)
    return _installed and _python_version


@get_database(['sql:mariadb', 'sql:mysql', ])
def getDatabase(**options):
    r"""Loads a MySQL database as a HERA elements tree

    :param \**options: Keyword arguments, see below.
    :Keyword arguments:
        * **url** (``str``) -- URL of the database to load
        * **entities** (``list``) -- List of tables to load;
          empty list will do nothing

    Regarding SQL to HERA transformation, the following apply:

    * Each of the SQL table name in the ``entities`` option
      will be loaded as a single HERA entity.
    * Each column of a table will be loaded as a single HERA
      attribute, referencing a single HERA property.
      This means that, for example, two tables with the same
      ``id`` primary key column will become two different
      attribues, referencing two different properties.
      These properties can then be factorized using pyHeimdall.
      See :py:class:`heimdall.util.merge_properties` module for details.
    """
    check_available()  # breaks if not
    connection = _connect(options['url'])
    with connection.cursor() as cursor:
        hera = _create_tree(options['entities'], cursor)
    connection.close()
    return hera


def _connect(url):
    url = urlparse(url)
    # due to urlparse, url.path is something like '/dbname'
    # but mysql.connector.connect wants database = 'dbname'
    connection = connect(database=url.path.split('/')[1],
                         user=url.username, password=url.password,
                         host=url.hostname, port=url.port)
    # TBD: can connection.is_connected() be False here?
    return connection


def _create_tree(tables, cursor):
    root = heimdall.createDatabase()
    properties = root.xpath('//properties')[0]
    entities = root.xpath('//entities')[0]
    items = root.xpath('//items')[0]
    for table in tables:
        # create entity for this table
        entity, aid_vs_property = _create_entity(table, cursor)
        entities.append(entity)
        # create properties for this entity
        for p in aid_vs_property.values():
            properties.append(p)
        # create items for this entity
        eid = entity.get('id')
        result = cursor.execute(f'SELECT * FROM {table}')
        for row in cursor.fetchall():
            items.append(_create_item(eid, row, aid_vs_property))
    return root


def _create_item(eid, row, aid_vs_property):
    item = etree.Element('item', {'eid': eid, })
    for index, (aid, p) in enumerate(aid_vs_property.items()):
        value = row[index]
        if value is None:
            continue
        item.append(_create_metadata(value, aid=aid, pid=p.get('id')))
    return item


def _create_metadata(value, pid=None, aid=None):
    metadata = etree.Element('metadata')
    if aid is not None:
        metadata.set('aid', aid)
    if pid is not None:
        metadata.set('pid', pid)
    metadata.text = str(value)
    return metadata


def _create_entity(table, cursor):
    cursor.execute(f'SHOW CREATE TABLE {table}')
    create_table_query = cursor.fetchall()[0][1]
    entity = etree.Element('entity', {'id': table, })
    etree.SubElement(entity, 'name').text = table
    comment = _get_table_comment(create_table_query)
    if comment is not None:
        etree.SubElement(entity, 'description').text = comment
    pointers = _get_pointers(table, cursor)
    aid_vs_property = dict()
    cursor.execute(f'SHOW FULL COLUMNS FROM {table}')
    for row in cursor.fetchall():
        a = _create_attribute(row, table, pointers)
        entity.append(a)
        aid_vs_property[a.get('id')] = _create_property(table, row)
    return entity, aid_vs_property


def _get_table_comment(create_table_query):
    pattern = _re.compile(r"COMMENT='(?P<res>[\w\s]*)'")
    m = pattern.search(create_table_query)
    return m.group('res') if m is not None else None


def _get_pointers(source_table, cursor):
    """Gets pointer attributes for ``source_table``

    Each foreign key in ``source_table`` in SQL is a pointer in HERA.
    For example if ``SHOW CREATE TABLE source_table`` returns something such as
    ``FOREIGN KEY (`source_attr`) REFERENCES `target_table` (`target_attr`)``,
    then the attribute ``source_attr`` of entity ``source_table`` is a pointer
    to the content of attribute ``target_attr`` of entity ``target_table``.
    """
    cursor.execute(f'SHOW CREATE TABLE {source_table}')
    parts = cursor.fetchall()
    assert len(parts) == 1
    assert len(parts[0]) == 2
    assert parts[0][0] == source_table
    haystack = parts[0][1]
    needle = _re.compile(r"FOREIGN KEY \(`(?P<source_attr>\w+)`\) REFERENCES `(?P<target_table>\w+)` \(`(?P<target_attr>\w+)`\)", _re.IGNORECASE)  # nopep8: E501
    groups = needle.findall(haystack)
    pointers = dict()
    for match in groups:
        source_attr = f'{match[0]}_attr'
        target_table = match[1]
        target_attr = f'{match[2]}_attr'
        pointers[source_attr] = f'@{target_table}.{target_attr}'
    return pointers


def _create_attribute(row, table, pointers=None):
    # @see https://dev.mysql.com/doc/refman/8.4/en/show-columns.html
    name = row[0]
    sqltype = row[1]
    collation = row[2]
    nullability = row[3]  # YES|NO
    indexed = row[4]  # PRI|UNI|MUL
    default_value = row[5]
    extra = row[6]
    privileges = row[7]
    comment = row[8]
    root = etree.Element('attribute', {
        'id': f'{table}.{name}_attr', 'pid': f'{table}.{name}',
        'min': str(0) if nullability == 'YES' else str(1),
        'max': str(1),  # TODO hera allows repeatability, sql does not (as is)
        })
    pointers = pointers or dict()
    pointer_type = pointers.get(f'{name}_attr', None)
    if pointer_type is not None:
        etree.SubElement(root, 'type').text = pointer_type
    else:
        etree.SubElement(root, 'type').text = _type_sql2hera(sqltype)
    etree.SubElement(root, 'name').text = name
    if comment:
        etree.SubElement(root, 'description').text = comment
    return root


def _create_property(table, row):
    # @see https://dev.mysql.com/doc/refman/8.4/en/show-columns.html
    name = row[0]
    sqltype = row[1]
    comment = row[8]
    root = etree.Element('property', id=f'{table}.{name}')
    etree.SubElement(root, 'type').text = _type_sql2hera(sqltype)
    etree.SubElement(root, 'name').text = name
    if comment is not None:
        etree.SubElement(root, 'description').text = comment
    return root


def _type_sql2hera(sqltype):
    # NOTE: the following lines might allow python3.7 support
    # if type(sqltype) == bytes:
    #     try:
    #         import chardet  # happens with python3.7 or lower
    #         encoding = chardet.detect(sqltype)['encoding']
    #     except ModuleNotFoundError:
    #         encoding = 'ascii'
    #     sqltype = sqltype.decode(encoding)
    if (sqltype == 'date' or
            sqltype == 'datetime' or
            sqltype == 'timestamp'):
        return 'datetime'
    if (sqltype.startswith('varchar') or
            sqltype.startswith('char') or
            sqltype.startswith('tinytext')):
        return 'text'
    if (sqltype.startswith('int') or
            sqltype.startswith('tinyint')):
        return 'number'
    raise ValueError(f"Unknown type '{sqltype}'")


@create_database(['sql:mariadb', 'sql:mysql', ])
def dump(tree, url, **options):
    r"""Serialize a HERA elements tree into a MySQL dump like file

    :param tree: HERA elements tree
    :param url: Path of the MySQL dump file to create
    :param \**options: (optional) Keyword arguments, see below.
    :Keyword arguments:
        * **allow_multivalues** (``bool``) -- (optional, default: ``True``)
          If ``True`` multiple values for the same entity attribute will be
          put in the same SQL column, separated by ``multivalue_separator``.
          If ``False``, this function will raise an error
          should any attribute have a ``max`` greater than 1.
        * **multivalue_separator** (``str``) -- (optional, default: ``,``)
          "Character" separating multiple values for the same attribute
          in a given entity; used only if ``allow_multivalues`` is ``True``.
    """
    check_available()  # breaks if not
    path = url
    if _os.path.exists(path):
        raise ValueError(f"File '{path}' already exists")

    allow = options.get('allow_multivalues', False)
    allow = True  # TODO
    comma = options.get('multivalue_separator', ',')
    with open(path, 'w', newline='') as f:
        f.write(f"{_pre_everything()}\n")
        for entity in heimdall.getEntities(tree):
            eid = entity.get('id')
            attributes = heimdall.getAttributes(entity)
            items = heimdall.getItems(tree, lambda n: n.get('eid') == eid)
            f.write(f"\n{_pre_create_table(eid)}\n")
            f.write(f"{_create_table(tree, eid, attributes, allow)}\n")
            f.write(f"{_pre_dump_data(eid)}\n")
            f.write(f"{_dump_data(items, eid, attributes, comma)}\n")
            f.write(f"{_post_dump_data()}\n")


def _pre_everything():
    text = "-- SQL dump, from a HERA database, using pyHeimdall\n"
    text += "-- ------------------------------------------------------\n"
    text += f"-- pyHeimdall version	{heimdall.__version__}"
    return text


def _pre_create_table(eid, drop=True):
    comment = f"--\n-- Table structure for table `{eid}`\n--"
    drop_table = f"\nDROP TABLE IF EXISTS `{eid}`;" if drop else ""
    return comment + drop_table


def _create_table(tree, eid, attributes, allow_multivalues):
    text = f"CREATE TABLE `{eid}` (\n"
    for attribute in attributes:
        (aid, pid) = _get_identifiers(attribute)
        if aid is None and pid is None:
            continue  # this unused attribute won't be part of the dump
        _id = aid if aid is not None else pid
        max = attribute.get('max')
        max = int(max) if max else None
        if not allow_multivalues and (max is None or max > 1):
            fault = f"{eid}.{aid}.max={max}"
            raise ValueError(f"Repeatable attributes not supported ({fault})")
        min = int(attribute.get('min') or 0)
        min = "NOT NULL" if min > 0 else "DEFAULT NULL"
        type = _get_type(tree, attribute)
        text += f"`{_id}` {type} {min},\n"
    if text.endswith(',\n'):
        text = text[:-2] + '\n'  # remove last comma
    text += ") ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;"
    return text


def _get_identifiers(attribute):
    return (attribute.get('id'), attribute.get('pid'))


def _get_type(tree, attribute):
    type_node = heimdall.util.get_node(attribute, 'type')
    if type_node is not None:
        type_ = type_node.text
    else:
        pid = attribute.get('pid')
        property_ = heimdall.getProperty(tree, lambda n: n.get('id') == pid)
        type_node = heimdall.util.get_node(attribute, 'type')
        if type_node is not None:
            type_ = type_node.text
        else:
            type_ = 'text'
    if type_ == 'datetime':
        return 'date'
    if type_ == 'number':
        return 'int'  # TODO unsigned
    rules = heimdall.util.get_nodes(attribute, 'rule')
    length = 255
    for rule in rules:
        if rule.text.startswith(LENGTH_PREFIX):
            length = int(rule.text[len(LENGTH_PREFIX):])
    if length > 1:
        return f'varchar({length})'
    return 'char(1)'


def _pre_dump_data(eid, lock=True):
    comment = f"--\n-- Dumping data for table `{eid}`\n--"
    lock_table = f"\nLOCK TABLE `{eid}` WRITE;" if lock else ""
    return comment + lock_table


def _dump_data(items, eid, attributes, multivalues_separator):
    if len(items) == 0:
        return f"-- No data in table `{eid}`"
    text = f"INSERT INTO `{eid}` VALUES "
    dumps = list()
    for item in items:
        values = list()
        for attribute in attributes:
            values.append(_dump_value(item, attribute, multivalues_separator))
        dumps.append(f"({','.join(values)})")
    text += ','.join(dumps)
    text += ";"
    return text


def _dump_value(item, attribute, multivalues_separator):
    (aid, pid) = _get_identifiers(attribute)
    values = list()
    if aid is not None:
        if pid is not None:
            values = heimdall.getValues(item, pid=pid, aid=aid)
        else:
            values = heimdall.getValues(item, aid=aid)
    else:
        if pid is not None:
            values = heimdall.getValues(item, pid=pid)
    values = [f"'{v}'" for v in values]
    if len(values) < 1:
        return 'NULL'
    return multivalues_separator.join(values)


def _post_dump_data(lock=True):
    return "UNLOCK TABLES;"
