import os
import json
import jsonschema
import sys
import traceback
from copy import deepcopy
from io import StringIO
from pathlib import Path
from threading import Thread
from .errors import DeadlineExceeded, InvalidArgument, NotFound


# Path Utilities.
rootPath = Path(__file__).parent.resolve()
envsPath = Path.joinpath(rootPath, "envs")


def getEnvPath(*path):
    return Path.joinpath(envsPath, *path)


# Primative Utilities.
def get(o, classinfo=None, default=None, path=[], isCallable=None, fallback=None):
    if o == None and default != None:
        o = default
    if has(o, classinfo, default, path, isCallable):
        cur = o
        for p in path:
            cur = cur[p]
        return cur
    else:
        if default != None:
            return default
        return fallback


def has(o, classinfo=None, default=None, path=[], isCallable=None):
    try:
        cur = o
        for p in path:
            cur = cur[p]
        if classinfo != None and not isinstance(cur, classinfo):
            raise "Not a match"
        if isCallable == True and not callable(cur):
            raise "Not callable"
        if isCallable == False and callable(cur):
            raise "Is callable"
        return True
    except:
        if default != None and o != None and len(path) > 0:
            cur = o
            for p in path[:-1]:
                if not has(cur, dict, path=[p]):
                    cur[p] = {}
                cur = cur[p]
            cur[path[-1]] = default
        return False

def call(o, default=None, path=[], args=[], kwargs={}):
    o = get(o, default=False, path=path, isCallable=True)
    if o != False:
        return o(*args, **kwargs)
    else:
        return default

class Struct(dict):
    def __init__(self, **entries):
        entries = {k: v for k, v in entries.items() if k != "items"}
        dict.__init__(self, entries)
        self.__dict__.update(entries)

    def __setattr__(self, attr, value):
        self.__dict__[attr] = value
        self[attr] = value


def timeout(fn, *args, **kwargs):
    seconds = get(kwargs, int, 60, path=["seconds"])
    rtn = [DeadlineExceeded(f"Timed out after {seconds} seconds.")]

    def target():
        try:
            rtn[0] = fn(*args)
        except Exception as e:
            rtn[0] = e

    t = Thread(target=target)
    t.daemon = True
    try:
        t.start()
        t.join(seconds)
    except Exception as e:
        raise e
    if isinstance(rtn[0], BaseException):
        raise rtn[0]
    return rtn[0]


# Added benifit of cloning lists and dicts.
def structify(o):
    if isinstance(o, list):
        return [structify(o[i]) for i in range(len(o))]
    elif isinstance(o, dict):
        return Struct(**{k: structify(v) for k, v in o.items()})
    return o


# File Utilities.
def readFile(path, fallback=None):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except:
        if fallback != None:
            return fallback
        raise NotFound(f"{path} not found")


def getExec(raw, fallback=None):
    buffer = StringIO()
    sys.stdout = buffer
    try:
        codeObject = compile(raw, "<string>", "exec")
        env = {}
        exec(codeObject, env)
        sys.stdout = sys.__stdout__
        print(buffer.getvalue())
        return env
    except Exception as e:
        sys.stdout = sys.__stdout__
        print(buffer.getvalue())
        if fallback != None:
            return fallback
        raise InvalidArgument("Invalid raw Python: " + str(e))


def getCallable(raw, callables, fallback=None):
    try:
        local = getExec(raw)
        for c in callables:
            if has(local, path=[c], isCallable=True):
                return local[c]
        raise "Nope"
    except:
        if fallback != None:
            return fallback
        raise InvalidArgument("No callable found")


def get_last_callable(raw, fallback=None):
    try:
        local = getExec(raw)
        callables = [v for v in local.values() if callable(v)]
        if len(callables) > 0:
            return callables[-1]
        raise "Nope"
    except Exception as e:
        if fallback != None:
            return fallback
        raise InvalidArgument("No callable found")


def getFileCallable(path, callables, fallback=None):
    raw = readFile(path, fallback)
    return getCallable(raw, callables, fallback)


def getFileJson(path, fallback=None):
    try:
        with open(path, "r") as json_file:
            return json.load(json_file)
    except:
        if fallback != None:
            return fallback
        raise InvalidArgument(f"{path} does not contain valid JSON")


# Schema Utilities.
schemas = structify(getFileJson(Path.joinpath(rootPath, "schemas.json")))


def defaultSchema(schema, data):
    default = get(schema, path=["default"])
    if default == None and data == None:
        return

    if get(schema, path=["type"]) == "object":
        default = deepcopy(get(default, dict, {}))
        if data == None or not has(data, dict):
            obj = default
        else:
            obj = data
            for k, v in default.items():
                if not k in obj:
                    obj[k] = v
        properties = get(schema, dict, {}, ["properties"])
        for key, propSchema in properties.items():
            newValue = defaultSchema(propSchema, get(obj, path=[key]))
            if newValue != None:
                obj[key] = newValue
        return obj

    if get(schema, path=["type"]) == "array":
        default = deepcopy(get(default, list, []))
        arr = get(data, list, default)
        itemSchema = get(schema, dict, {}, ["items"])
        for index, value in enumerate(arr):
            if value == None and len(default) > index:
                newValue = default[index]
            else:
                newValue = defaultSchema(itemSchema, value)
            if newValue != None:
                arr[index] = newValue
        return arr

    return data if data != None else default


def validateSchema(schema, data):
    try:
        jsonschema.validate(data, schema)
        return None
    except Exception as err:
        traceback.print_exc()
        return str(err)


def processSchema(schema, data, useDefaultSchema=True):
    error = None
    if useDefaultSchema == True:
        data = defaultSchema(schema, deepcopy(data))
    try:
        jsonschema.validate(data, schema)
    except Exception as err:
        traceback.print_exc()
        error = str(err)
    return error, data


# Player utilities
def get_player(window_kaggle, renderer):
    key = "/*window.kaggle*/"
    value = f"""
window.kaggle = {json.dumps(window_kaggle, indent=2)};\n\n
window.kaggle.renderer = {renderer.strip()};\n\n
    """
    return readFile(Path.joinpath(rootPath, "static", "player.html")).replace(
        key, value
    )

