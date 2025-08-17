"""
Test Example Service
"""

import pytest
from app.services.example_service import ExampleService


class TestExampleService:
    """Test Example Service"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.service = ExampleService()
    
    def test_get_example_data(self):
        """Test getting example data"""
        data = self.service.get_example_data()
        
        assert 'message' in data
        assert 'timestamp' in data
        assert 'total_examples' in data
        assert 'examples' in data
        assert isinstance(data['examples'], list)
    
    def test_create_example(self):
        """Test creating an example"""
        data = {
            'name': 'Test Example',
            'value': 'Test Value',
            'description': 'Test Description'
        }
        
        result = self.service.create_example(data)
        
        assert result['name'] == data['name']
        assert result['value'] == data['value']
        assert result['description'] == data['description']
        assert 'id' in result
        assert 'created_at' in result
        assert 'updated_at' in result
    
    def test_get_example_by_id(self):
        """Test getting example by ID"""
        # Create an example first
        data = {'name': 'Test', 'value': 'Value'}
        created = self.service.create_example(data)
        
        # Retrieve it by ID
        retrieved = self.service.get_example_by_id(created['id'])
        
        assert retrieved is not None
        assert retrieved['id'] == created['id']
        assert retrieved['name'] == created['name']
    
    def test_get_nonexistent_example(self):
        """Test getting non-existent example"""
        result = self.service.get_example_by_id('nonexistent-id')
        assert result is None
    
    def test_update_example(self):
        """Test updating an example"""
        # Create an example first
        data = {'name': 'Original', 'value': 'Value'}
        created = self.service.create_example(data)
        
        # Update it
        update_data = {'name': 'Updated', 'value': 'New Value'}
        updated = self.service.update_example(created['id'], update_data)
        
        assert updated is not None
        assert updated['name'] == 'Updated'
        assert updated['value'] == 'New Value'
        assert updated['id'] == created['id']
    
    def test_update_nonexistent_example(self):
        """Test updating non-existent example"""
        result = self.service.update_example('nonexistent-id', {'name': 'Test'})
        assert result is None
    
    def test_delete_example(self):
        """Test deleting an example"""
        # Create an example first
        data = {'name': 'To Delete', 'value': 'Value'}
        created = self.service.create_example(data)
        
        # Delete it
        success = self.service.delete_example(created['id'])
        assert success is True
        
        # Verify it's gone
        retrieved = self.service.get_example_by_id(created['id'])
        assert retrieved is None
    
    def test_delete_nonexistent_example(self):
        """Test deleting non-existent example"""
        success = self.service.delete_example('nonexistent-id')
        assert success is False
    
    def test_list_examples(self):
        """Test listing examples with pagination"""
        # Create some examples
        for i in range(5):
            data = {'name': f'Example {i}', 'value': f'Value {i}'}
            self.service.create_example(data)
        
        # Test listing with pagination
        result = self.service.list_examples(page=1, per_page=3)
        
        assert 'examples' in result
        assert 'total' in result
        assert 'page' in result
        assert 'per_page' in result
        assert 'pages' in result
        assert len(result['examples']) <= 3
        assert result['total'] == 5
