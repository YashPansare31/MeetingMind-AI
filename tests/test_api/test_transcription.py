import json
import io


def test_analyze_text_endpoint(client, sample_text):
    """Test text analysis endpoint"""
    response = client.post(
        '/api/analyze/text',
        json={'text': sample_text},
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['success'] == True
    assert 'action_items' in data
    assert 'summary' in data
    assert len(data['action_items']) > 0


def test_analyze_text_with_custom_keywords(client, sample_text):
    """Test text analysis with custom keywords"""
    response = client.post(
        '/api/analyze/text',
        json={
            'text': sample_text,
            'custom_keywords': ['follow up', 'urgent', 'deadline']
        },
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['success'] == True
    assert len(data['action_items']) > 0


def test_analyze_text_empty_text(client):
    """Test text analysis with empty text"""
    response = client.post(
        '/api/analyze/text',
        json={'text': ''},
        content_type='application/json'
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    
    assert data['success'] == False
    assert data['error'] == 'ValidationError'


def test_analyze_text_no_text_field(client):
    """Test text analysis without text field"""
    response = client.post(
        '/api/analyze/text',
        json={},
        content_type='application/json'
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    
    assert data['success'] == False
    assert data['error'] == 'ValidationError'
