"""
Test API endpoints
"""

import json
import pytest


class TestAPIRoutes:
    """Test API routes"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert data['message'] == 'API is running'
    
    def test_api_status(self, client):
        """Test API status endpoint"""
        response = client.get('/api/v1/status')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'data' in data
        assert data['data']['api_version'] == 'v1'
        assert data['data']['status'] == 'running'
    
    def test_get_example_without_api_key(self, client):
        """Test GET example endpoint without API key"""
        response = client.get('/api/v1/example')
        assert response.status_code == 401
        
        data = json.loads(response.data)
        assert 'error' in data
        assert 'API key required' in data['error']
    
    def test_get_example_with_invalid_api_key(self, client):
        """Test GET example endpoint with invalid API key"""
        headers = {'X-API-Key': 'invalid-key'}
        response = client.get('/api/v1/example', headers=headers)
        assert response.status_code == 401
        
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Invalid API key' in data['error']
    
    def test_get_example_with_valid_api_key(self, client, api_headers):
        """Test GET example endpoint with valid API key"""
        response = client.get('/api/v1/example', headers=api_headers)
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'data' in data
    
    def test_create_example_without_data(self, client, api_headers):
        """Test POST example endpoint without required data"""
        response = client.post('/api/v1/example', headers=api_headers)
        assert response.status_code == 400
    
    def test_create_example_with_invalid_json(self, client, api_headers):
        """Test POST example endpoint with invalid JSON"""
        response = client.post(
            '/api/v1/example', 
            headers={'X-API-Key': 'test-api-key', 'Content-Type': 'application/json'},
            data='invalid json'
        )
        assert response.status_code == 400
    
    def test_create_example_missing_required_fields(self, client, api_headers):
        """Test POST example endpoint with missing required fields"""
        payload = {'description': 'Test description'}
        response = client.post(
            '/api/v1/example',
            headers=api_headers,
            data=json.dumps(payload)
        )
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'Missing required fields' in data['error']
    
    def test_create_example_success(self, client, api_headers):
        """Test POST example endpoint with valid data"""
        payload = {
            'name': 'Test Example',
            'value': 'Test Value',
            'description': 'Test Description'
        }
        response = client.post(
            '/api/v1/example',
            headers=api_headers,
            data=json.dumps(payload)
        )
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'data' in data
        assert data['data']['name'] == payload['name']
        assert data['data']['value'] == payload['value']
    
    def test_get_example_by_id_not_found(self, client, api_headers):
        """Test GET example by ID when ID doesn't exist"""
        response = client.get('/api/v1/example/nonexistent-id', headers=api_headers)
        assert response.status_code == 404
    
    def test_update_example_not_found(self, client, api_headers):
        """Test PUT example by ID when ID doesn't exist"""
        payload = {'name': 'Updated Name'}
        response = client.put(
            '/api/v1/example/nonexistent-id',
            headers=api_headers,
            data=json.dumps(payload)
        )
        assert response.status_code == 404
    
    def test_delete_example_not_found(self, client, api_headers):
        """Test DELETE example by ID when ID doesn't exist"""
        response = client.delete('/api/v1/example/nonexistent-id', headers=api_headers)
        assert response.status_code == 404
