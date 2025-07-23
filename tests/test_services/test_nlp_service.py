import pytest
from app.services.nlp_service import NLPService


@pytest.fixture
def nlp_service():
    """Create NLP service instance"""
    return NLPService()


def test_extract_sentences_with_keywords(nlp_service):
    """Test sentence extraction with action keywords"""
    text = """
    This is a regular sentence.
    John needs to follow up with the client by Friday.
    Another normal sentence here.
    Sarah should prepare the report immediately.
    """
    
    sentences = nlp_service.extract_sentences_with_keywords(text)
    
    assert len(sentences) >= 2
    assert any('follow up' in sentence.lower() for sentence in sentences)
    assert any('should' in sentence.lower() for sentence in sentences)


def test_extract_deadlines(nlp_service):
    """Test deadline extraction"""
    text = "John needs to follow up by Friday and Sarah should complete the report by next Tuesday."
    
    deadlines = nlp_service.extract_deadlines(text)
    
    assert len(deadlines) >= 1
    assert any('friday' in deadline.lower() for deadline in deadlines)


def test_determine_priority(nlp_service):
    """Test priority determination"""
    high_priority_text = "This is urgent and needs immediate attention"
    medium_priority_text = "John should follow up with the client"
    low_priority_text = "When possible, we can update the documentation"
    
    assert nlp_service.determine_priority(high_priority_text) == "high"
    assert nlp_service.determine_priority(medium_priority_text) == "medium"
    assert nlp_service.determine_priority(low_priority_text) == "low"


def test_extract_action_items(nlp_service, sample_text):
    """Test full action item extraction"""
    action_items = nlp_service.extract_action_items(sample_text)
    
    assert len(action_items) > 0
    
    # Check first action item structure
    first_item = action_items[0]
    assert hasattr(first_item, 'id')
    assert hasattr(first_item, 'task')
    assert hasattr(first_item, 'assignees')
    assert hasattr(first_item, 'deadlines')
    assert hasattr(first_item, 'priority')
    assert hasattr(first_item, 'confidence')