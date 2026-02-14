from watchmatch.models import Availability, ProviderPrice
from typing import Optional

def rank_availability(avail: Availability) -> Optional[ProviderPrice]:
    """
    Returns the 'best' availability for a movie.
    Priority:
      1. Flatrate
      2. Rent (lowest display_priority)
      3. Buy (lowest display_priority)
    """
    if avail.flatrate:
        return avail.flatrate[0]
    elif avail.rent:
        return sorted(avail.rent, key=lambda p: p.display_priority or 0)[0]
    elif avail.buy:
        return sorted(avail.buy, key=lambda p: p.display_priority or 0)[0]
    return None
