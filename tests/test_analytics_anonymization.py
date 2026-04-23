"""
Property-Based Tests for Analytics Data Anonymization
Validates that all analytics data is properly anonymized and contains no PII
"""

import pytest
from hypothesis import given, strategies as st, settings
import hashlib
import json
from datetime import datetime, timedelta


@given(
    st.floats(min_value=10, max_value=100000),
    st.sampled_from(["INR", "USD", "EUR", "GBP", "JPY", "CAD", "AUD", "SGD", "CNY"])
)
@settings(max_examples=50, deadline=None)
def test_budget_range_calculation(budget, currency):
    """Property: Budget range should be correctly categorized"""
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    
    from components.analytics import calculate_budget_range
    
    budget_range = calculate_budget_range(budget, currency)
    
    # Should return one of three valid categories
    assert budget_range in ["low", "medium", "high"]
    
    # Verify categorization logic
    conversion_rates = {
        "INR": 0.012,
        "USD": 1.0,
        "EUR": 1.08,
        "GBP": 1.27,
        "JPY": 0.0067,
        "CAD": 0.74,
        "AUD": 0.66,
        "SGD": 0.75,
        "CNY": 0.14
    }
    
    budget_usd = budget * conversion_rates.get(currency, 0.012)
    
    if budget_usd < 500:
        assert budget_range == "low"
    elif budget_usd < 2000:
        assert budget_range == "medium"
    else:
        assert budget_range == "high"


@given(
    st.sampled_from([
        ("Delhi", "domestic"),
        ("Mumbai", "domestic"),
        ("Goa", "domestic"),
        ("Kerala", "domestic"),
        ("Tokyo", "international"),
        ("Paris", "international"),
        ("New York", "international"),
        ("London", "international"),
        ("Unknown City", "international")
    ])
)
def test_destination_type_calculation(destination_and_type):
    """Property: Destination type should be correctly identified"""
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    
    from components.analytics import calculate_destination_type
    
    destination, expected_type = destination_and_type
    actual_type = calculate_destination_type(destination)
    assert actual_type == expected_type


def test_hashed_session_id_format():
    """Property: Session ID should be properly hashed"""
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    
    from components.analytics import get_anonymized_session_id
    
    # Test with a known session ID
    import streamlit as st
    st.session_state.session_id = "test-session-id-12345"
    
    session_id = get_anonymized_session_id()
    
    # Should be a 16-character hexadecimal string
    assert len(session_id) == 16
    assert all(c in '0123456789abcdef' for c in session_id)
    
    # Should not contain original session ID
    assert "test-session-id" not in session_id
    
    # Verify it's a valid SHA256 hash (truncated)
    expected_hash = hashlib.sha256("test-session-id-12345".encode()).hexdigest()[:16]
    assert session_id == expected_hash


def test_anonymized_id_is_consistent():
    """Property: Anonymized ID should be consistent across calls"""
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    
    from components.analytics import get_anonymized_session_id
    
    # Set a session ID
    import streamlit as st
    st.session_state.session_id = "test-session-id-12345"
    
    id1 = get_anonymized_session_id()
    id2 = get_anonymized_session_id()
    
    # Should be the same (based on session_id in session state)
    assert id1 == id2


def test_anonymized_id_changes_with_different_session():
    """Property: Anonymized ID should change with different session IDs"""
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    
    from components.analytics import get_anonymized_session_id
    
    import streamlit as st
    
    # Set first session ID
    st.session_state.session_id = "session-1"
    id1 = get_anonymized_session_id()
    
    # Set different session ID
    st.session_state.session_id = "session-2"
    id2 = get_anonymized_session_id()
    
    # Should be different
    assert id1 != id2


def test_budget_range_boundaries():
    """Property: Budget range should correctly categorize boundary values"""
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    
    from components.analytics import calculate_budget_range
    
    # Test boundary values for INR
    # Low: < 500 USD = < 41667 INR
    # Medium: 500-2000 USD = 41667-166667 INR
    # High: > 2000 USD = > 166667 INR
    
    # Low budget boundary
    assert calculate_budget_range(40000, "INR") == "low"
    assert calculate_budget_range(41666, "INR") == "low"
    
    # Medium budget boundary
    assert calculate_budget_range(50000, "INR") == "medium"
    assert calculate_budget_range(100000, "INR") == "medium"
    assert calculate_budget_range(166666, "INR") == "medium"
    
    # High budget boundary
    assert calculate_budget_range(170000, "INR") == "high"
    assert calculate_budget_range(500000, "INR") == "high"
    
    # Test with USD
    assert calculate_budget_range(400, "USD") == "low"
    assert calculate_budget_range(1000, "USD") == "medium"
    assert calculate_budget_range(3000, "USD") == "high"


def test_destination_type_keywords():
    """Property: Destination type should correctly identify domestic destinations"""
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    
    from components.analytics import calculate_destination_type
    
    # Test domestic destinations
    assert calculate_destination_type("Delhi") == "domestic"
    assert calculate_destination_type("Mumbai") == "domestic"
    assert calculate_destination_type("Goa") == "domestic"
    assert calculate_destination_type("Kerala") == "domestic"
    assert calculate_destination_type("Rajasthan") == "domestic"
    assert calculate_destination_type("Uttarakhand") == "domestic"
    assert calculate_destination_type("Himachal Pradesh") == "domestic"
    
    # Test international destinations
    assert calculate_destination_type("Tokyo") == "international"
    assert calculate_destination_type("Paris") == "international"
    assert calculate_destination_type("New York") == "international"
    assert calculate_destination_type("London") == "international"
    assert calculate_destination_type("Dubai") == "international"
    assert calculate_destination_type("Singapore") == "international"
    assert calculate_destination_type("Unknown City") == "international"


def test_destination_type_case_insensitive():
    """Property: Destination type should be case insensitive"""
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    
    from components.analytics import calculate_destination_type
    
    assert calculate_destination_type("DELHI") == "domestic"
    assert calculate_destination_type("delhi") == "domestic"
    assert calculate_destination_type("Goa") == "domestic"
    assert calculate_destination_type("GOA") == "domestic"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
