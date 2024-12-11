# # Create python xml structures compatible with
# # http://search.cpan.org/~grantm/XML-Simple-2.18/lib/XML/Simple.pm
# from __future__ import  unicode_literals
# from __future__ import print_function
#
# from lxml import etree
# from itertools import groupby
#
#
# # TODO: two copies of this code: here and in bq.metadoc.xmldict... eliminate one!
#
# def xml2d(e, attribute_prefix=None, group_lists=False, keep_tags=False):
#     """Convert an etree into a dict structure
#     """
#
#     def _get_tag(el):
#         if el.tag == 'tag' and not keep_tags:
#             return el.get('name', 'tag')
#         else:
#             return el.tag
#
#     def _xml2d(e):
#         # map attributes
#         if attribute_prefix is not None:
#             kids = dict(('%s%s' % (attribute_prefix, k) , v) for k,v in e.attrib.items() if e.tag != 'tag' or k != 'name' or keep_tags)
#         else:
#             kids = dict((k, v) for k,v in e.attrib.items() if e.tag != 'tag' or k != 'name' or keep_tags)
#         # map text
#         if e.text:
#             if len(e)==0 and len(kids) == 0:
#                 kids = e.text
#                 return kids
#             else:
#                 kids['%svalue' % attribute_prefix] = e.text
#         # map children
#         for k, g in groupby(sorted(e, key=lambda x: _get_tag(x)), key=lambda x: _get_tag(x)):
#             g = [ _xml2d(x) for x in g ]
#             if group_lists:
#                 g = ",".join (g)
#             kids[k] = g if len(g) > 1 else g[0]
#         return kids
#     return { _get_tag(e) : _xml2d(e) }
#
#
# def d2xml(d, attribute_prefix=None, keep_value_attr=False):
#     """convert dict to etree
#     """
#     assert isinstance(d, dict)
#
#     def _setval(node, val):
#         val = str(val)  # TODO: need to come up with better solution for numbers etc
#         if keep_value_attr:
#             node.set('value', val)
#         else:
#             node.text = val
#
#     def _d2xml(d, p):
#         for k,v in d.items():
#             if isinstance(v,dict):
#                 try:
#                     node = etree.SubElement(p, k)
#                 except ValueError:
#                     # illegal xml tag
#                     node = etree.SubElement(p, 'tag', name=k)
#                 _d2xml(v, node)
#             elif isinstance(v,list):
#                 for item in v:
#                     try:
#                         node = etree.SubElement(p, k)
#                     except ValueError:
#                     # illegal xml tag
#                         node = etree.SubElement(p, 'tag', name=k)
#                     if isinstance(item, dict):
#                         _d2xml(item, node)
#                     else:
#                         _setval(node, item)
#             else:
#                 if k == '%svalue' % attribute_prefix:
#                     _setval(p, v)
#                 else:
#                     if k.startswith(attribute_prefix):
#                         p.set(k.lstrip (attribute_prefix), v)
#                     else:
#                         try:
#                             node = etree.SubElement(p, k)
#                         except ValueError:
#                             # illegal xml tag
#                             node = etree.SubElement(p, 'tag', name=k)
#                         _setval(node, v)
#                 #p.set(k, v)
#
#     k,v = list(d.items())[0]
#     try:
#         node = etree.Element(k)
#     except ValueError:
#         # illegal xml tag
#         node = etree.Element('tag', name=k)
#     if isinstance(v, dict):
#         _d2xml(v, node)
#     else:
#         _setval(node, v)
#     return node
#
# # simple dictionary output of name-value pairs, useful for image metadata
# def xml2nv(e):
#     """Convert an etree into a dict structure
#
#     @type  e: etree.Element
#     @param e: the root of the tree
#     @return: The dictionary representation of the XML tree
#     """
#     def _xml2nv(e, a, path):
#         for g in e:
#             n = g.get('name', 'tag') if g.tag == 'tag' else g.tag
#             if n is None:
#                 continue
#             a['%s%s'%(path, n)] = g.text
#             for child in g:
#                 _xml2nv(child, a, '%s%s/'%(path, n))
#         return
#     a = {}
#     _xml2nv(e, a, '')
#     return a
#
# # if __name__=="__main__":
# #
# #     X = """<T uri="boo"><a n="1"/><a n="2"/><b n="3"><c x="y"/></b></T>"""
# #     print (X)
# #     Y = xml2d(etree.XML(X))
# #     print (Y)
# #     Z = etree.tostring (d2xml(Y), encoding='unicode')
# #     print (Z)
# #     assert X == Z
