"""
Caching Utilities for Performance Optimization
Implements 24-hour caching with localStorage
"""

from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import json
import streamlit as st


# Cache expiration time in hours
CACHE_EXPIRATION_HOURS = 24


def generate_cache_key(destination: str, days: int, budget: float, 
                       currency: str, interests: str = "") -> str:
    """
    Generate a unique cache key for the given parameters.
    
    Args:
        destination: Travel destination
        days: Number of days
        budget: Total budget
        currency: Currency code
        interests: User interests (optional)
    
    Returns:
        Unique cache key string
    """
    # Normalize inputs for consistent caching
    key_parts = [
        destination.lower().strip(),
        str(days),
        str(budget),
        currency.upper().strip(),
        interests.lower().strip()
    ]
    
    return "_".join(key_parts)


def get_cached_results(cache_key: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve cached results if they exist and haven't expired.
    
    Args:
        cache_key: The cache key to look up
    
    Returns:
        Cached results or None if not found/expired
    """
    # Check if we're in a Streamlit session
    if not hasattr(st.session_state, '_cache'):
        st.session_state._cache = {}
    
    if cache_key in st.session_state._cache:
        entry = st.session_state._cache[cache_key]
        expires_at = entry.get('expires_at')
        
        if expires_at and datetime.now() < expires_at:
            return entry.get('results')
        else:
            # Expired, remove from cache
            del st.session_state._cache[cache_key]
    
    return None


def cache_results(cache_key: str, results: Dict[str, Any]) -> bool:
    """
    Cache results for 24 hours.
    
    Args:
        cache_key: The cache key to store under
        results: The results to cache
    
    Returns:
        True if caching was successful
    """
    if not hasattr(st.session_state, '_cache'):
        st.session_state._cache = {}
    
    expires_at = datetime.now() + timedelta(hours=CACHE_EXPIRATION_HOURS)
    
    st.session_state._cache[cache_key] = {
        'results': results,
        'expires_at': expires_at,
        'cached_at': datetime.now()
    }
    
    return True


def clear_cache(cache_key: str = None) -> bool:
    """
    Clear cache entries.
    
    Args:
        cache_key: Specific key to clear, or None to clear all
    
    Returns:
        True if operation was successful
    """
    if not hasattr(st.session_state, '_cache'):
        st.session_state._cache = {}
    
    if cache_key:
        if cache_key in st.session_state._cache:
            del st.session_state._cache[cache_key]
    else:
        st.session_state._cache = {}
    
    return True


def is_cache_expired(cache_key: str) -> bool:
    """
    Check if a cache entry is expired.
    
    Args:
        cache_key: The cache key to check
    
    Returns:
        True if expired or not found
    """
    if not hasattr(st.session_state, '_cache'):
        return True
    
    if cache_key not in st.session_state._cache:
        return True
    
    entry = st.session_state._cache[cache_key]
    expires_at = entry.get('expires_at')
    
    if not expires_at:
        return True
    
    return datetime.now() >= expires_at


def get_cache_stats() -> Dict[str, Any]:
    """
    Get cache statistics.
    
    Returns:
        Dictionary with cache statistics
    """
    if not hasattr(st.session_state, '_cache'):
        return {
            'total_entries': 0,
            'expired_entries': 0,
            'valid_entries': 0
        }
    
    total = len(st.session_state._cache)
    expired = 0
    valid = 0
    
    for key, entry in st.session_state._cache.items():
        expires_at = entry.get('expires_at')
        if expires_at and datetime.now() < expires_at:
            valid += 1
        else:
            expired += 1
    
    return {
        'total_entries': total,
        'expired_entries': expired,
        'valid_entries': valid,
        'expiration_hours': CACHE_EXPIRATION_HOURS
    }


def load_from_cache(destination: str, days: int, budget: float,
                    currency: str, interests: str = "") -> Optional[Dict[str, Any]]:
    """
    Load results from cache if available.
    
    Args:
        destination: Travel destination
        days: Number of days
        budget: Total budget
        currency: Currency code
        interests: User interests (optional)
    
    Returns:
        Cached results or None
    """
    cache_key = generate_cache_key(destination, days, budget, currency, interests)
    return get_cached_results(cache_key)


def save_to_cache(destination: str, days: int, budget: float,
                  currency: str, interests: str = "",
                  results: Dict[str, Any] = None) -> bool:
    """
    Save results to cache.
    
    Args:
        destination: Travel destination
        days: Number of days
        budget: Total budget
        currency: Currency code
        interests: User interests (optional)
        results: Results to cache
    
    Returns:
        True if caching was successful
    """
    if not results:
        return False
    
    cache_key = generate_cache_key(destination, days, budget, currency, interests)
    return cache_results(cache_key, results)


def clear_expired_cache() -> int:
    """
    Clear all expired cache entries.
    
    Returns:
        Number of entries cleared
    """
    if not hasattr(st.session_state, '_cache'):
        return 0
    
    expired_keys = []
    
    for key, entry in st.session_state._cache.items():
        expires_at = entry.get('expires_at')
        if expires_at and datetime.now() >= expires_at:
            expired_keys.append(key)
    
    for key in expired_keys:
        del st.session_state._cache[key]
    
    return len(expired_keys)
