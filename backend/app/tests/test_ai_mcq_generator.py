import pytest
from unittest.mock import patch
from app.services.ai_service import generate_mcqs_from_document_async, generate_mcqs_from_text

@pytest.mark.anyio
async def test_ai_mcq_generation_from_document_with_mock_llm():
    custom_doc = (
        "In the Annual Survey of Industries (ASI), the primary frame consists of all factories registered under "
        "Sections 2m(i) and 2m(ii) of the Factories Act, 1948, as well as bidi manufacturing establishments registered under the Bidi and Cigar Workers Act."
    )
    
    mock_llm_response = """
    [
      {
        "question_text": "Under which sections of the Factories Act 1948 are factories registered to form the ASI frame?",
        "option_a": "Sections 2m(i) and 2m(ii)",
        "option_b": "Sections 5a and 5b",
        "option_c": "Section 10 only",
        "option_d": "Section 100",
        "correct_option": "A",
        "explanation": "Factories registered under Sections 2m(i) and 2m(ii) form the core frame of the Annual Survey of Industries.",
        "competency_code": "STAT_IND_AGRI",
        "difficulty": "Intermediate"
      },
      {
        "question_text": "Which establishments besides standard factories are included in the ASI frame?",
        "option_a": "Bidi manufacturing establishments registered under the Bidi and Cigar Workers Act",
        "option_b": "Unregistered roadside stalls",
        "option_c": "Foreign software subsidiaries only",
        "option_d": "Municipal water authorities",
        "correct_option": "A",
        "explanation": "Bidi manufacturing establishments are explicitly included in the ASI universe.",
        "competency_code": "STAT_IND_AGRI",
        "difficulty": "Intermediate"
      }
    ]
    """
    
    with patch("app.services.ai_service.call_llm", return_value=mock_llm_response):
        questions = await generate_mcqs_from_document_async(
            text=custom_doc,
            topic="Annual Survey of Industries Frame",
            num_questions=2,
            difficulty="Intermediate",
            competency_code="STAT_IND_AGRI"
        )
        
        assert len(questions) == 2
        assert "Factories Act 1948" in questions[0]["question_text"]
        assert "Sections 2m(i)" in questions[0]["option_a"]
        assert questions[0]["correct_option"] == "A"
        assert questions[0]["competency_code"] == "STAT_IND_AGRI"

@pytest.mark.anyio
async def test_ai_mcq_generation_fallback_on_malformed_llm():
    custom_doc = "National Accounts GDP calculation and intermediate consumption."
    
    with patch("app.services.ai_service.call_llm", return_value="Invalid non-json response from LLM"):
        questions = await generate_mcqs_from_document_async(
            text=custom_doc,
            topic="National Accounts GDP",
            num_questions=2,
            difficulty="Intermediate"
        )
        
        assert len(questions) == 2
        for q in questions:
            assert "question_text" in q
            assert q["correct_option"] in ["A", "B", "C", "D"]
            assert len(q["explanation"]) > 0

@pytest.mark.anyio
async def test_different_documents_yield_different_fallback_content():
    text_computing = "Python pandas dataframe vectorization and sql query optimization"
    text_sampling = "Multistage stratified cluster sampling first stage units fsu plfs"
    
    q_comp = generate_mcqs_from_text(text=text_computing, topic="Python Computing", num_questions=2)
    q_samp = generate_mcqs_from_text(text=text_sampling, topic="Sampling Frame", num_questions=2)
    
    assert q_comp[0]["competency_code"] == "STAT_COMPUTE"
    assert q_samp[0]["competency_code"] == "STAT_SURVEY"
    assert q_comp[0]["question_text"] != q_samp[0]["question_text"]
