"""
Test Enhanced LJPW Analyzer on Gold-Standard Code

This tests whether the analyzer can find improvement opportunities
even in production-quality, well-architected code.

We'll analyze code based on industry best practices and see what
the enhanced metrics reveal.
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from enhanced_ljpw_analyzer import EnhancedLJPWAnalyzer


# ==============================================================================
# GOLD STANDARD CODE
# Based on best practices from requests, flask, click libraries
# ==============================================================================

GOLD_STANDARD_CODE = '''
"""
HTTP Client Library - Gold Standard Implementation

Based on best practices from:
- requests library (Kenneth Reitz)
- urllib3 (Andrey Petrov)
- httpx (Tom Christie)

Features:
- Comprehensive documentation
- Type hints throughout
- Robust error handling
- Clean architecture
- High cohesion, low coupling
- Extensive logging
"""

from typing import Optional, Dict, Any, Union, List
from dataclasses import dataclass, field
from enum import Enum
from urllib.parse import urljoin, urlparse
import logging
import json
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


# ==============================================================================
# CONSTANTS & ENUMS
# ==============================================================================

class HTTPMethod(Enum):
    """HTTP methods."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class HTTPStatus(Enum):
    """Common HTTP status codes."""
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_ERROR = 500


# Configuration constants
DEFAULT_TIMEOUT = 30.0
MAX_REDIRECTS = 10
DEFAULT_USER_AGENT = "PythonHTTPClient/1.0"
CHUNK_SIZE = 8192


# ==============================================================================
# EXCEPTIONS
# ==============================================================================

class HTTPError(Exception):
    """Base exception for HTTP errors."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        """
        Initialize HTTP error.

        Args:
            message: Error message
            status_code: HTTP status code if applicable
        """
        super().__init__(message)
        self.status_code = status_code
        self.message = message


class ConnectionError(HTTPError):
    """Connection-related errors."""
    pass


class TimeoutError(HTTPError):
    """Request timeout errors."""
    pass


class InvalidURLError(HTTPError):
    """Invalid URL errors."""
    pass


# ==============================================================================
# DATA MODELS
# ==============================================================================

@dataclass
class Response:
    """HTTP response with rich metadata."""

    status_code: int
    headers: Dict[str, str]
    content: bytes
    url: str
    encoding: str = "utf-8"
    elapsed: Optional[timedelta] = None

    @property
    def text(self) -> str:
        """Decode response content as text."""
        return self.content.decode(self.encoding)

    @property
    def json(self) -> Any:
        """Parse response as JSON."""
        try:
            return json.loads(self.text)
        except json.JSONDecodeError as e:
            raise HTTPError(f"Invalid JSON response: {e}")

    @property
    def ok(self) -> bool:
        """Check if response status indicates success."""
        return 200 <= self.status_code < 300

    def raise_for_status(self) -> None:
        """Raise exception for error status codes."""
        if not self.ok:
            raise HTTPError(
                f"HTTP {self.status_code} error",
                status_code=self.status_code
            )


@dataclass
class Request:
    """HTTP request with all parameters."""

    method: HTTPMethod
    url: str
    headers: Dict[str, str] = field(default_factory=dict)
    params: Dict[str, str] = field(default_factory=dict)
    data: Optional[Union[str, bytes, Dict]] = None
    json_data: Optional[Any] = None
    timeout: float = DEFAULT_TIMEOUT

    def __post_init__(self):
        """Validate and normalize request."""
        self._validate_url()
        self._set_default_headers()

    def _validate_url(self) -> None:
        """Validate URL format."""
        parsed = urlparse(self.url)
        if not parsed.scheme or not parsed.netloc:
            raise InvalidURLError(f"Invalid URL: {self.url}")
        logger.debug(f"URL validated: {self.url}")

    def _set_default_headers(self) -> None:
        """Set default headers if not provided."""
        if 'User-Agent' not in self.headers:
            self.headers['User-Agent'] = DEFAULT_USER_AGENT

        if self.json_data is not None:
            self.headers['Content-Type'] = 'application/json'


# ==============================================================================
# CONNECTION POOL
# ==============================================================================

class ConnectionPool:
    """
    Manage reusable connections.

    Implements connection pooling for efficiency:
    - Reuses existing connections
    - Manages connection lifecycle
    - Thread-safe operations
    """

    def __init__(self, max_connections: int = 10):
        """
        Initialize connection pool.

        Args:
            max_connections: Maximum number of pooled connections
        """
        self.max_connections = max_connections
        self._connections: Dict[str, Any] = {}
        self._connection_count = 0
        logger.info(f"ConnectionPool initialized: max={max_connections}")

    def get_connection(self, host: str) -> Any:
        """
        Get connection for host.

        Args:
            host: Target host

        Returns:
            Connection object
        """
        if host in self._connections:
            logger.debug(f"Reusing connection for {host}")
            return self._connections[host]

        if self._connection_count >= self.max_connections:
            logger.warning("Connection pool full, reusing oldest")
            # In real implementation: LRU eviction
            oldest_host = list(self._connections.keys())[0]
            del self._connections[oldest_host]
            self._connection_count -= 1

        logger.info(f"Creating new connection for {host}")
        connection = self._create_connection(host)
        self._connections[host] = connection
        self._connection_count += 1

        return connection

    def _create_connection(self, host: str) -> Any:
        """Create new connection."""
        # Placeholder for actual connection logic
        return {"host": host, "created_at": datetime.now()}

    def close_all(self) -> None:
        """Close all pooled connections."""
        count = len(self._connections)
        self._connections.clear()
        self._connection_count = 0
        logger.info(f"Closed {count} connections")


# ==============================================================================
# SESSION MANAGEMENT
# ==============================================================================

class Session:
    """
    HTTP session with persistent configuration.

    Features:
    - Persistent cookies
    - Connection pooling
    - Custom headers
    - Authentication
    """

    def __init__(self):
        """Initialize session."""
        self.headers: Dict[str, str] = {}
        self.cookies: Dict[str, str] = {}
        self.auth: Optional[tuple] = None
        self._pool = ConnectionPool()
        logger.info("Session created")

    def request(
        self,
        method: Union[HTTPMethod, str],
        url: str,
        **kwargs
    ) -> Response:
        """
        Send HTTP request.

        Args:
            method: HTTP method
            url: Target URL
            **kwargs: Additional request parameters

        Returns:
            Response object

        Raises:
            HTTPError: On request failure
            TimeoutError: On timeout
            ConnectionError: On connection failure
        """
        # Convert string method to enum
        if isinstance(method, str):
            method = HTTPMethod(method.upper())

        # Merge session headers with request headers
        headers = {**self.headers, **kwargs.get('headers', {})}
        kwargs['headers'] = headers

        # Create request
        request = Request(method=method, url=url, **kwargs)

        # Send request
        logger.info(f"{method.value} {url}")
        start_time = datetime.now()

        try:
            response = self._send(request)
            elapsed = datetime.now() - start_time
            response.elapsed = elapsed

            logger.info(
                f"Response: {response.status_code} in {elapsed.total_seconds():.2f}s"
            )

            return response

        except Exception as e:
            logger.error(f"Request failed: {e}")
            raise

    def _send(self, request: Request) -> Response:
        """
        Internal method to send request.

        Args:
            request: Request object

        Returns:
            Response object
        """
        # Get connection from pool
        parsed = urlparse(request.url)
        host = f"{parsed.scheme}://{parsed.netloc}"
        connection = self._pool.get_connection(host)

        # Simulate HTTP request (placeholder)
        # In real implementation: use connection to send request
        return Response(
            status_code=200,
            headers={'Content-Type': 'application/json'},
            content=b'{"status": "ok"}',
            url=request.url
        )

    def get(self, url: str, **kwargs) -> Response:
        """Send GET request."""
        return self.request(HTTPMethod.GET, url, **kwargs)

    def post(self, url: str, **kwargs) -> Response:
        """Send POST request."""
        return self.request(HTTPMethod.POST, url, **kwargs)

    def put(self, url: str, **kwargs) -> Response:
        """Send PUT request."""
        return self.request(HTTPMethod.PUT, url, **kwargs)

    def delete(self, url: str, **kwargs) -> Response:
        """Send DELETE request."""
        return self.request(HTTPMethod.DELETE, url, **kwargs)

    def close(self) -> None:
        """Close session and cleanup resources."""
        self._pool.close_all()
        logger.info("Session closed")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# ==============================================================================
# CONVENIENCE FUNCTIONS
# ==============================================================================

def request(
    method: Union[HTTPMethod, str],
    url: str,
    **kwargs
) -> Response:
    """
    Send HTTP request (convenience function).

    Args:
        method: HTTP method
        url: Target URL
        **kwargs: Additional parameters

    Returns:
        Response object
    """
    with Session() as session:
        return session.request(method, url, **kwargs)


def get(url: str, **kwargs) -> Response:
    """Send GET request."""
    return request(HTTPMethod.GET, url, **kwargs)


def post(url: str, **kwargs) -> Response:
    """Send POST request."""
    return request(HTTPMethod.POST, url, **kwargs)


def put(url: str, **kwargs) -> Response:
    """Send PUT request."""
    return request(HTTPMethod.PUT, url, **kwargs)


def delete(url: str, **kwargs) -> Response:
    """Send DELETE request."""
    return request(HTTPMethod.DELETE, url, **kwargs)
'''


# ==============================================================================
# ANALYZE GOLD STANDARD CODE
# ==============================================================================

def analyze_gold_standard():
    """Analyze gold-standard code with enhanced metrics."""

    print("╔" + "=" * 78 + "╗")
    print("║" + "GOLD STANDARD CODE ANALYSIS".center(78) + "║")
    print("║" + "Testing Enhanced Analyzer on Production-Quality Code".center(78) + "║")
    print("╚" + "=" * 78 + "╝\n")

    print("📚 Code being analyzed:")
    print("  • HTTP Client Library (requests-style)")
    print("  • Based on best practices from Kenneth Reitz, Tom Christie")
    print("  • Features:")
    print("    - Comprehensive documentation")
    print("    - Full type hints")
    print("    - Enums for constants")
    print("    - Exception hierarchy")
    print("    - Connection pooling")
    print("    - Session management")
    print("    - Context managers")
    print()

    analyzer = EnhancedLJPWAnalyzer(quiet=True)
    result = analyzer.analyze_code(GOLD_STANDARD_CODE)

    analyzer.print_detailed_report(result, GOLD_STANDARD_CODE)

    # Analyze specific areas
    print("\n\n" + "=" * 80)
    print("DETAILED FINDINGS")
    print("=" * 80)

    print("\n✅ STRENGTHS:")
    print("-" * 80)

    strengths = []

    if result.patterns.get('docstrings', 0) > 10:
        strengths.append(f"Excellent documentation ({result.patterns['docstrings']} docstrings)")

    if result.patterns.get('type_hints', 0) > 20:
        strengths.append(f"Comprehensive type hints ({result.patterns['type_hints']} type annotations)")

    if result.patterns.get('classes', 0) > 5:
        strengths.append(f"Well-structured OOP ({result.patterns['classes']} classes)")

    if result.patterns.get('constants', 0) > 3:
        strengths.append(f"Good use of constants ({result.patterns['constants']} defined)")

    if result.complexity.avg_complexity < 5:
        strengths.append(f"Low complexity (avg {result.complexity.avg_complexity:.1f})")

    if result.coupling.coupling_score < 0.4:
        strengths.append(f"Low coupling ({result.coupling.coupling_score:.2f})")

    if result.cohesion.avg_cohesion > 0.6:
        strengths.append(f"High cohesion ({result.cohesion.avg_cohesion:.2f})")

    for strength in strengths:
        print(f"  ✓ {strength}")

    # Areas for improvement (even in gold standard code)
    print("\n📋 POTENTIAL IMPROVEMENTS:")
    print("-" * 80)

    improvements = []

    if result.patterns.get('try_except', 0) < result.patterns.get('functions', 1) * 0.3:
        improvements.append(
            f"Could add more error handling (only {result.patterns.get('try_except', 0)} try/except blocks)"
        )

    if result.patterns.get('logging_calls', 0) < result.patterns.get('functions', 1) * 0.5:
        improvements.append(
            f"Could add more logging ({result.patterns.get('logging_calls', 0)} log calls for {result.patterns.get('functions', 0)} functions)"
        )

    if result.complexity.high_complexity_functions:
        for name, comp in result.complexity.high_complexity_functions[:3]:
            improvements.append(
                f"Function '{name}' has complexity {comp} (consider refactoring)"
            )

    if result.cohesion.low_cohesion_classes:
        for class_name in result.cohesion.low_cohesion_classes[:3]:
            improvements.append(
                f"Class '{class_name}' has low cohesion (consider splitting responsibilities)"
            )

    if result.coupling.coupling_score > 0.3:
        improvements.append(
            f"Coupling could be reduced ({result.coupling.coupling_score:.2f} > 0.3 target)"
        )

    if len(result.dependencies.third_party_imports) > 5:
        improvements.append(
            f"Many third-party dependencies ({len(result.dependencies.third_party_imports)} packages)"
        )

    if improvements:
        for improvement in improvements:
            print(f"  • {improvement}")
    else:
        print("  🌟 No significant improvements needed - truly gold standard!")

    # Comparison with thresholds
    print("\n\n" + "=" * 80)
    print("COMPARISON WITH EXCELLENCE THRESHOLDS")
    print("=" * 80)

    thresholds = [
        ("Love", result.love, 0.8, "High documentation, clarity"),
        ("Justice", result.justice, 0.7, "Strong validation, error handling"),
        ("Power", result.power, 0.6, "Efficient implementation"),
        ("Wisdom", result.wisdom, 0.8, "Excellent architecture"),
        ("Harmony", result.harmony, 0.7, "Overall excellence"),
    ]

    print(f"\n  {'Dimension':<15} {'Score':>8} {'Target':>8} {'Status':>10} {'Notes'}")
    print("-" * 80)

    for name, score, target, notes in thresholds:
        if score >= target:
            status = "✅ Exceeds"
            symbol = "✅"
        elif score >= target * 0.9:
            status = "⚠️  Close"
            symbol = "⚠️"
        else:
            status = "❌ Below"
            symbol = "❌"

        print(f"  {name:<15} {score:>8.2f} {target:>8.2f} {status:>10}  {notes}")

    # Overall assessment
    print("\n\n" + "=" * 80)
    print("FINAL ASSESSMENT")
    print("=" * 80)

    if result.harmony >= 0.7:
        grade = "A+ (Gold Standard)"
        assessment = "Exceptional code quality. This is reference implementation level."
    elif result.harmony >= 0.6:
        grade = "A (Excellent)"
        assessment = "High quality, production-ready code with minor improvement areas."
    elif result.harmony >= 0.5:
        grade = "B (Good)"
        assessment = "Solid code quality with some areas for improvement."
    else:
        grade = "C or below"
        assessment = "Needs refactoring to meet quality standards."

    print(f"\n  Grade: {grade}")
    print(f"  Harmony Score: {result.harmony:.2f}")
    print(f"  Assessment: {assessment}")

    print("\n" + "=" * 80)
    print("METRICS BREAKDOWN")
    print("=" * 80)

    print(f"\n  Complexity:")
    print(f"    • Average: {result.complexity.avg_complexity:.1f} (target: < 5)")
    print(f"    • Maximum: {result.complexity.max_complexity} (target: < 15)")

    print(f"\n  Coupling:")
    print(f"    • Score: {result.coupling.coupling_score:.2f} (target: < 0.3)")
    print(f"    • External deps: {len(result.coupling.external_dependencies)}")

    print(f"\n  Cohesion:")
    print(f"    • Average: {result.cohesion.avg_cohesion:.2f} (target: > 0.7)")
    print(f"    • LCOM: {result.cohesion.lcom_score:.2f} (target: < 0.3)")

    print("\n✨ Analysis complete! Even gold-standard code has measurable metrics.")


if __name__ == "__main__":
    analyze_gold_standard()
