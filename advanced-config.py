"""
Advanced Configuration for Code Review Agent
Customize the behavior and rules of your autonomous code reviewer.
"""

from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class LinterConfig:
    """Configuration for individual linters"""
    enabled: bool = True
    timeout: int = 30
    custom_args: List[str] = None

@dataclass
class AIConfig:
    """Configuration for AI analysis"""
    model: str = "gpt-3.5-turbo"  # or "claude-3-sonnet-20240229"
    max_tokens: int = 1000
    temperature: float = 0.3
    custom_prompt: str = None

@dataclass
class ReviewConfig:
    """Main configuration for the code review agent"""
    
    # File patterns to include/exclude
    include_patterns: List[str] = None
    exclude_patterns: List[str] = None
    
    # Maximum file size to analyze (in bytes)
    max_file_size: int = 1024 * 1024  # 1MB
    
    # Linter configurations
    linters: Dict[str, LinterConfig] = None
    
    # AI configuration
    ai_config: AIConfig = None
    
    # Review categories to focus on
    review_categories: List[str] = None
    
    # Custom rules for specific languages/frameworks
    language_rules: Dict[str, Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.include_patterns is None:
            self.include_patterns = [
                "*.py", "*.js", "*.ts", "*.jsx", "*.tsx", 
                "*.java", "*.cpp", "*.c", "*.go", "*.rs"
            ]
        
        if self.exclude_patterns is None:
            self.exclude_patterns = [
                "*.min.js", "*.min.css", "*.map",
                "node_modules/*", "venv/*", "__pycache__/*"
            ]
        
        if self.linters is None:
            self.linters = {
                "pylint": LinterConfig(enabled=True, custom_args=["--disable=C0114"]),
                "flake8": LinterConfig(enabled=True),
                "black": LinterConfig(enabled=True),
                "eslint": LinterConfig(enabled=True),
                "prettier": LinterConfig(enabled=True)
            }
        
        if self.ai_config is None:
            self.ai_config = AIConfig()
        
        if self.review_categories is None:
            self.review_categories = [
                "code_quality",
                "security",
                "performance", 
                "maintainability",
                "documentation"
            ]
        
        if self.language_rules is None:
            self.language_rules = {
                "python": {
                    "type_hints": True,
                    "docstrings": True,
                    "imports": "isort",
                    "formatting": "black"
                },
                "javascript": {
                    "es6_features": True,
                    "async_await": True,
                    "error_handling": True
                },
                "typescript": {
                    "strict_types": True,
                    "interface_usage": True,
                    "generic_types": True
                },
                "react": {
                    "hooks_rules": True,
                    "component_structure": True,
                    "state_management": True
                }
            }

# Default configuration
DEFAULT_CONFIG = ReviewConfig()

# Custom configurations for different project types
WEB_APP_CONFIG = ReviewConfig(
    review_categories=["security", "performance", "accessibility"],
    language_rules={
        "javascript": {
            "es6_features": True,
            "async_await": True,
            "error_handling": True,
            "security_best_practices": True
        },
        "react": {
            "hooks_rules": True,
            "component_structure": True,
            "state_management": True,
            "performance_optimization": True
        }
    }
)

API_CONFIG = ReviewConfig(
    review_categories=["security", "performance", "documentation"],
    language_rules={
        "python": {
            "type_hints": True,
            "docstrings": True,
            "error_handling": True,
            "input_validation": True
        }
    }
)

DATA_SCIENCE_CONFIG = ReviewConfig(
    review_categories=["code_quality", "performance", "documentation"],
    language_rules={
        "python": {
            "type_hints": True,
            "docstrings": True,
            "numpy_pandas_best_practices": True,
            "memory_optimization": True
        }
    }
)

# Custom prompts for different review categories
REVIEW_PROMPTS = {
    "security": """
    Focus on security vulnerabilities:
    - SQL injection prevention
    - XSS protection
    - Input validation
    - Authentication/authorization
    - Secure coding practices
    """,
    
    "performance": """
    Focus on performance optimization:
    - Algorithm efficiency
    - Memory usage
    - Database query optimization
    - Caching strategies
    - Resource management
    """,
    
    "maintainability": """
    Focus on code maintainability:
    - Code organization
    - Naming conventions
    - Function/method complexity
    - Code duplication
    - Modularity
    """,
    
    "documentation": """
    Focus on documentation quality:
    - Function/method documentation
    - Code comments
    - README files
    - API documentation
    - Inline documentation
    """
}

# Severity levels for issues
SEVERITY_LEVELS = {
    "critical": "🔴 Critical - Must fix immediately",
    "high": "🟠 High - Should fix soon",
    "medium": "🟡 Medium - Consider fixing",
    "low": "🟢 Low - Nice to have",
    "info": "ℹ️ Info - FYI only"
}

# Custom rules for specific frameworks
FRAMEWORK_RULES = {
    "django": {
        "check_orm_usage": True,
        "check_security_middleware": True,
        "check_url_patterns": True
    },
    "flask": {
        "check_blueprint_usage": True,
        "check_error_handling": True,
        "check_security_headers": True
    },
    "express": {
        "check_middleware_order": True,
        "check_error_handling": True,
        "check_route_security": True
    },
    "react": {
        "check_hooks_dependencies": True,
        "check_prop_types": True,
        "check_memoization": True
    }
}

def get_config_for_project_type(project_type: str) -> ReviewConfig:
    """Get appropriate configuration based on project type"""
    configs = {
        "web_app": WEB_APP_CONFIG,
        "api": API_CONFIG,
        "data_science": DATA_SCIENCE_CONFIG,
        "default": DEFAULT_CONFIG
    }
    return configs.get(project_type, DEFAULT_CONFIG)

def customize_prompt_for_language(language: str, base_prompt: str) -> str:
    """Customize AI prompt based on programming language"""
    language_specific = {
        "python": "\n\nPay special attention to Python best practices, PEP 8 compliance, and type hints.",
        "javascript": "\n\nFocus on ES6+ features, async/await patterns, and modern JavaScript practices.",
        "typescript": "\n\nEmphasize TypeScript-specific features like strict typing, interfaces, and generics.",
        "react": "\n\nConsider React best practices, hooks rules, component structure, and performance optimization."
    }
    
    return base_prompt + language_specific.get(language.lower(), "") 