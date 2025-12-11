"""
Intent-to-Module Generator
==========================

Transforms natural language business intent into LJPW-balanced Python modules.

This is the missing piece for autopoietic enterprise software.
Instead of "writing code", users express intent and the system grows.

Architecture:
    INTENT → PARSE → ENTITIES → TEMPLATE → MODULE → HEAL → DEPLOY

Example:
    intent = "Create a loan application tracking system"
    module = generator.grow(intent)
    # → Creates loans.py with LoanApplication class, validation, logging, docs
"""

import os
import re
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from .engine import AutopoiesisEngine


# =============================================================================
# DOMAIN KNOWLEDGE
# =============================================================================

# Financial domain entities and their typical attributes
FINANCIAL_ENTITIES = {
    'loan': {
        'class_name': 'Loan',
        'attributes': [
            ('id', 'str', 'Unique identifier'),
            ('amount', 'float', 'Loan principal amount'),
            ('interest_rate', 'float', 'Annual interest rate'),
            ('term_months', 'int', 'Loan duration in months'),
            ('status', 'str', 'Current status: pending, approved, disbursed, closed'),
            ('applicant_id', 'str', 'Reference to applicant'),
            ('created_at', 'datetime', 'Creation timestamp'),
        ],
        'operations': ['create', 'approve', 'disburse', 'close', 'calculate_payment'],
    },
    
    'account': {
        'class_name': 'Account',
        'attributes': [
            ('id', 'str', 'Unique identifier'),
            ('account_number', 'str', 'Account number'),
            ('account_type', 'str', 'Type: savings, current, fixed_deposit'),
            ('balance', 'float', 'Current balance'),
            ('currency', 'str', 'Currency code'),
            ('holder_id', 'str', 'Account holder reference'),
            ('status', 'str', 'Status: active, frozen, closed'),
            ('created_at', 'datetime', 'Creation timestamp'),
        ],
        'operations': ['create', 'deposit', 'withdraw', 'transfer', 'freeze', 'close'],
    },
    
    'payment': {
        'class_name': 'Payment',
        'attributes': [
            ('id', 'str', 'Unique identifier'),
            ('amount', 'float', 'Payment amount'),
            ('from_account', 'str', 'Source account'),
            ('to_account', 'str', 'Destination account'),
            ('status', 'str', 'Status: pending, processing, completed, failed'),
            ('reference', 'str', 'Payment reference'),
            ('created_at', 'datetime', 'Creation timestamp'),
        ],
        'operations': ['initiate', 'process', 'complete', 'reverse'],
    },
    
    'customer': {
        'class_name': 'Customer',
        'attributes': [
            ('id', 'str', 'Unique identifier'),
            ('name', 'str', 'Full name'),
            ('email', 'str', 'Email address'),
            ('phone', 'str', 'Phone number'),
            ('kyc_status', 'str', 'KYC status: pending, verified, rejected'),
            ('risk_rating', 'str', 'Risk rating: low, medium, high'),
            ('created_at', 'datetime', 'Registration timestamp'),
        ],
        'operations': ['register', 'verify_kyc', 'update_profile', 'assess_risk'],
    },
    
    'transaction': {
        'class_name': 'Transaction',
        'attributes': [
            ('id', 'str', 'Unique identifier'),
            ('type', 'str', 'Transaction type'),
            ('amount', 'float', 'Transaction amount'),
            ('account_id', 'str', 'Related account'),
            ('description', 'str', 'Transaction description'),
            ('timestamp', 'datetime', 'Transaction timestamp'),
        ],
        'operations': ['record', 'reverse', 'query'],
    },
    
    'collateral': {
        'class_name': 'Collateral',
        'attributes': [
            ('id', 'str', 'Unique identifier'),
            ('type', 'str', 'Collateral type: property, vehicle, securities'),
            ('value', 'float', 'Estimated value'),
            ('loan_id', 'str', 'Associated loan'),
            ('status', 'str', 'Status: pending_valuation, verified, released'),
            ('verified_at', 'datetime', 'Verification timestamp'),
        ],
        'operations': ['register', 'valuate', 'verify', 'release'],
    },
}

# Keywords that map to entities
ENTITY_KEYWORDS = {
    'loan': ['loan', 'lending', 'borrow', 'credit', 'mortgage'],
    'account': ['account', 'balance', 'savings', 'deposit'],
    'payment': ['payment', 'pay', 'transfer', 'remit', 'send money'],
    'customer': ['customer', 'client', 'user', 'member', 'applicant'],
    'transaction': ['transaction', 'movement', 'activity', 'ledger'],
    'collateral': ['collateral', 'security', 'guarantee', 'asset'],
}


@dataclass
class ParsedIntent:
    """Parsed representation of user intent."""
    raw_intent: str
    entities: List[str]
    operations: List[str]
    constraints: List[str]
    module_name: str
    description: str


@dataclass
class GeneratedModule:
    """A generated module ready for deployment."""
    path: str
    content: str
    entities: List[str]
    operations: List[str]
    ljpw_target: Dict[str, float]
    harmony_score: float = 0.0
    healed: bool = False


class IntentParser:
    """Parses natural language intent into structured components."""
    
    def parse(self, intent: str) -> ParsedIntent:
        """
        Parse natural language intent.
        
        Args:
            intent: Natural language business requirement
            
        Returns:
            ParsedIntent with extracted entities and operations
        """
        intent_lower = intent.lower()
        
        # Extract entities from keywords
        entities = []
        for entity, keywords in ENTITY_KEYWORDS.items():
            if any(kw in intent_lower for kw in keywords):
                entities.append(entity)
        
        # Default to generic if no entities found
        if not entities:
            entities = ['entity']
        
        # Extract operations from verbs
        operations = []
        operation_verbs = {
            'create': ['create', 'add', 'new', 'register'],
            'update': ['update', 'modify', 'change', 'edit'],
            'delete': ['delete', 'remove', 'cancel'],
            'approve': ['approve', 'accept', 'confirm'],
            'reject': ['reject', 'deny', 'decline'],
            'track': ['track', 'monitor', 'watch', 'follow'],
            'calculate': ['calculate', 'compute', 'determine'],
            'validate': ['validate', 'verify', 'check'],
            'report': ['report', 'generate', 'export'],
        }
        
        for op, verbs in operation_verbs.items():
            if any(v in intent_lower for v in verbs):
                operations.append(op)
        
        # Default operations
        if not operations:
            operations = ['create', 'get', 'update', 'delete']  # CRUD
        
        # Extract constraints (numbers, thresholds)
        constraints = []
        amount_match = re.search(r'\$?([\d,]+)', intent)
        if amount_match:
            constraints.append(f"threshold_{amount_match.group(1).replace(',', '')}")
        
        # Generate module name
        module_name = '_'.join(entities) + 's'  # e.g., "loans"
        
        # Generate description
        description = f"Module for managing {', '.join(entities)}"
        
        return ParsedIntent(
            raw_intent=intent,
            entities=entities,
            operations=operations,
            constraints=constraints,
            module_name=module_name,
            description=description
        )


class ModuleGenerator:
    """Generates LJPW-balanced Python modules from parsed intent."""
    
    def __init__(self):
        self.parser = IntentParser()
    
    def generate(self, parsed: ParsedIntent) -> str:
        """
        Generate a complete Python module from parsed intent.
        
        The generated module will have high LJPW scores:
        - Love: Comprehensive documentation
        - Justice: Input validation on all methods
        - Power: Error handling throughout
        - Wisdom: Logging infrastructure
        
        Args:
            parsed: Parsed intent
            
        Returns:
            Complete Python module as string
        """
        lines = []
        
        # Module docstring (Love)
        lines.extend(self._generate_module_header(parsed))
        
        # Imports
        lines.extend(self._generate_imports())
        
        # Logging setup (Wisdom)
        lines.extend(self._generate_logging())
        
        # Generate each entity class
        for entity in parsed.entities:
            if entity in FINANCIAL_ENTITIES:
                entity_def = FINANCIAL_ENTITIES[entity]
            else:
                entity_def = self._create_generic_entity(entity)
            
            lines.extend(self._generate_class(entity_def, parsed))
        
        # Generate service class
        lines.extend(self._generate_service(parsed))
        
        return '\n'.join(lines)
    
    def _generate_module_header(self, parsed: ParsedIntent) -> List[str]:
        """Generate module docstring with full documentation (Love dimension)."""
        return [
            '"""',
            f'{parsed.module_name.title()} Module',
            '=' * len(f'{parsed.module_name.title()} Module'),
            '',
            f'Generated from intent: "{parsed.raw_intent}"',
            f'Created: {datetime.now().isoformat()}',
            '',
            'This module was auto-generated with LJPW principles:',
            '- Love: Comprehensive documentation',
            '- Justice: Input validation on all public methods',
            '- Power: Error handling for resilience',
            '- Wisdom: Logging for observability',
            '',
            f'Entities: {", ".join(parsed.entities)}',
            f'Operations: {", ".join(parsed.operations)}',
            '"""',
            '',
        ]
    
    def _generate_imports(self) -> List[str]:
        """Generate import statements."""
        return [
            'import logging',
            'import uuid',
            'from datetime import datetime',
            'from typing import Dict, List, Optional, Any',
            'from dataclasses import dataclass, field',
            'from enum import Enum',
            '',
        ]
    
    def _generate_logging(self) -> List[str]:
        """Generate logging infrastructure (Wisdom dimension)."""
        return [
            '# Logging infrastructure (Wisdom dimension)',
            '_logger = logging.getLogger(__name__)',
            'if not _logger.handlers:',
            '    _handler = logging.StreamHandler()',
            '    _handler.setFormatter(logging.Formatter(',
            "        '%(asctime)s [%(levelname)s] %(name)s: %(message)s'",
            '    ))',
            '    _logger.addHandler(_handler)',
            '    _logger.setLevel(logging.INFO)',
            '',
            '',
        ]
    
    def _generate_class(self, entity_def: Dict, parsed: ParsedIntent) -> List[str]:
        """Generate a complete entity class with LJPW principles."""
        class_name = entity_def['class_name']
        attributes = entity_def['attributes']
        operations = entity_def['operations']
        
        lines = []
        
        # Status enum if entity has status
        if any(attr[0] == 'status' for attr in attributes):
            lines.extend([
                f'class {class_name}Status(Enum):',
                '    """Status enumeration for state management."""',
            ])
            # Generate status values based on entity type
            if class_name == 'Loan':
                lines.extend([
                    '    PENDING = "pending"',
                    '    APPROVED = "approved"',
                    '    DISBURSED = "disbursed"',
                    '    CLOSED = "closed"',
                    '    REJECTED = "rejected"',
                ])
            else:
                lines.extend([
                    '    PENDING = "pending"',
                    '    ACTIVE = "active"',
                    '    COMPLETED = "completed"',
                    '    CANCELLED = "cancelled"',
                ])
            lines.append('')
            lines.append('')
        
        # Class definition
        lines.extend([
            '@dataclass',
            f'class {class_name}:',
            '    """',
            f'    {class_name} entity.',
            '    ',
            f'    Auto-generated entity for managing {class_name.lower()} data.',
            '    Implements LJPW principles for self-healing capability.',
            '    """',
        ])
        
        # Attributes
        for attr_name, attr_type, attr_doc in attributes:
            py_type = self._map_type(attr_type)
            default = self._get_default(attr_name, attr_type)
            lines.append(f'    {attr_name}: {py_type}{default}  # {attr_doc}')
        
        lines.append('')
        
        # Validation method (Justice dimension)
        lines.extend([
            '    def validate(self) -> bool:',
            '        """',
            f'        Validate {class_name} data integrity.',
            '        ',
            '        Returns:',
            '            bool: True if valid, raises ValueError otherwise',
            '        """',
            f'        _logger.debug(f"Validating {class_name} {{self.id}}")',
        ])
        
        # Add validation rules
        for attr_name, attr_type, _ in attributes:
            if attr_type == 'str' and attr_name not in ['id', 'created_at']:
                lines.append(f'        if not self.{attr_name}:')
                lines.append(f'            raise ValueError("{attr_name} is required")')
            elif attr_type == 'float' and 'amount' in attr_name or 'value' in attr_name:
                lines.append(f'        if self.{attr_name} < 0:')
                lines.append(f'            raise ValueError("{attr_name} must be non-negative")')
        
        lines.extend([
            f'        _logger.info(f"{class_name} {{self.id}} validated successfully")',
            '        return True',
            '',
        ])
        
        lines.append('')
        return lines
    
    def _generate_service(self, parsed: ParsedIntent) -> List[str]:
        """Generate service class with all operations."""
        service_name = f'{parsed.module_name.title().replace("_", "")}Service'
        
        lines = [
            f'class {service_name}:',
            '    """',
            f'    Service layer for {parsed.module_name} operations.',
            '    ',
            '    Provides business logic with LJPW-compliant implementation:',
            '    - All inputs validated (Justice)',
            '    - All operations logged (Wisdom)',
            '    - All errors handled (Power)',
            '    """',
            '',
            '    def __init__(self):',
            '        """Initialize service with empty storage."""',
            '        self._storage: Dict[str, Any] = {}',
            f'        _logger.info("{service_name} initialized")',
            '',
        ]
        
        # Generate CRUD operations
        for entity in parsed.entities:
            if entity in FINANCIAL_ENTITIES:
                entity_def = FINANCIAL_ENTITIES[entity]
                class_name = entity_def['class_name']
            else:
                class_name = entity.title()
            
            # Create
            lines.extend([
                f'    def create_{entity}(self, **kwargs) -> {class_name}:',
                '        """',
                f'        Create a new {class_name}.',
                '        ',
                '        Args:',
                '            **kwargs: Entity attributes',
                '            ',
                '        Returns:',
                f'            {class_name}: The created entity',
                '            ',
                '        Raises:',
                '            ValueError: If validation fails',
                '            RuntimeError: If creation fails',
                '        """',
                '        # Input validation (Justice)',
                '        if not kwargs:',
                '            raise ValueError("At least one attribute is required")',
                '',
                f'        _logger.debug(f"Creating {class_name} with {{kwargs}}")',
                '',
                '        # Error handling (Power)',
                '        try:',
                "            entity_id = str(uuid.uuid4())[:8]",
                f"            entity = {class_name}(id=entity_id, **kwargs)",
                '            entity.validate()',
                '            self._storage[entity_id] = entity',
                f'            _logger.info(f"Created {class_name} {{entity_id}}")',
                '            return entity',
                '        except Exception as e:',
                f'            _logger.error(f"Failed to create {class_name}: {{e}}")',
                '            raise RuntimeError(f"Creation failed: {e}") from e',
                '',
            ])
            
            # Get
            lines.extend([
                f'    def get_{entity}(self, entity_id: str) -> Optional[{class_name}]:',
                '        """',
                f'        Retrieve a {class_name} by ID.',
                '        ',
                '        Args:',
                '            entity_id: The entity identifier',
                '            ',
                '        Returns:',
                f'            {class_name} or None if not found',
                '        """',
                '        # Input validation (Justice)',
                '        if not isinstance(entity_id, str):',
                '            raise TypeError("entity_id must be a string")',
                '',
                f'        _logger.debug(f"Retrieving {class_name} {{entity_id}}")',
                '        return self._storage.get(entity_id)',
                '',
            ])
            
            # List
            lines.extend([
                f'    def list_{entity}s(self) -> List[{class_name}]:',
                '        """',
                f'        List all {class_name} entities.',
                '        ',
                '        Returns:',
                f'            List of {class_name} entities',
                '        """',
                f'        _logger.debug("Listing all {class_name}s")',
                f'        return [e for e in self._storage.values() if isinstance(e, {class_name})]',
                '',
            ])
        
        return lines
    
    def _create_generic_entity(self, entity: str) -> Dict:
        """Create a generic entity definition."""
        return {
            'class_name': entity.title(),
            'attributes': [
                ('id', 'str', 'Unique identifier'),
                ('name', 'str', 'Entity name'),
                ('status', 'str', 'Current status'),
                ('created_at', 'datetime', 'Creation timestamp'),
            ],
            'operations': ['create', 'get', 'update', 'delete'],
        }
    
    def _map_type(self, type_str: str) -> str:
        """Map simple types to Python types."""
        mapping = {
            'str': 'str',
            'int': 'int',
            'float': 'float',
            'bool': 'bool',
            'datetime': 'datetime',
        }
        return mapping.get(type_str, 'Any')
    
    def _get_default(self, attr_name: str, attr_type: str) -> str:
        """Get default value for attribute."""
        if attr_name == 'id':
            return ' = field(default_factory=lambda: str(uuid.uuid4())[:8])'
        elif attr_name == 'created_at':
            return ' = field(default_factory=datetime.now)'
        elif attr_name == 'status':
            return ' = "pending"'
        elif attr_type == 'float':
            return ' = 0.0'
        elif attr_type == 'int':
            return ' = 0'
        elif attr_type == 'str':
            return ' = ""'
        return ''


class IntentToModuleGenerator:
    """
    Main generator that transforms intent into self-healing modules.
    
    This is the bridge between natural language and autopoietic code.
    """
    
    def __init__(self, output_dir: str = '.'):
        """
        Initialize the generator.
        
        Args:
            output_dir: Directory to write generated modules
        """
        self.output_dir = Path(output_dir)
        self.parser = IntentParser()
        self.module_generator = ModuleGenerator()
    
    def grow(self, intent: str, auto_heal: bool = True) -> GeneratedModule:
        """
        Grow a new module from natural language intent.
        
        This is the main entry point for intent-to-code generation.
        
        Args:
            intent: Natural language business requirement
            auto_heal: Whether to automatically run autopoiesis healing
            
        Returns:
            GeneratedModule with path, content, and LJPW metrics
        """
        print(f"\n{'='*60}")
        print(f"  GROWING MODULE FROM INTENT")
        print(f"{'='*60}")
        print(f"\n  Intent: \"{intent}\"")
        
        # Parse intent
        print(f"\n  Parsing intent...")
        parsed = self.parser.parse(intent)
        print(f"    Entities: {parsed.entities}")
        print(f"    Operations: {parsed.operations}")
        print(f"    Module name: {parsed.module_name}")
        
        # Generate module
        print(f"\n  Generating LJPW-balanced module...")
        content = self.module_generator.generate(parsed)
        
        # Write to file
        module_path = self.output_dir / f"{parsed.module_name}.py"
        with open(module_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"    Written to: {module_path}")
        
        # Create result
        result = GeneratedModule(
            path=str(module_path),
            content=content,
            entities=parsed.entities,
            operations=parsed.operations,
            ljpw_target={'L': 0.9, 'J': 0.9, 'P': 0.9, 'W': 0.9}
        )
        
        # Auto-heal if requested
        if auto_heal:
            print(f"\n  Running autopoiesis healing...")
            engine = AutopoiesisEngine(str(module_path), dry_run=False)
            engine.analyze()
            result.harmony_score = engine.current_report.harmony
            result.healed = True
            print(f"    Harmony score: {result.harmony_score:.3f}")
        
        print(f"\n{'='*60}")
        print(f"  MODULE GROWN SUCCESSFULLY")
        print(f"{'='*60}\n")
        
        return result


# Convenience function
def grow(intent: str, output_dir: str = '.', auto_heal: bool = True) -> GeneratedModule:
    """
    Convenience function to grow a module from intent.
    
    Args:
        intent: Natural language business requirement
        output_dir: Where to write the generated module
        auto_heal: Whether to run autopoiesis healing
        
    Returns:
        GeneratedModule
        
    Example:
        >>> module = grow("Create a loan application tracking system")
        >>> print(module.path)
        ./loans.py
    """
    generator = IntentToModuleGenerator(output_dir)
    return generator.grow(intent, auto_heal)
