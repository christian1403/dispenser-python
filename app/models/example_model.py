"""
Example Model for data structure
"""

from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class ExampleModel:
    """
    Example model representing the data structure
    """
    id: str
    name: str
    value: str
    description: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    def to_dict(self):
        """Convert model to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create model instance from dictionary"""
        return cls(**data)
    
    def validate(self):
        """Validate model data"""
        errors = []
        
        if not self.name or not self.name.strip():
            errors.append("Name is required")
        
        if len(self.name) > 100:
            errors.append("Name must be less than 100 characters")
        
        if self.value and len(self.value) > 500:
            errors.append("Value must be less than 500 characters")
        
        if self.description and len(self.description) > 1000:
            errors.append("Description must be less than 1000 characters")
        
        return errors
    
    def is_valid(self):
        """Check if model is valid"""
        return len(self.validate()) == 0
