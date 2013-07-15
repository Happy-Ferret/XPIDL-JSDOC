#!/usr/bin/env python
# header.py - Generate C++ header files from IDL.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Print a C++ header file for the IDL files specified on the command line"""

import sys, os.path, re, xpidl, itertools, glob

printdoccomments = False

if printdoccomments:
    def printComments(fd, clist, indent):
        for c in clist:
            fd.write("%s%s\n" % (indent, c))
else:
    def printComments(fd, clist, indent):
        pass

def firstCap(str):
    return str[0].upper() + str[1:]

def attributeParamName(a):
    return "a" + firstCap(a.name)

def attributeParamNames(a):
    l = [attributeParamName(a)]
    if a.implicit_jscontext:
        l.insert(0, "cx")
    return ", ".join(l)

def attributeNativeName(a, getter):
    binaryname = a.binaryname is not None and a.binaryname or a.name
    return "%s%s" % (getter and '' or '', binaryname)

def attributeReturnType(a, macro):
    """macro should be NS_IMETHOD or NS_IMETHODIMP"""
    if (a.nostdcall):
        return macro == "NS_IMETHOD" and "virtual nsresult" or "nsresult"
    else:
        return macro

def attributeParamlist(a, getter):
    l = ["%s%s" % (a.realtype.nativeType(getter and 'out' or 'in'),
                   attributeParamName(a))]
    if a.implicit_jscontext:
        l.insert(0, "JSContext* cx")

    return ", ".join(l)

def attributeAsNative(a, getter):
        deprecated = a.deprecated and "NS_DEPRECATED " or ""
        params = {'deprecated': deprecated,
                  'returntype': attributeReturnType(a, 'NS_IMETHOD'),
                  'binaryname': attributeNativeName(a, getter),
                  'paramlist': attributeParamlist(a, getter)}
        return "%(deprecated)s%(returntype)s %(binaryname)s(%(paramlist)s)" % params

def methodNativeName(m):
    return m.binaryname is not None and m.binaryname or firstCap(m.name)

def methodReturnType(m, macro):
    """macro should be NS_IMETHOD or NS_IMETHODIMP"""
    if m.nostdcall and m.notxpcom:
        return "%s%s" % (macro == "NS_IMETHOD" and "virtual " or "",
                         m.realtype.nativeType('in').strip())
    elif m.nostdcall:
        return "%snsresult" % (macro == "NS_IMETHOD" and "virtual " or "")
    elif m.notxpcom:
        return "%s_(%s)" % (macro, m.realtype.nativeType('in').strip())
    else:
        return macro

def methodAsNative(m):
    return "%s %s(%s)" % (methodReturnType(m, 'NS_IMETHOD'),
                          methodNativeName(m),
                          paramlistAsNative(m))

def paramlistAsNative(m, empty='void'):
    l = [paramAsNative(p) for p in m.params]

    if m.implicit_jscontext:
        l.append("JSContext* cx")

    if m.optional_argc:
        l.append('uint8_t _argc')

    if not m.notxpcom and m.realtype.name != 'void':
        l.append(paramAsNative(xpidl.Param(paramtype='out',
                                           type=None,
                                           name='_retval',
                                           attlist=[],
                                           location=None,
                                           realtype=m.realtype)))

    if len(l) == 0:
        return empty

    return ", ".join(l)

def paramAsNative(p):
    return "%s%s" % (p.nativeType(),
                     p.name)

def paramlistNames(m):
    names = [p.name for p in m.params]

    if m.implicit_jscontext:
        names.append('cx')

    if m.optional_argc:
        names.append('_argc')

    if not m.notxpcom and m.realtype.name != 'void':
        names.append('_retval')

    if len(names) == 0:
        return ''
    return ', '.join(names)

header = """/*
 * DO NOT EDIT.  THIS FILE IS GENERATED FROM %(filename)s
 */
"""

include = """
"""

jspubtd_include = """
"""

infallible_includes = """
"""

header_end = """/* For IDL files that don't want to include root IDL files. */
"""

footer = """
"""

forward_decl = """"""

def idl_basename(f):
    """returns the base name of a file with the last extension stripped"""
    return os.path.basename(f).rpartition('.')[0]

def print_header(idl, fd, filename):

    for p in idl.productions:
        if p.kind == 'interface':
            write_interface(p, fd)
            continue

    fd.write(footer % {'basename': idl_basename(filename)})

iface_header = r""""""

uuid_decoder = re.compile(r"""(?P<m0>[a-f0-9]{8})-
                              (?P<m1>[a-f0-9]{4})-
                              (?P<m2>[a-f0-9]{4})-
                              (?P<m3>[a-f0-9]{4})-
                              (?P<m4>[a-f0-9]{12})$""", re.X)

iface_prolog = """"""

iface_epilog = """"""


iface_forward = """"""

iface_forward_safe = """"""

iface_template_prolog = """

/* Use the code below as a template for the implementation class for this interface. */

/** 
 * %(implclass)s IDL
 * @typedef {Object} %(implclass)s
"""

example_tmpl = """ * @property %(nativeName)s %(memberIDL)s
"""

iface_template_epilog = """*/
var %(implclass)s = {};
"""

attr_infallible_tmpl = """"""

def write_interface(iface, fd):
    if iface.namemap is None:
        raise Exception("Interface was not resolved.")


    defname = iface.name.upper()
    if iface.name[0:2] == 'ns':
        defname = 'NS_' + defname[2:]

    names = uuid_decoder.match(iface.attributes.uuid).groupdict()
    m3str = names['m3'] + names['m4']
    names['m3joined'] = ", ".join(["0x%s" % m3str[i:i+2] for i in xrange(0, 16, 2)])

    implclass = iface.name

    names.update({'defname': defname,
                  'macroname': iface.name.upper(),
                  'name': iface.name,
                  'iid': iface.attributes.uuid,
                  'implclass': implclass})

#    fd.write(iface_header % names)
    fd.write(iface_template_prolog % names)

    for member in iface.members:
        if isinstance(member, xpidl.ConstMember) or isinstance(member, xpidl.CDATA): continue
        # fd.write("/* %s */\n" % member.toIDL())
        if isinstance(member, xpidl.Attribute):
            fd.write(example_tmpl % {'implclass': implclass,
                                     'returntype': attributeReturnType(member, 'NS_IMETHODIMP'),
                                     'nativeName': attributeNativeName(member, True),
                                     'paramList': attributeParamlist(member, True),
                                     'memberIDL':member.toIDL()
                                     })
        elif isinstance(member, xpidl.Method):
            fd.write(example_tmpl % {'implclass': implclass,
                                     'returntype': methodReturnType(member, 'NS_IMETHODIMP'),
                                     'nativeName': methodNativeName(member),
                                     'paramList': paramlistAsNative(member, empty=''),
                                     'memberIDL':member.toIDL()})
        # fd.write('\n')

    fd.write(iface_template_epilog % names)

if __name__ == '__main__':
    from optparse import OptionParser
    o = OptionParser()
    o.add_option('-I', action='append', dest='incdirs', default=['.'],
                 help="Directory to search for imported files")
    o.add_option('--cachedir', dest='cachedir', default=None,
                 help="Directory in which to cache lex/parse tables.")
    o.add_option('-o', dest='outfile', default=None,
                 help="Output file (default is stdout)")
    o.add_option('-d', dest='depfile', default=None,
                 help="Generate a make dependency file")
    o.add_option('--regen', action='store_true', dest='regen', default=False,
                 help="Regenerate IDL Parser cache")
    options, args = o.parse_args()
    file = args[0] if args else None

    if options.cachedir is not None:
        if not os.path.isdir(options.cachedir):
            os.mkdir(options.cachedir)
        sys.path.append(options.cachedir)

    # The only thing special about a regen is that there are no input files.
    if options.regen:
        if options.cachedir is None:
            print >>sys.stderr, "--regen useless without --cachedir"
        # Delete the lex/yacc files.  Ply is too stupid to regenerate them
        # properly
        for fileglobs in [os.path.join(options.cachedir, f) for f in ["xpidllex.py*", "xpidlyacc.py*"]]:
            for filename in glob.glob(fileglobs):
                os.remove(filename)

    # Instantiate the parser.
    p = xpidl.IDLParser(outputdir=options.cachedir)

    if options.regen:
        sys.exit(0)

    if options.depfile is not None and options.outfile is None:
        print >>sys.stderr, "-d requires -o"
        sys.exit(1)

    if options.outfile is not None:
        outfd = open(options.outfile, 'w')
        closeoutfd = True
    else:
        outfd = sys.stdout
        closeoutfd = False

    idl = p.parse(open(file).read(), filename=file)
    idl.resolve(options.incdirs, p)
    print_header(idl, outfd, file)

    if closeoutfd:
        outfd.close()

    if options.depfile is not None:
        dirname = os.path.dirname(options.depfile)
        if dirname:
            try:
                os.makedirs(dirname)
            except:
                pass
        depfd = open(options.depfile, 'w')
        deps = [dep.replace('\\', '/') for dep in idl.deps]

        print >>depfd, "%s: %s" % (options.outfile, " ".join(deps))
