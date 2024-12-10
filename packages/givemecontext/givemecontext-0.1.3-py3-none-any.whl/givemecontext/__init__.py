from givemecontext.decorators.to_log import to_log
from givemecontext.givemecontext import GiveMeContext

# Create singleton instance
context = GiveMeContext()

# Export commonly used components
__all__ = ["context", "to_log"]
