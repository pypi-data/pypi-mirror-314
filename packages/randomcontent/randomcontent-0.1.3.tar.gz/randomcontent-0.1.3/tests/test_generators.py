# tests/test_generators.py

from randomcontent.generators.text_generator import generate_text
from randomcontent.generators.structured_generator import generate_mock_data

def test_generate_text():
    sentence = generate_text(type="sentence", length=5)
    assert isinstance(sentence, str)
    assert len(sentence.split()) == 5



def test_generate_mock_data():
    schema = {
        "name": "random_name",
        "email": "random_email",
        "age": "random_int(min=18, max=99)"
    }
    
    # Generate mock data
    mock_data = generate_mock_data(schema, count=3)
    
    # Assert that the generated data is a list
    assert isinstance(mock_data, list)
    
    # Assert that each item in the mock data is a dictionary
    for item in mock_data:
        assert isinstance(item, dict)
        
    # Assert that the name, email, and age fields are generated
    for item in mock_data:
        assert "name" in item
        assert "email" in item
        assert "age" in item
        
    # Assert that the age is between 18 and 99
    for item in mock_data:
        assert 18 <= item["age"] <= 99
