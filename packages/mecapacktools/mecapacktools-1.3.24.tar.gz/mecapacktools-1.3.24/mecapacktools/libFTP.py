#! /usr/bin/env python
# -*- coding:Utf-8 -*-
# pylint: disable=fixme,invalid-name,line-too-long
""" FTP system management."""
import os
from stat import S_ISDIR

import paramiko

from . import libLog


class libFTP:
    """Class to manage FTP service"""

    #: Variables
    hshParam = {"hostname": "", "user": "", "keyFile": ""}

    # pylint: disable-next=dangerous-default-value
    def __init__(self, phshParam={}):
        # Work variables
        self.__ssh = None
        self.__sftp_client = None
        # Start log manager
        self.log = libLog.Log()
        # Update of parameters
        self.hshParam.update(phshParam)

    def Connections_Load(self):
        """
        Loading connexion
        """
        # Connection
        self.log.setStep = "Connection to FTP"
        __key = paramiko.RSAKey.from_private_key_file(self.hshParam["keyFile"])
        self.__ssh = paramiko.SSHClient()
        self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.__ssh.connect(hostname=self.hshParam["hostname"], username=self.hshParam["user"], pkey=__key)
        self.__sftp_client = self.__ssh.open_sftp()
        self.log.Debug(f"Connection to {self.hshParam['hostname']} successfully")

    def listdir(self, path="."):
        """
        Retourne la liste des fichiers du répertoire path

        Args:
            path (str, optional): chemin relatif du répertoire. Defaults to "."

        Returns:
            list: Nom des entrée présentes dans le répertoire
        """
        return self.__sftp_client.listdir(path)

    def isdir(self, path):
        """
        Retourne si le chemin est un répertoire ou non

        Args:
            path (str): chemin à tester

        Returns:
            bool: True si répertoire False sinon
        """
        try:
            return S_ISDIR(self.__sftp_client.stat(path).st_mode)
        except IOError:
            return False

    def mkdir(self, path, mode=511, ignore_existing=False):
        """
        Créer un répertoire distant

        Args:
            path (str): Nom et chemin du répertoire
            mode (int, optional): Droits sur le répertoire. Defaults to 511.
            ignore_existing (bool, optional): Ne lève pas d'exception si le répertoire existe déjà.
                Defaults to False.
        """
        try:
            self.__sftp_client.mkdir(path, mode)
            self.log.Debug(f"Répertoire {path} créé")
        except IOError:
            if ignore_existing:
                pass
            else:
                raise

    def rmdir(self, path, only_empty=True):
        """
        Supprime le répertoire et tout son contenu

        Args:
            path (str): Nom et chemin du répertoire
            only_empty (bool, optional): Supprime le répertoire uniquement s'il est vide. Defaults to True.
        """
        files = self.__sftp_client.listdir(path)

        for f in files:
            filepath = f"{path}/{f}"
            if self.isdir(filepath):
                self.rmdir(filepath, only_empty)
            elif not only_empty:
                self.__sftp_client.remove(filepath)
        if not only_empty:
            self.__sftp_client.rmdir(path)
            self.log.Debug(f"Répertoire {path} supprimé")
        else:
            try:
                self.__sftp_client.rmdir(path)
                self.log.Debug(f"Répertoire {path} supprimé")
            # pylint: disable-next=broad-exception-caught
            except Exception:
                pass

    def putdir(self, source, target):
        """
        Upload le contenu du répertoire source vers le répertoire de destination
        Le répertoire de destination doit exister.

        Args:
            source (str): Nom et chemin du répertoire source
            target (str): Nom et chemin du répertoire distant
        """
        for item in os.listdir(source):
            if os.path.isfile(os.path.join(source, item)):
                self.__sftp_client.put(os.path.join(source, item), f"{target}/{item}")
            else:
                self.mkdir(f"{target}/{item}", ignore_existing=True)
                self.putdir(os.path.join(source, item), f"{target}/{item}")
        self.log.Debug(f"Répertoire {source} envoyé")

    def put(self, source, target):
        """
        Upload un fichier source vers le répertoire de destination
        Le répertoire de destination doit exister.

        Args:
            source (str): Nom et chemin du fichier source
            target (str): Nom et chemin du répertoire distant
        """
        if os.path.isfile(source):
            filename = os.path.basename(source)
            self.__sftp_client.put(source, f"{target}/{filename}")
            self.log.Debug(f"Fichier {source} envoyé")
        else:
            self.log.Warning(f"Le fichier {source} n'existe pas")
