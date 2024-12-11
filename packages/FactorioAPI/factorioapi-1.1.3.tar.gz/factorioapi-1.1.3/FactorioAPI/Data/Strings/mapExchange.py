from io import BytesIO
import json
import string
from FactorioAPI.Data.IO.read import *
from FactorioAPI.Data.IO.write import *
import zlib
import base64


def readAutoplaceControls(f: io.BufferedReader | io.BytesIO):
    def keyDecoder(f: io.BufferedReader | io.BytesIO):
        print(
            hex(14 * (f.tell() // 14))[2:], ",", hex(f.tell() % 14)[2:], ",", f.tell()
        )
        return readString(f, spaceOptimized=True)

    def valueDecoder(f: io.BufferedReader | io.BytesIO):
        return {
            "frequency": readFloat(f),
            "size": readFloat(f),
            "richness": readFloat(f),
        }

    controls = readDict(f, keyDecoder, valueDecoder, spaceOptimized=True)
    return controls


def readMapGenSettings(f: io.BufferedReader | io.BytesIO):
    mapSettings = dict()
    # print(f.tell())
    # print(f.read(1))
    # print(f.read(1))
    print(f.read(1))
    # mapSettings["terrain_segmentation"] = readByte(f)
    # mapSettings["water"] = readByte(f)
    mapSettings["autoplace_controls"] = readAutoplaceControls(f)
    mapSettings["Unknown1"] = f.read(2).hex()
    mapSettings["seed"] = readUInt(f)
    mapSettings["width"] = readUInt(f)
    mapSettings["height"] = readUInt(f)
    mapSettings["starting_area"] = readByte(f)
    mapSettings["peaceful_mode"] = readBool(f)
    return mapSettings


def readMapSettings(exchangeString):
    """this expects the map exchange string, including the >>> and <<< that surround it"""

    binaryData = base64.b64decode(exchangeString[3:-3])
    try:
        binaryData = zlib.decompress(binaryData)
    except:
        None
    with open("meow.bin", "wb") as f:
        f.write(binaryData)
    buffer = BytesIO(binaryData)

    mapSettings = dict()

    mapSettings["Version"] = readVersionString(buffer)
    mapSettings["MapGenSettings"] = readMapGenSettings(buffer)
    # mapSettings["MapGenSettings"] = readMapGenSettings(buffer)

    mapSettings["checksum"] = readUInt(buffer)
    print(buffer.tell())
    buffer.read()
    print(buffer.tell())
    return mapSettings


settings = readMapSettings(
    ">>>eNp1Ur+LE0EUnrm43Jm7aJAgCMeZ4toInhYWkh0FERH9F9bJZrIObnbi/IhGC1Ncp2Jjo43X2lxnYXcoiIJCOLGwO7GxUIko2ghxJpvZ7G7iwLz99n1v3nvfm1kAAJQABGC1jK8rGjLP56pJPEZDAPqu3Ys+Dn0qSdq3z2c4E1T0WadDeI3xTNz+ccZaLmORRKTdqzWwyASXWqFinEbE65JIZhkVBoxjzw9pq5VmDlqGihBHTZHmloOQNOacKcf+cRNevomVmOzobHJeNiFZROb4b2BJeNq/RDmL8vMohVRepartNYzOTN0Iqy4Vs906nPnXMp04wue4k/YcFhJzSaPAw5xgr82okCpb2ZlpvCJU2FKc+h72adMLSE9kFTiSE5KpvCJVFAhJIi+na1lxHGldM3q7KvRxpLSu3IM5lDBdZgAV7UztmXkC2Lt7c7e/uQbMHt0B1dHIbI329EM2G8B+HA210y5nMlFQPaP32Wk6CG9Xts9/uvXQhXHkMTQBw4lnp2E9Fyy4jP5LrVtwMpXnxHj9TIG4qNQlJlFLaApictOQEN7/9mzrz6tBHf59+mP3UuOKC4+fq3wfbmzXNblo5C4k5vEjs55bKcDm3HMn1EcXvntr1lcXOuZExRh0SpudiwUAywc02rqnTXUV2NbqNk0FwdZ4/bZKPlvw3s3r0IM4bZKvGfPamHHBpDMYQ/QAQXTUskemIfr8Bkj30JwqfGPLvkzVzzUyexFpHTnPOppzDUVTsJmYL4WkGz3PwaL9Q08QLBhgon5pX/xnGJsq/pbReNyF5FEO3exLM8AkeTEIPvwD2sk5+w==<<<"
)

with open("meow.json", "w") as f:
    f.write(json.dumps(settings, indent=4))
