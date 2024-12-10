#! /usr/bin/env python
# -*- coding:Utf-8 -*-
# pylint: disable=fixme,invalid-name,line-too-long
""" WebServices system management."""

import time
from datetime import datetime

import requests
import xmltodict
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
from suds.client import Client
from urllib3.exceptions import MaxRetryError
from urllib3.util import SKIP_HEADER, Retry

from . import libLog


class webServices_WSDL:
    """Class to manage SOAP Webservice (ie: Kelio)"""

    hshParam = {}
    __hshData = {}

    @property
    def data(self):
        """
        return data

        Returns:
            dict: data
        """
        return self.__hshData

    # pylint: disable-next=dangerous-default-value
    def __init__(self, phshParam={}):
        # Work variables
        self.token = ""
        self.login = ""

        # Start log manager
        self.log = libLog.Log()

        # Update of parameters
        self.hshParam.update(phshParam)

    def Call(self, pqueryfilter):
        """
        Appel de fonction

        Args:
            pqueryfilter (str):   request key from param
        """
        url = self.hshParam["address"].format(
            self.hshParam["request"][pqueryfilter]["address"]
        )

        client = Client(
            url, username=self.hshParam["user"], password=self.hshParam["password"]
        )
        request_data = self.hshParam["request"][pqueryfilter]["request_data"]

        method = getattr(
            client.service, self.hshParam["request"][pqueryfilter]["function"]
        )
        result = method(**request_data)
        if result != "\n":
            self.__hshData[pqueryfilter] = result
        else:
            self.__hshData[pqueryfilter] = None


class webServices_Sylob:
    """Class Webservices Sylob"""

    #: Variables
    hshParam = {}
    hshParam["auth_cognito"] = {"address": "", "login": "", "pwd": ""}
    hshParam["auth"] = {"adress": "", "societe": ""}
    hshParam["request"] = {}
    hshParam["MaxRetryError"] = {"IterationMax": 2, "timeSleep": 120}
    __hshData = {}
    retour_ligne = "<cr/>"

    @property
    def data(self):
        """
        return data

        Returns:
            dict: data
        """
        return self.__hshData

    # pylint: disable-next=dangerous-default-value
    def __init__(self, phshParam={}):
        # Work variables
        self.token = ""
        self.login = ""
        self.auth = None
        self.__NbIteration = 0
        self.session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=1,
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retries))
        # Start log manager
        self.log = libLog.Log()

        # Update of parameters
        self.hshParam.update(phshParam)

    def __Authentification(self, **kw):
        # pylint: disable=broad-exception-raised
        hshOption = {"plogconnect": "DEBUG"}
        # Setting dictionary option
        if isinstance(kw, dict):
            hshOption.update(kw)
        address = self.hshParam["auth_cognito"]["address"]
        params = {
            "grant_type": "client_credentials",
            "scope": "ClientExterne/rest_read",
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        auth = HTTPBasicAuth(
            self.hshParam["auth_cognito"]["login"],
            self.hshParam["auth_cognito"]["pwd"],
        )
        try:
            resp = self.session.post(
                address,
                headers=headers,
                params=params,
                auth=auth,
            )
            self.__NbIteration = 0
        # TODO : Gestion en paramètre de 2 infos : waitingtime et nbiteration
        #   avant déclenchement de l'erreur Max retries exceeded with url = urllib3.exceptions.MaxRetryError
        except MaxRetryError as e:
            if self.__NbIteration < self.hshParam["MaxRetryError"]["IterationMax"]:
                time.sleep(self.hshParam["MaxRetryError"]["timeSleep"])
                self.__NbIteration += 1
                self.__Authentification(**kw)
            else:
                self.__NbIteration = 0
                raise Exception(f"POST /auth/ {e}") from e

        if resp.status_code != 200:
            raise Exception(
                f"POST /auth/ {resp.status_code} [reason: {str(resp.reason)}]"
            )
        if hshOption["plogconnect"]:
            self.log.Write(
                self.log.LEVEL[hshOption["plogconnect"]],
                f"Connection {self.log.setStep} successfully",
            )
        self.token = resp.json().get("access_token")
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        self.auth = HTTPBasicAuth(
            f"{self.hshParam['auth_cognito']['login']}@@{self.hshParam['auth']['societe']}@@{now}",
            f"oauth.clientcredentials.{self.token}",
        )

    # //////////////////////////////////////////////////
    #     Call
    # //////////////////////////////////////////////////
    def Call(self, pqueryfilter, pbind=None, pparameters=None, **kw):
        """
        Lancement du web services avec infos à passer et résultats stockés dans data

        Args:
            pqueryfilter (str): filter string in queries dictionary
            pbind (str, optional): the bind variables of queries. Defaults to None.
            pparameters (dict, optional): dict of key, value to send. Defaults to None.
            phisto (bool, optional): save into history or not. Defaults to False.
            **piteration (int): First launch function for authentication problems(not to be changed)
            **plimit (int): Number of elements to load (default=99999)
            **plogrequest (LOG_LEVEL): Log level display for request. "None" for no display (default=DEBUG)
        Raises:
            Exception: No connection
        """
        hshOption = {"piteration": 0, "plogrequest": "DEBUG", "plimit": 99999}
        # Setting dictionary option
        if isinstance(kw, dict):
            hshOption.update(kw)

        for k, v in filter(
            lambda x: pqueryfilter == x[0][: len(pqueryfilter)],
            self.hshParam["request"].items(),
        ):
            self.log.setStep = f"R[{k}]"
            if pbind:
                req = v.format(**pbind)
            else:
                req = v
            site = f"{self.hshParam['auth']['address']}/query/{req}/resultat?limite={hshOption['plimit']}"
            if pparameters is not None:
                site = (
                    site + "&" + "&".join(f"{k}={v}" for (k, v) in pparameters.items())
                )
            if hshOption["plogrequest"]:
                self.log.Write(
                    self.log.LEVEL[hshOption["plogrequest"]],
                    f"Request {k} : {site}",
                )

            try:
                resp = self.session.get(
                    site,
                    headers={"accept": "application/json"},
                    auth=self.auth,
                )
            except requests.ConnectionError as err:
                if hshOption["piteration"] < 2:
                    self.log.Warning(f"Problem with connection : {err}")
                    hshOption["piteration"] += 1
                    time.sleep(1)
                    self.Call(
                        pqueryfilter,
                        pbind=pbind,
                        pparameters=pparameters,
                        **{
                            "piteration": hshOption["piteration"] + 1,
                            "plimit": hshOption["plimit"],
                        },
                    )
                    return None
                else:
                    raise ConnectionError from err
            if resp.status_code in (401, 403, 500) and hshOption["piteration"] < 2:
                self.__Authentification()
                self.Call(
                    pqueryfilter,
                    pbind=pbind,
                    pparameters=pparameters,
                    **{
                        "piteration": hshOption["piteration"] + 1,
                        "plimit": hshOption["plimit"],
                    },
                )
                return None
            if resp.status_code != 200:
                try:
                    msg = resp.json()["errors"][0]["detail"]
                # pylint: disable-next=broad-exception-caught
                except Exception:
                    msg = ""
                # pylint: disable-next=broad-exception-raised
                raise ConnectionError(
                    f"get /{pqueryfilter}/ {resp.status_code} : {msg}"
                )
            self.__hshData[k] = self._mef_data_s9(resp.json())
            self.log.setStep = ""

    # //////////////////////////////////////////////////
    #     Action
    # //////////////////////////////////////////////////
    def Action(self, pcode, pbody=None, pparameters=None, **kw):
        """
        Lancement du web services avec infos à passer et résultats stockés dans data

        Args:
            pcode (str): Sylob9 Code Action
            pbody (dict, optional): dict question, answser for scenario. Defaults to None.
            pparameters (dict, optional): dict of key, value to send. Defaults to None.
            **piteration (int): First launch function for authentication problems(not to be changed)
            **plogrequest (LOG_LEVEL): Log level display for request. "None" for no display (default=DEBUG)
            **pcarriagereturn (str) : Carriage return used for multiples infos. (default="\\n")

        Raises:
            Exception: No connection
            Exception: Returned Error
        """
        hshOption = {"piteration": 0, "plogrequest": "DEBUG", "pcarriagereturn": "\n"}
        if isinstance(kw, dict):
            hshOption.update(kw)

        self.log.setStep = f"R[{pcode}]"
        site = f"{self.hshParam['auth']['address']}/v2/action/{pcode}/execute"
        if pparameters is not None:
            site = site + "&" + "&".join(f"{k}={v}" for (k, v) in pparameters.items())
        if hshOption["plogrequest"]:
            self.log.Write(
                self.log.LEVEL[hshOption["plogrequest"]],
                f"Request {pcode} : {site} = {pbody}",
            )
        try:
            resp = self.session.post(
                site, headers={"accept": "application/json"}, auth=self.auth, json=pbody
            )
        except requests.ConnectionError as err:
            if hshOption["piteration"] < 2:
                self.log.Warning(f"Problem with connection : {err}")
                hshOption["piteration"] += 1
                time.sleep(1)
                self.Action(
                    pcode,
                    pbody=pbody,
                    pparameters=pparameters,
                    **hshOption,
                )
                return None
            raise ConnectionError from err
        resp.encoding = "utf-8"
        if resp.status_code in (401, 403, 500) and hshOption["piteration"] < 2:
            self.__Authentification()
            hshOption["piteration"] += 1
            self.Action(
                pcode,
                pbody=pbody,
                pparameters=pparameters,
                **hshOption,
            )
            return None

        if resp.status_code not in (200, 400):
            raise ConnectionError(
                f"post /{pcode} : {resp.status_code}  [reason: {str(resp.reason)}]"
            )
        self.__hshData[pcode] = self._analyse_reponse_s9(
            resp.json(), hshOption["pcarriagereturn"]
        )
        if hshOption["plogrequest"]:
            self.log.Write(
                self.log.LEVEL[hshOption["plogrequest"]],
                f"Response {pcode} : {resp.json()}",
            )

        self.log.setStep = ""

    # //////////////////////////////////////////////////
    #     Get_pj
    # //////////////////////////////////////////////////
    def Get_pj(self, pcode, pfilename=None, **kw):
        """
        Récupère le document selon l'id

        Args:
            pcode (str): Sylob9 ID du document
            pfilename (str, optional): filename to save document. "None" returns fileObject. Defaults to None.
            **piteration (int): First launch function for authentication problems(not to be changed)
            **plogrequest (LOG_LEVEL): Log level display for request. "None" for no display (default=DEBUG)

        Returns:
            str: File Object or filename if not None
        """

        hshOption = {"piteration": 0, "plogrequest": "DEBUG"}
        if isinstance(kw, dict):
            hshOption.update(kw)

        self.log.setStep = f"R[{pcode}]"
        site = (
            self.hshParam["auth"]["address"].replace("/rest", "")
            + "/CochiseWeb/ouvrirDocument?cmd=displayImage&id="
            + pcode
        )
        if hshOption["plogrequest"]:
            self.log.Write(
                self.log.LEVEL[hshOption["plogrequest"]],
                f"Request {pcode} : {site}",
            )

        try:
            resp = self.session.get(site, auth=self.auth)
        except ConnectionError as err:
            if hshOption["piteration"] < 2:
                self.log.Warning(f"Problem with connection : {err}")
                hshOption["piteration"] += 1
                self.Get_pj(
                    pcode,
                    **hshOption,
                )
            else:
                raise ConnectionError from err
        if resp.status_code in (401, 403, 500) and hshOption["piteration"] < 2:
            self.__Authentification()
            hshOption["piteration"] += 1
            self.Get_pj(
                pcode,
                **hshOption,
            )
            return None
        if hshOption["plogrequest"]:
            self.log.Write(
                self.log.LEVEL[hshOption["plogrequest"]],
                f"Response {pcode} : {resp.content}",
            )
        self.log.setStep = ""
        if pfilename:
            # write to file
            with open(pfilename, "wb") as newFile:
                newFile.write(resp.content)
            return pfilename

        return resp.content

    def _analyse_reponse_s9(self, reponse, CR):
        retour = {}
        if not isinstance(reponse["status"], dict):
            # Erreur
            # self.log.Error(f"Erreur {reponse['status']} : {reponse['errors']}")
            retour["status"] = "ERREUR"
            retour["info"] = CR.join(
                [
                    e.get("message", "") + " : " + e.get("help", "")
                    for e in reponse["errors"]
                ]
            )
        elif "schema" in reponse:
            # saisie incomplète
            # self.log.Error(f"Saisie incompète : {str(reponse['schema'])}")
            retour["status"] = "INCOMPLET"
            retour["info"] = reponse["schema"]
            if "body" in reponse:
                try:
                    for ques, rep in reponse["body"].items():
                        retour["info"]["properties"][ques]["value"] = rep
                # pylint: disable-next=broad-exception-caught
                except Exception:
                    pass
        elif reponse["status"]["success"]:
            retour["status"] = "OK"
            retour["info"] = "Traitement OK"
        elif not reponse["status"]["success"]:
            retour["status"] = "WARNING"
            retour["info"] = (
                CR.join(reponse["status"]["messages"])
                + " : "
                + CR.join(reponse["status"]["warnings"])
            )

        else:
            # self.log.Error(f"unknown response : {reponse}")
            retour["status"] = "ERREUR"
            retour["info"] = reponse
        return retour

    def _mef_data_s9(self, data):
        """
        Permet de créer un dictionnaire des éléments retournés par Sylob 9

        Args:
            data (json): Données json transmises par Sylob 9

        Returns:
            lst(dict): Tous les éléments mis en forme
        """
        ordre_colonne = []
        tmp_format = {}
        modele = {}
        retour = []
        # Déclaration des colonnes dans l'ordre
        ordre_colonne = data["colonne"]
        # Récupération des types attendus
        for col in data["colonneQueryWS"]:
            tmp_format[col["libelle"]] = col["type"]
        # enregistrement d'un dictionnaire modèle
        for k in ordre_colonne:
            modele[k] = ""
        # enregistrement de toutes les lignes
        for lig in data["ligneResultatWS"]:
            val = modele.copy()
            for idx, e in enumerate(lig["valeur"]):
                k = ordre_colonne[idx]
                if tmp_format[k] == "Boolean":
                    val[k] = e.lower() in ["vrai", "true", "activé", "1"]
                else:
                    val[k] = e
            retour.append(val)
        return retour


# "Debugage de Request"
# http_client.HTTPConnection.debuglevel = 1


class webServices_S9000:
    """Class Webservices S9000"""

    #: Variables
    hshParam = {}
    hshParam["adress"] = ""
    hshParam = {"adress": "", "user": "", "password": ""}
    hshParam["request"] = [{"action": "", "param": ""}]
    __hshData = {}
    retour_ligne = "&#10;"

    @property
    def data(self):
        """
        return data

        Returns:
            dict: data
        """
        return self.__hshData

    # pylint: disable-next=dangerous-default-value
    def __init__(self, phshParam={}):
        # Work variables
        self.token = ""
        self.login = ""

        # Start log manager
        self.log = libLog.Log()
        self.session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=1,
            # status_forcelist=[502, 503, 504]
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

        # Update of parameters
        self.headers = {
            "Content-Type": "text/xml; charset=ISO-8859-1",
            "SOAPAction": "{address}/{request}",
            "Except": "100-continue",
            "Cache-Control": "no-cache",
            "Accept-Encoding": SKIP_HEADER,
        }
        self.body = (
            """<?xml version="1.0" encoding="ISO-8859-1"?>
            <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope" """
            + """xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/" """
            + """xmlns:tns="http://s9.mecapack.com:8091/webservice_test/ws_complet.php" """
            + """xmlns:types="http://s9.mecapack.com:8091/webservice_test/ws_complet.php/encodedTypes" """
            + """xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                <soap:Body soap:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
                    <q1:{request} xmlns:q1="http://s9.mecapack.com:8091/webservice_test/ws_complet.php?wsdl">
                        <Login xsi:type="xsd:string">{user}</Login>
                        <Password xsi:type="xsd:string">{password}</Password>
                        {param}
                    </q1:{request}>
                </soap:Body>
            </soap:Envelope>
            """
        )

        self.hshParam.update(phshParam)

    # pylint: disable=unused-argument,too-many-locals,broad-exception-caught,broad-exception-raised
    def Call(self, pqueryfilter, pbind=None, pparameters=None, **kw):
        """
        Lancement du web services avec infos à passer et résultats stockés dans data

        Args:
            pqueryfilter (str): filter string in queries dictionary
            pparameters (xml, optional): dict of key, value to send. Defaults to None.
            **piteration (int): First launch function for authentication problems(not to be changed)
            **plogrequest (LOG_LEVEL): Log level display for request. "None" for no display (default=DEBUG)

        Raises:
            Exception: No connection
        """
        # pylint: disable=possibly-unused-variable
        hshOption = {"piteration": 0, "plogrequest": "DEBUG"}
        # Setting dictionary option
        if isinstance(kw, dict):
            hshOption.update(kw)
        address = self.hshParam["address"]
        site = f"{address}?wsdl"
        user = self.hshParam["user"]
        password = self.hshParam["password"]
        for key, infos in filter(
            lambda x: pqueryfilter == x[0][: len(pqueryfilter)],
            self.hshParam["request"].items(),
        ):
            self.log.setStep = f"R[{key}]"
            if hshOption["plogrequest"]:
                self.log.Write(
                    self.log.LEVEL[hshOption["plogrequest"]],
                    f"Request {key} : {site}",
                )
            headers = self.headers.copy()
            request = infos["action"]
            if pparameters:
                param = infos["param"].format(**pparameters)  # NOQA
            else:
                param = infos["param"]
            headers["SOAPAction"] = headers["SOAPAction"].format(**locals())
            body = self.body.format(**locals()).replace("\n", "")
            try:
                resp = self.session.post(
                    site,
                    headers=headers,
                    data=body.encode("utf-8"),
                )
                # # Pour débugage plus poussé
                # req = requests.Request(
                #     "POST", site, headers=headers, data=body.encode("utf-8")
                # )
                # # prepared = req.prepare()
                # prepared = self.session.prepare_request(req)
                # del prepared.headers["accept-encoding"]
                # resp = self.session.send(prepared)
            except requests.ConnectionError as err:
                if hshOption["piteration"] < 2:
                    self.log.Warning(f"Problem with connection : {err}")
                    hshOption["piteration"] += 1
                    time.sleep(1)
                    self.Call(
                        pqueryfilter,
                        pbind=pbind,
                        pparameters=pparameters,
                        **{
                            "piteration": hshOption["piteration"] + 1,
                            "plogrequest": hshOption["plogrequest"],
                        },
                    )
                    return None
                else:
                    raise ConnectionError from err

            if resp.status_code != 200:
                try:
                    # Récupérer le message contenu dans le xml
                    msg = xmltodict.parse(resp.text)["SOAP-ENV:Envelope"][
                        "SOAP-ENV:Body"
                    ]["SOAP-ENV:Fault"]
                except Exception:
                    msg = resp.text
                raise Exception(f"get /{pqueryfilter}/ {resp.status_code} : {msg}")
            # Transcrire le XML et récupérer le contenu significatif
            content = xmltodict.parse(resp.text)["SOAP-ENV:Envelope"]["SOAP-ENV:Body"][
                f"ns1:{request}Response"
            ]["return"]
            if content["type_erreur"]["#text"] not in ["000", "251"]:
                # ERREUR d'envoi
                raise Exception(
                    f"retour /{pqueryfilter}/: {content['msg_erreur']['#text']}"
                )
            # décoder HTML
            if "xml" in content:
                self.__hshData[key] = xmltodict.parse(content["xml"]["#text"])
            else:
                res = {}
                for k, v in content.items():
                    if "#text" in v:
                        res[k] = v["#text"]
                self.__hshData[key] = res
            self.log.setStep = ""
