"""CommitLoom - Weave perfect git commits with AI-powered intelligence."""

from .cli.main import CommitLoom, main
from .core.analyzer import CommitAnalysis, CommitAnalyzer, Warning, WarningLevel
from .core.git import GitError, GitFile, GitOperations
from .services.ai_service import AIService, CommitSuggestion, TokenUsage

__version__ = "0.1.0"
__author__ = "Petru Arakiss"
__email__ = "petruarakiss@gmail.com"

__all__ = [
    "CommitLoom",
    "main",
    "GitOperations",
    "GitFile",
    "GitError",
    "CommitAnalyzer",
    "CommitAnalysis",
    "Warning",
    "WarningLevel",
    "AIService",
    "CommitSuggestion",
    "TokenUsage",
]
