"""
    Regouping all models imports is necessary
    to allow the metadata.create_all function to work well
"""
# flake8: noqa: E401
from caerp_base.models.base import DBBASE
from caerp_base.models.base import DBSESSION

from . import activity
from . import career_stage
from . import career_path
from . import commercial
from . import company
from . import competence
from . import config
from . import files
from . import form_options
from . import holiday
from . import indicators
from . import node
from . import notification
from . import options
from . import payments
from . import progress_invoicing
from . import project
from . import statistics
from . import supply
from . import third_party
from . import tva
from . import task
from . import workshop

from .accounting import operations
from .accounting import balance_sheet_measures
from .accounting import treasury_measures
from .accounting import income_statement_measures
from .accounting import accounting_closures
from .accounting import general_ledger_account_wordings
from .accounting import bookeeping
from .expense import sheet
from .expense import types
from .expense import payment

from .sale_product import category
from .sale_product import base

# Évite les conflits de chemin lors d'import depuis pshell
from .sale_product import sale_product as s
from .sale_product import work
from .sale_product import work_item
from .sale_product import training
from .price_study import work
from .price_study import work_item
from .price_study import product
from .price_study import discount
from .price_study import chapter

# Évite les conflits de chemin lors d'import depuis pshell
from .price_study import price_study as p

# from .sale_product import price_study_work
from .training import trainer
from .training import bpf

# Évite les conflits de chemin lors d'import depuis pshell
from .user import user as u
from .user import login
from .user import group
from .user import userdatas
from caerp_celery import models

# Importe systématiquement les modèles des plugins
# Même si ils sont inutilisés
from caerp.plugins.sap.models import sap
from caerp.plugins.sap_urssaf3p import models


def adjust_for_engine(engine):
    """
    Ajust the models definitions to fit the current database engine
    :param obj engine: The current engine to be used
    """
    if engine.dialect.name == "mysql":
        # Mysql does case unsensitive comparison by default
        login.Login.__table__.c.login.type.collation = "utf8mb4_bin"
