from dateutil import parser
import time
from datetime import timezone

def to_unix(datetime_str: str) -> int:
    """
    Convert any datetime string to Unix timestamp.
    
    Args:
        datetime_str (str): A string representing a date/time in any common format
        
    Returns:
        int: Unix timestamp (seconds since epoch)
        
    Examples:
        >>> to_unix("2021-01-01")
        1609459200
        >>> to_unix("2021/01/01")
        1609459200
        >>> to_unix("01-01-2021")
        1609459200
    """
    try:
        parsed_date = parser.parse(datetime_str)
        # If no timezone info, assume UTC
        if parsed_date.tzinfo is None:
            parsed_date = parsed_date.replace(tzinfo=timezone.utc)
        return int(parsed_date.timestamp())
    except (ValueError, TypeError) as e:
        raise ValueError(f"Could not parse datetime string: {datetime_str}") from e
