"""
Example Service for handling business logic
"""

import uuid
from datetime import datetime
from app.models.example_model import ExampleModel
from app.utils.helpers import generate_uuid, current_timestamp


class ExampleService:
    """Service class for handling example-related operations"""
    
    def __init__(self):
        """Initialize the service with in-memory storage (replace with database)"""
        # In a real application, this would be a database connection
        self._storage = {}
    
    def get_example_data(self):
        """
        Get all example data
        
        Returns:
            List of example data
        """
        return {
            'message': 'This is example data from the service',
            'timestamp': current_timestamp(),
            'total_examples': len(self._storage),
            'examples': list(self._storage.values())
        }
    
    def create_example(self, data):
        """
        Create a new example
        
        Args:
            data: Dictionary containing example data
            
        Returns:
            Created example data
        """
        example = ExampleModel(
            id=generate_uuid(),
            name=data['name'],
            value=data.get('value', ''),
            description=data.get('description', ''),
            created_at=current_timestamp(),
            updated_at=current_timestamp()
        )
        
        # Store in memory (replace with database save)
        self._storage[example.id] = example.to_dict()
        
        return example.to_dict()
    
    def get_example_by_id(self, example_id):
        """
        Get example by ID
        
        Args:
            example_id: ID of the example
            
        Returns:
            Example data or None if not found
        """
        return self._storage.get(example_id)
    
    def update_example(self, example_id, data):
        """
        Update example by ID
        
        Args:
            example_id: ID of the example
            data: Updated data
            
        Returns:
            Updated example data or None if not found
        """
        if example_id not in self._storage:
            return None
        
        example_data = self._storage[example_id]
        
        # Update fields
        example_data['name'] = data.get('name', example_data['name'])
        example_data['value'] = data.get('value', example_data['value'])
        example_data['description'] = data.get('description', example_data['description'])
        example_data['updated_at'] = current_timestamp()
        
        self._storage[example_id] = example_data
        
        return example_data
    
    def delete_example(self, example_id):
        """
        Delete example by ID
        
        Args:
            example_id: ID of the example
            
        Returns:
            Boolean indicating success
        """
        if example_id not in self._storage:
            return False
        
        del self._storage[example_id]
        return True
    
    def list_examples(self, page=1, per_page=10):
        """
        List examples with pagination
        
        Args:
            page: Page number
            per_page: Items per page
            
        Returns:
            Paginated list of examples
        """
        examples = list(self._storage.values())
        total = len(examples)
        
        # Calculate pagination
        start = (page - 1) * per_page
        end = start + per_page
        
        return {
            'examples': examples[start:end],
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        }
