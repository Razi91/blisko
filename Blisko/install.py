# -*- coding: utf-8 -*-
__author__ = 'jkonieczny'
"""
    Plik zawiera skrypty instalujące podstawową konfigurację systemu
"""

from web.models import *

def install_basic():
    """
        Kompletnie podstawowa konfiguracja do wywołania zaraz po zresetowaniu bazy danych
    """
    user = User()
    user.id = 0
    user.login = "Niezalogowany"
    user.privilages_id = 0
    user.save()