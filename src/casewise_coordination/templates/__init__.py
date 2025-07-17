"""
Session Templates
Pre-configured templates for different types of Claude sessions
"""

from .base_template import SessionTemplate
from .frontend_template import FrontendTemplate
from .backend_template import BackendTemplate
from .testing_template import TestingTemplate
from .documentation_template import DocumentationTemplate
from .integration_template import IntegrationTemplate

__all__ = [
    "SessionTemplate",
    "FrontendTemplate", 
    "BackendTemplate",
    "TestingTemplate",
    "DocumentationTemplate",
    "IntegrationTemplate"
]