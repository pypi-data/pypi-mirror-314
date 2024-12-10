# -*- coding: utf-8 -*-
import csv as _csv
import os as _os
import heimdall
from ..decorators import get_database, create_database
from glob import glob as _glob


@get_database('csv')
def getDatabase(url, **options):
    r"""Imports a database from one or more CSV files

    :param \**options: Keyword arguments, see below.
    :return: HERA element tree
    :rtype: lxml.ElementTree

    :Keyword arguments:
        * **url** (``str``) -- Pattern of CSV files to read from

    .. ERROR::
       This feature is not implemented yet.

       Interested readers can submit a request to further this topic.
       See the ``CONTRIBUTING`` file at the root of the repository for details.
    """
    tree = heimdall.createDatabase()
    for path in _glob(url):
        _file2hera(tree, path, **options)
    return tree


def _file2hera(tree, url, **options):
    newline = ''
    header = options.get('header', True)
    comma = options.get('delimiter', ',')
    quote = options.get('quotechar', '"')
    pipe = options.get('multivalue', '|')
    eid = options.get('eid', _os.path.splitext(_os.path.basename(url))[0])
    with open(url, newline=newline) as f:
        reader = _csv.DictReader(f, delimiter=comma, quotechar=quote)
        columns = None
        for row in reader:
            if header and columns is None:
                columns = list(row.keys())
                _row2properties(tree, columns)
                _row2entity(tree, eid, columns)
            _row2item(tree, eid, row)
    return tree


def _row2properties(tree, header):
    properties = list()
    for column in header:
        properties.append(heimdall.createProperty(tree, id=column))
    return properties


def _row2entity(tree, eid, header):
    entity = heimdall.createEntity(tree, id=eid)
    for column in header:
        heimdall.createAttribute(entity, pid=column, id=column)
    return entity


def _row2item(tree, eid, row):
    heimdall.createItem(tree, eid=eid, **row)


@create_database('csv')
def serialize(tree, url, **options):
    r"""Serializes a HERA elements tree into CSV files

    :param tree: HERA elements tree
    :param url: Path to an existing directory
    :param \**options: (optional) Keyword arguments, see below.
    :Keyword arguments:
        * **header** (``bool``) -- (optional, default: ``True``)
          If ``True``, first line in each CSV is a header containing column
          names; if ``False``, first line will be the first item in ``tree``
        * **delimiter** (``str``) -- (optional, default: ``,``)
          CSV column delimiter
        * **quotechar** (``str``) -- (optional, default: ``"``)
          CSV "quoting character"; quotes will only be used if necessary
        * **multivalue** (``str``) -- (optional, default: ``|``)
          CSV multivalue delimiter

    This function can be used to export an HERA elements tree as CSV files.
    One CSV file is created per entity in ``tree``; this CSV has one column
    per attribute in this entity, and one line (excluding header if any)
    per item belonging to this entity in ``tree``.

    Each CSV file path will be ``<url>/<eid>.csv``, with ``eid`` being each
    entity's identifier in ``tree``.
    If a given entity doesn't have any attribute, the file will be empty.
    If no item belongs to this entity in ``tree``, the file will be empty,
    bar the header if any.
    """
    folder = url
    if not _os.path.isdir(folder):
        raise ValueError("Option 'path' must be a directory")

    header = options.get('header', True)
    comma = options.get('delimiter', ',')
    quote = options.get('quotechar', '"')
    pipe = options.get('multivalue', '|')

    for entity in heimdall.getEntities(tree):
        eid = entity.get('id')
        path = _os.path.join(folder, f'{eid}.csv')
        attributes = heimdall.getAttributes(entity)
        header = [_attr2col(a) for a in attributes]
        with open(path, 'w', newline='') as f:
            writer = _csv.writer(
                f,
                delimiter=comma,
                quotechar=quote,
                quoting=_csv.QUOTE_MINIMAL)
            if header:
                writer.writerow(header)
            items = heimdall.getItems(tree, lambda n: n.get('eid') == eid)
            for item in items:
                row = _item2row(item, attributes, pipe)
                writer.writerow(row)


def _attr2col(attribute):
    """Deduces column name from `attribute`

    :param attribute: HERA attribute element
    """
    name = attribute.get('id')
    if name is not None:
        return name
    name = attribute.get('pid')
    entity = attribute.getparent()
    if name is not None:
        eid = f"{entity.get('id')}." if entity is not None else ''
        return f'{eid}{name}'
    # NOTE: from here, an error could be raised IF we take into
    #       account that a pid is mandatory for each attribute
    #       and that this feature should only be used as part
    #       of the serialization process of valid HERA trees
    if entity is not None:
        attributes = heimdall.getAttributes(entity)
        index = attributes.index(attribute)
        return f"{entity.get('id')}.{index}"
    return "?"


def _item2row(item, attributes, pipe):
    """TODO

    :param item: HERA item element
    :param attributes: Attribute identifiers
    :param pipe: Multivalue separator
    """
    row = list()
    for a in attributes:
        aid = a.get('id')
        pid = a.get('pid')
        metadata = heimdall.getMetadata(item, aid=aid, pid=pid)
        value = pipe.join((m.text or '') for m in metadata)
        row.append(value)
    return row
