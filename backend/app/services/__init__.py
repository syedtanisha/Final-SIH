import sys

from .ai_service import *
from .catalog_service import *
from .assessment_service import *

from . import catalog_service, assessment_service, ai_service

sys.modules['app.services.competency_service'] = catalog_service
sys.modules['app.services.recommendation_service'] = catalog_service
sys.modules['app.services.assessment_service'] = assessment_service
sys.modules['app.services.progress_service'] = assessment_service
sys.modules['app.services.quiz_generator_service'] = assessment_service
sys.modules['app.services.document_service'] = assessment_service
sys.modules['app.services.final_interview_service'] = assessment_service

