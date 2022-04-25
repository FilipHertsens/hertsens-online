"""
Demo Client using b.Alert API over HTTP

Making API calls over REST

Format:
http://api.balert.net/?method=balert.all_devices&api_key=X&user=U&time_stamp=T&nonce=N&hash=H

    api_key 		X = obtained API key, a b64 encoded integer of 128 bits => 0123456789ABCDEF0123456789ABCDEF
    user 			U = b64 encoded user name, the login name test@test.be  => dGVzdEB0ZXN0LmJl
    time_stamp 		T = seconds since 2012-01-01 00:00:00 UTC => may deviate up to 5 minutes from the real UTC
    nonce			N = 16 byte long string => must be unique over the last 15 minutes or will be rejected
    hash			H = sha1(X+U+P+T+nonce)

    P = sha1(password).hexdigest() 	with lower case

    api_key will unlock a particular set of functionality and may cause a rejection of the call

Typical responses:

    stat="fail"
    failcode = 1 	reason="invalid api key"
    failcode = 2	reason="functionality not bound to api key"
    failcode = 3	reason="repeated nonce"
    failcode = 4	reason="invalid time stamp"
    failcode = 5	reason="invalid hash"
    failcode = 6	reason="insufficient number of arguments"
    failcode = 7 	reason="over quota"

"""

_DEBUG_LEVEL = 1

import http.client
import base64
def _total_seconds(td):
    try:
        return td._total_seconds()
    except:
        return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6

def mapToXmlAttributes( mapping ):
    from xml.sax.saxutils import escape
    from xml.sax.saxutils import quoteattr
    xmlRow = []
    for name,value in mapping.items():
        valueStr = escape(quoteattr(str(value)))
        xmlRow.append('%(name)s=%(valueStr)s ' % vars())
    return '\n'.join(xmlRow)


class BAlertClient:
    def __init__(self, server, api_key, api_key_secret, port=8080):
        self.server = server
        self.port = port
        self.api_key = api_key
        self.api_key_secret = api_key_secret
        self.nonces = 0

    def _dataFromQuery( self, query ):
        if _DEBUG_LEVEL>0:
            pass
            #print("_dataFromQuery", query)
            ##print("Querying ", (self.server, self.port))
        conn = http.client.HTTPConnection(self.server, self.port)
        conn.request("GET", query)
        r1 = conn.getresponse()
        if _DEBUG_LEVEL>0:
            pass
            #print("_dataFromQuery response", r1)
        if r1.status!=200:
            raise RuntimeError("Call to balert API failed")
        data = r1.read()
        return data

    def _putQuery( self, query ):
        if _DEBUG_LEVEL>0:
            pass
            #print("_putQuery", query)
        conn = http.client.HTTPConnection(self.server, self.port)
        conn.putrequest("PUT", query)
        r1 = conn.getresponse()
        if _DEBUG_LEVEL>0:
            pass
            #print("_putQuery response", r1)
        if r1.status!=200:
            raise RuntimeError("Call to balert API failed")
        data = r1.read()
        return data

    def _postQuery( self, query, data ):
        if _DEBUG_LEVEL>0:
            pass
            #print("_postQuery", query)
        conn = http.client.HTTPConnection(self.server, self.port)
        request = conn.putrequest("POST", query)
        conn.putheader('Content-Type','application/xml')
        conn.putheader('Content-Length', str(len(data)))
        conn.endheaders()
        conn.send( data )
        r1 = conn.getresponse()
        if _DEBUG_LEVEL>0:
            pass
            #print("_postQuery response", r1)
        if r1.status!=200:
            raise RuntimeError("Call to balert API failed")
        data = r1.read()
        return data

    def getVehicles( self, user, password ):
        """
        get all the vehicles for given user with given password
        Returns the XML answer from server.  Throws a RuntimeError when the call fails (for instance, server cannot be contacted).
        """
        time_stamp = self._generateTimestamp()
        nonce = self._generateNonce()
        hash = self._generateHash(password.encode(), time_stamp, nonce )
        api_key = self.api_key
        user = base64.b64encode(user.encode())
        user = user.decode('utf-8')
        urlQuery = "/?method=balert.tpms.vehicles.get&user=%(user)s&api_key=%(api_key)s&time_stamp=%(time_stamp)d&nonce=%(nonce)s&hash=%(hash)s" % vars()
        print(urlQuery)
        return self._dataFromQuery( urlQuery )

    def getTires( self, user, password, optionalFilter="" ):
        """
        get all the tires for given user with given password
        Returns the XML answer from server.  Throws a RuntimeError when the call fails (for instance, server cannot be contacted).
        """
        time_stamp = self._generateTimestamp()
        nonce = self._generateNonce()
        hash = self._generateHash(password.encode(), time_stamp, nonce )
        api_key = self.api_key
        user = base64.b64encode(user.encode())
        user = user.decode('utf-8')
        if optionalFilter!="":
            optionalFilterStr = "&" + optionalFilter
        else:
            optionalFilterStr = ""
        urlQuery = "/?method=balert.tpms.tires.get&user=%(user)s&api_key=%(api_key)s&time_stamp=%(time_stamp)d&nonce=%(nonce)s&hash=%(hash)s%(optionalFilterStr)s" % vars()
        return self._dataFromQuery( urlQuery )

    def getTirePositionNames(self, user, password):
        time_stamp = self._generateTimestamp()
        nonce = self._generateNonce()
        hash = self._generateHash(password.encode(), time_stamp, nonce )
        api_key = self.api_key
        user = base64.b64encode(user.encode())
        user = user.decode('utf-8')

        urlQuery = "/?method=balert.tpms.tires.position_names.get&user=%(user)s&api_key=%(api_key)s&time_stamp=%(time_stamp)d&nonce=%(nonce)s&hash=%(hash)s" % vars()
        return self._dataFromQuery( urlQuery )

    def getTireMeasurements( self, user, password, tireId, fromIdOrTime, toIdOrTime, count ):
        """
        get all the measurement for a given tire by id
        Returns the XML answer from server.  Throws a RuntimeError when the call fails (for instance, server cannot be contacted).
        """
        time_stamp = self._generateTimestamp()
        nonce = self._generateNonce()
        hash = self._generateHash(password, time_stamp, nonce )
        api_key = self.api_key
        user = base64.b64encode(user)
        user = user.decode('utf-8')
        fromId, toId= None, None
        fromTime, toTime = None, None
        try:
            fromId = int(fromIdOrTime)
        except (ValueError, TypeError):
            fromTime = fromIdOrTime
        try:
            toId = int(toIdOrTime)
        except (ValueError, TypeError):
            toTime = toIdOrTime

        urlQuery = "/?method=balert.tpms.tire.measurements.history.get&user=%(user)s&api_key=%(api_key)s&time_stamp=%(time_stamp)d&nonce=%(nonce)s&hash=%(hash)s&tireId=%(tireId)d" % vars()
        if fromId!=None:
            urlQuery += "&fromId=%(fromId)d" % vars()
        if toId!=None:
            urlQuery += "&toId=%(toId)d" % vars()
        if fromTime!=None:
            fromTime = fromTime[:].replace(" ","-")
            urlQuery += "&from=%(fromTime)s" % vars()
        if toTime!=None:
            toTime = toTime[:].replace(" ","-")
            urlQuery += "&to=%(toTime)s" % vars()
        if count!=None:
            urlQuery += "&$top=%(count)d" % vars()
        return self._dataFromQuery( urlQuery )

    @staticmethod
    def _generateNonce():
        import random
        nonce = random.randrange(0,1e16)
        return "%016d" % nonce

    @staticmethod
    def _generateTimestamp():
        from datetime import datetime
        firstDayOf2012 = datetime(2012,1,1)
        now = datetime.utcnow()
        deltaSince2012 = now - firstDayOf2012
        deltaInSeconds = _total_seconds(deltaSince2012)
        return int(deltaInSeconds)

    def _generateHash(self, password, time_stamp, nonce):
        import hashlib
        shaPw = hashlib.sha1()
        shaPw.update( password )
        m = hashlib.sha1()
        m.update(str(time_stamp).encode('utf-8'))
        m.update(nonce.encode('utf-8'))
        m.update(shaPw.hexdigest().encode('utf-8'))
        m.update(self.api_key_secret.encode())
        return m.hexdigest()

def rspToNamedTuple(data):
    """
    Converts the return value from the API into a list of NamedTuples for
    easier downstream processing.
    """
    from xml.dom.minidom import parseString
    import collections
    dom = parseString(data)
    rsp = dom.getElementsByTagName("rsp")[0]
    attrs = rsp.attributes
    if attrs.getNamedItem("stat").value=="fail":
        try:
            code = attrs.getNamedItem("failcode").value
            reason = attrs.getNamedItem("reason").value
        except:
            pass
            #print("Return code not understood")
            #print(data)
        raise RuntimeError("API Failed: Code=%(code)s Reason=%(reason)s" % vars())

    def toAscii(x):
        what = x.encode('utf-8',errors='ignore')
        return what

    rvalues = []
    for child in rsp.childNodes:
        if child.nodeType==child.ELEMENT_NODE:
            attrs = child.attributes
            QueryResult = collections.namedtuple( child.tagName, list(attrs.keys()) )
            values = [ toAscii(attrs.getNamedItem(key).value) for key in list(attrs.keys())]
            value = QueryResult(*values)
            rvalues.append(value)
    return rvalues