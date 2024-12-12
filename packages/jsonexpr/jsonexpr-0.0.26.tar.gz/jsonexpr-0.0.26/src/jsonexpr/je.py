__copyright__ = "Copyright 2024 Mark Kim"
__license__ = "Apache 2.0"
__version__ = "0.0.26"
__author__ = "Mark Kim"

import re
import os
import json
import wasmer
import wasmer_compiler_cranelift


##############################################################################
# PUBLIC FUNCTIONS

def eval(code, symbols=None):
    compiled = compile(str(code)) 

    if symbols is not None:
        compiled.setSymbols(symbols)

    return compiled.eval()

def evalfd(fd, symbols=None):
    code = fd.read()

    return eval(code, symbols)

def compile(code):
    return Compiled(code)

def compilefd(fd):
    code = fd.read()

    return compile(code)


##############################################################################
# HELPER CLASSES

class Compiled:
    def __init__(self, code):
        scriptdir = os.path.dirname(__file__)
        wasmfile = os.path.join(scriptdir, "je.wasm")

        # Setup
        with open(wasmfile, mode="rb") as fd:
            self.store = wasmer.Store()
            self.module = wasmer.Module(self.store, fd.read())

        self.iface = Interface()
        self.instance = wasmer.Instance(self.module, {
            "env": {
                "read"   : wasmer.Function(self.store, self.iface.read),
                "write"  : wasmer.Function(self.store, self.iface.write),
                "_exit"  : wasmer.Function(self.store, self.iface._exit),
            }
        })
        self.iface.memory8 = self.instance.exports.memory.uint8_view()
        self.util = Util(self.instance)
        self.wsymtbl = self.util.symnew()

        # Parse
        self.code = self.util.strdup(code)
        self.wtree = self.util.parse(self.code)

    def eval(self):
        wresult = self.util.eval(self.wtree, self.wsymtbl)
        wquoted = self.util.valqstr(wresult)
        quoted = self.util.strat(wquoted)
        result = json_loads(quoted, self.instance, wresult)

        self.util.valfree(wresult)

        return result

    def __contains__(self, name):
        wname = self.util.strdup(name)
        result = self.util.symget(self.wsymtbl, wname)

        self.util.free(wname)

        return result != 0
    
    def __getitem__(self, name):
        jstr = self.getJson(name)
        wname = self.util.strdup(name)
        wsymval = self.util.symget(self.wsymtbl, wname)

        self.util.free(wname)

        return json_loads(jstr, self.instance, wsymval)
    
    def __setitem__(self, name, value):
        self.setJson(name, json_dumps(value))

    def __delitem__(self, name):
        wname = self.util.strdup(name)

        self.util.symunset(self.wsymtbl, wname)
        self.util.free(wname)

    def setSymbols(self, symbols):
        for key,value in symbols.items():
            self.setJson(key, json_dumps(value))

    def clearSymbols(self, localonly=1):
        self.util.symclear(self.wsymtbl, localonly)

    def setJson(self, name, jstr):
        # Verify name is an identifier
        if not re.match(r"^[_a-zA-Z][_a-zA-Z0-9]*$", name, re.MULTILINE):
            raise SyntaxError(f"Identifier expected, got `{name}`")

        expr = f"{name} = {jstr};"
        wexpr = self.util.strdup(expr)
        wtree = self.util.parse(wexpr)
        wresult = self.util.eval(wtree, self.wsymtbl)

        self.util.nodefree(wtree)
        self.util.valfree(wresult)
        self.util.free(wexpr)

    def getJson(self, name):
        wname = self.util.strdup(name)
        wresult = self.util.symget(self.wsymtbl, wname)
        wstr = self.util.valqstr(wresult)
        jstr = self.util.strat(wstr)

        self.util.free(wname)

        return jstr

    def nodetree(self):
        return self.util.nodetree(self.wtree)

class Interface:
    def read(self, fd:"i32", buf:"i32", count:"i32") -> "i32":
        data = os.read(fd, count)
        count = len(data)
        self.memory8[buf:buf+count] = data

        return count

    def write(self, fd:"i32", buf:"i32", count:"i32") -> "i32":
        return os.write(fd, bytearray(self.memory8[buf:buf+count]))

    def _exit(self, status:"i32") -> None:
        raise Exit(status)

class Util:
    def __init__(self, instance):
        self.memory8 = instance.exports.memory.uint8_view()
        self.instance = instance
        self.allocated = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        for waddr in self.allocated:
            self.instance.exports.free(waddr)

        self.allocated = []

    def strat(self, waddr):
        len = 0

        while(self.memory8[waddr+len] != 0):
            len += 1

        return bytearray(self.memory8[waddr:waddr+len]).decode("utf-8")

    def strdup(self, string):
        encoded = string.encode("utf-8")
        waddr = self.instance.exports.calloc(1, len(encoded)+1)
        self.memory8[waddr:waddr+len(string)] = encoded
        self.memory8[waddr+len(encoded)] = 0

        self.allocated += [waddr]

        return waddr

    def free(self, waddr):
        if waddr in self.allocated:
            self.allocated.remove(waddr)

        self.instance.exports.free(waddr)

    def parse(self, wcode):
        return self.instance.exports.je_parse(wcode)

    def eval(self, wtree, wsymtbl):
        return self.instance.exports.je_eval(wtree, wsymtbl)

    def nodefree(self, wnode):
        self.instance.exports.je_freenode(wnode)

    def nodetree(self, wnode):
        wtree = self.instance.exports.je_nodetree(wnode)
        tree = self.strat(wtree)

        self.free(wtree)

        return tree

    def strval(self, wstr):
        return self.instance.exports.je_strval(wstr)

    def symnew(self, wsymtbl=0):
        return self.instance.exports.je_newtable(wsymtbl)

    def symget(self, wsymtbl, wkey):
        return self.instance.exports.je_tableget(wsymtbl, wkey)

    def symclear(self, wsymtbl, localonly=1):
        return self.instance.exports.je_tableclear(wsymtbl, localonly)

    def mapset(self, wmap, wkey, wval):
        return self.instance.exports.je_mapset(wmap, wkey, wval)

    def mapunset(self, wmap, wkey):
        self.instance.exports.je_mapunset(wmap, wkey)

    def mapget(self, wmap, wkey):
        return self.instance.exports.je_mapget(wmap, wkey)

    def mapkey(self, wmap):
        return self.instance.exports.je_mapkey(wmap)

    def mapnext(self, wmap):
        return self.instance.exports.je_mapnext(wmap)

    def vecset(self, wvec, index, wval):
        return self.instance.exports.je_vecset(wvec, index, wval)

    def vecpush(self, wvec, wval):
        return self.instance.exports.je_vecpush(wvec, wval)

    def vecunset(self, wvec, index):
        self.instance.exports.je_vecunset(wvec, index)

    def vecget(self, wvec, index):
        return self.instance.exports.je_vecget(wvec, index)

    def veclen(self, wvec):
        return self.instance.exports.je_veclen(wvec)

    def valbool(self, wval):
        return self.instance.exports.je_boolval(wval)

    def valint(self, wval):
        return self.instance.exports.je_intval(wval)

    def valdbl(self, wval):
        return self.instance.exports.je_dblval(wval)

    def valmap(self, wval):
        if(wval): return self.instance.exports.je_getobject(wval)
        else: return self.instance.exports.je_objval(0)

    def valvec(self, wval):
        if(wval): return self.instance.exports.je_getarray(wval)
        else: return self.instance.exports.je_arrval(0)

    def valstr(self, wval):
        return self.instance.exports.je_valstr(wval)

    def valqstr(self, wval):
        return self.instance.exports.je_valqstr(wval)

    def valfree(self, wresult):
        self.instance.exports.je_freeval(wresult)

def _wvalue(instance, value):
    with Util(instance) as util:
        if   isinstance(value, bool):
            wvalue = util.valbool(value)
        elif isinstance(value, int):
            wvalue = util.valint(value)
        elif isinstance(value, float):
            wvalue = util.valdbl(value)
        elif isinstance(value, list):
            wvalue = util.valvec(0)
            warray = util.valvec(wvalue)

            for i in range(len(value)):
                item = value[i]
                (wval, pval) = _wvalue(instance, item)

                util.vecpush(warray, wval)
                value[i] = pval

            value = Array(value, instance, warray)

        elif isinstance(value, dict):
            wvalue = util.mapvec(0)
            wobject = util.valmap(wvalue)

            with Util(instance) as util:
                for k,v in value.items():
                    wk = util.strdup(str(k))
                    (wv, v2) = _wvalue(instance, v)

                    util.mapset(wobject, wk, wv)
                    value[k] = v2

            value = Object(value, instance, wobject)

        else:
            value = str(value)
            wstr = util.strdup(value)
            wvalue = util.strval(wstr)

    return (wvalue, value)

class Object(dict):
    def __init__(self, obj, instance, wsymmap):
        super().__init__(obj)
        self.__instance = instance
        self.__wsymmap = wsymmap

    def __setitem__(self, name, value):
        with Util(self.__instance) as util:
            wname = util.strdup(str(name))
            (wvalue, pvalue) = _wvalue(self.__instance, value)

            util.mapset(self.__wsymmap, wname, wvalue)

        return super().__setitem__(name, pvalue)

    def __delitem__(self, name):
        with Util(self.__instance) as util:
            wname = util.strdup(name)

            util.mapunset(self.__wsymmap, wname)

        return super().__delitem__(name)

class Array(list):
    def __init__(self, array, instance, wsymvec):
        super().__init__(array)
        self.__instance = instance
        self.__wsymvec = wsymvec

    def __setitem__(self, index, value):
        (wvalue, pvalue) = _wvalue(self.__instance, value)

        with Util(self.__instance) as util:
            util.vecset(self.__wsymvec, index, wvalue)

        return super().__setitem__(index, pvalue)

    def __delitem__(self, index):
        with Util(self.__instance) as util:
            util.vecunset(self.__wsymvec, index)

        return super().__delitem__(index)


##############################################################################
# HELPER FUNCTIONS

def json_dumps(value):
    return json.dumps(value, default=str)

def json_loads(jstr, instance, symval):
    result = json.loads(jstr)

    return _enrich(result, instance, symval)

def _enrich(value, instance, symval):
    if   isinstance(value, dict):
        with Util(instance) as util:
            symmap = util.valmap(symval)

            for k,v in value.items():
                wname = util.strdup(k)
                wsymval = util.mapget(symmap, wname)
                value[k] = _enrich(v, instance, wsymval)

            value = Object(value, instance, symmap)

    elif isinstance(value, list):
        with Util(instance) as util:
            symvec = util.valvec(symval)

            for i in range(len(value)):
                wsymval = util.vecget(symvec, i)
                value[i] = _enrich(value[i], instance, wsymval)

            value = Array(value, instance, symvec)

    return value


##############################################################################
# EXCEPTIONS

class JeException(Exception):
    pass

class SyntaxError(JeException):
    def __init__(self, text):
        self.text = text

class Exit(JeException):
    def __init__(self, code):
        self.code = code


##############################################################################
# TEST CODE

if __name__ == "__main__":
    import sys
    import errno

    def main():
        compiled = compile("""
            PRINT("I have " + LEN(grades) + " students");
            PRINT("Alice's grade is " + grades.alice);
        """)

        compiled.setSymbols({
            "grades" : {
                "alice" : "A",
                "bob"   : "B",
            },
        #     "nested" : {
        #         "alice" : {
        #             "grade"     : [ "A", "B", "C" ],
        #             "last_name" : "Smith",
        #         },
        #         "bob"   : {
        #             "grade"     : "B",
        #             "last_name" : "Johnson",
        #         },
        #     },
        })

        result = compiled.eval()

        # compiled["nested"]["alice"]["grade"] = [ 1, 3, 2 ]
        # compiled["nested"]["alice"]["grade"][1] = {
        #     "a" : True,
        #     "b" : True,
        #     "c" : False,
        # }
        # compiled["nested"]["alice"]["grade"][1]["b"] = "Hello!"
        # compiled["nested"]["alice"]["grade"] = {
        #     "a" : "b",
        #     "c" : "d",
        # }
        # print("hello" in compiled)
        # print("grades" in compiled)
        print(json.dumps(compiled["grades"], indent=2))

        # print(type(result), result)

    try:
        main()
    except Exit as e:
        sys.exit(e.code)
    except KeyboardInterrupt:
        print("")
        sys.exit(errno.EOWNERDEAD)


# vim:ft=python:
