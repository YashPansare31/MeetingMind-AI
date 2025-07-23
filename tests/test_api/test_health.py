import json


def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/api/health')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['status'] == 'healthy'
    assert 'timestamp' in data
    assert data['version'] == '1.0.0'


def test_models_health_endpoint(client):
    """Test models health endpoint"""
    response = client.get('/api/health/models')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['status'] in ['healthy', 'unhealthy']
    assert 'timestamp' in data
