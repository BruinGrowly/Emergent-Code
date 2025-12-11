"""
Test Enhanced LJPW Analyzer

Demonstrates advanced metrics:
- Cyclomatic complexity detection
- Coupling analysis
- Cohesion measurement
- Dependency tracking
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from enhanced_ljpw_analyzer import EnhancedLJPWAnalyzer


# ==============================================================================
# TEST CASE 1: High Complexity Code
# ==============================================================================

HIGH_COMPLEXITY_CODE = '''
def process_order(order_data):
    """Process order with complex business logic."""
    if order_data is None:
        return None

    if 'items' not in order_data:
        return None

    total = 0
    for item in order_data['items']:
        if item['price'] < 0:
            continue

        if item['quantity'] <= 0:
            continue

        if 'discount' in item:
            if item['discount'] > 0 and item['discount'] < 1:
                price = item['price'] * (1 - item['discount'])
            else:
                price = item['price']
        else:
            price = item['price']

        subtotal = price * item['quantity']

        if 'tax_rate' in order_data:
            if order_data['tax_rate'] > 0:
                subtotal = subtotal * (1 + order_data['tax_rate'])

        total += subtotal

    if 'shipping' in order_data:
        if order_data['shipping'] > 0:
            total += order_data['shipping']

    if 'promo_code' in order_data:
        if order_data['promo_code'] == 'SAVE10':
            total = total * 0.9
        elif order_data['promo_code'] == 'SAVE20':
            total = total * 0.8
        elif order_data['promo_code'] == 'SAVE50':
            total = total * 0.5

    return total
'''

# Cyclomatic Complexity: ~20 (very high!)
# - 15+ if statements
# - Nested conditions
# - Multiple branches


# ==============================================================================
# TEST CASE 2: Low Complexity Code (Same Logic, Better Structure)
# ==============================================================================

LOW_COMPLEXITY_CODE = '''
"""Order processing with clean structure."""

from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional

PROMO_CODES = {
    'SAVE10': Decimal('0.10'),
    'SAVE20': Decimal('0.20'),
    'SAVE50': Decimal('0.50')
}


@dataclass
class OrderItem:
    """Order item with pricing."""
    price: Decimal
    quantity: int
    discount: Decimal = Decimal('0')

    def subtotal(self) -> Decimal:
        """Calculate item subtotal."""
        price = self.price * (1 - self.discount)
        return price * self.quantity


class OrderCalculator:
    """Calculate order totals."""

    def __init__(self, tax_rate: Decimal = Decimal('0')):
        self.tax_rate = tax_rate

    def calculate_items_total(self, items: List[OrderItem]) -> Decimal:
        """Sum all item subtotals."""
        return sum(item.subtotal() for item in items)

    def apply_tax(self, amount: Decimal) -> Decimal:
        """Apply tax to amount."""
        return amount * (1 + self.tax_rate)

    def apply_promo(self, amount: Decimal, promo_code: Optional[str]) -> Decimal:
        """Apply promo code discount."""
        if promo_code in PROMO_CODES:
            discount = PROMO_CODES[promo_code]
            return amount * (1 - discount)
        return amount

    def calculate_total(
        self,
        items: List[OrderItem],
        shipping: Decimal = Decimal('0'),
        promo_code: Optional[str] = None
    ) -> Decimal:
        """Calculate final order total."""
        # Sum items
        subtotal = self.calculate_items_total(items)

        # Add tax
        subtotal = self.apply_tax(subtotal)

        # Add shipping
        subtotal += shipping

        # Apply promo
        total = self.apply_promo(subtotal, promo_code)

        return total
'''

# Cyclomatic Complexity: Each function ~2-3 (excellent!)
# - Simple, focused functions
# - No deep nesting
# - Clear separation of concerns


# ==============================================================================
# TEST CASE 3: High Coupling Code
# ==============================================================================

HIGH_COUPLING_CODE = '''
"""Highly coupled module with many dependencies."""

import os
import sys
import json
import re
import datetime
import hashlib
import random
import requests
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sqlalchemy import create_engine
from flask import Flask, request
from redis import Redis
from celery import Celery
import boto3
import stripe

app = Flask(__name__)
redis_client = Redis()
celery_app = Celery()
s3_client = boto3.client('s3')

def process_data():
    """Process with many external dependencies."""
    df = pd.read_csv('data.csv')
    df = df.fillna(0)

    model = LinearRegression()
    model.fit(df[['x']], df['y'])

    stripe.Charge.create(amount=1000, currency='usd')

    return model.predict([[5]])
'''

# Coupling Score: Very high (~0.9)
# - 15+ external imports
# - Multiple third-party dependencies
# - High fan-out


# ==============================================================================
# TEST CASE 4: Low Coupling Code
# ==============================================================================

LOW_COUPLING_CODE = '''
"""Well-isolated module with minimal dependencies."""

from typing import List, Dict
from dataclasses import dataclass


@dataclass
class User:
    """User data model."""
    user_id: str
    email: str
    name: str


class UserRepository:
    """User data access with dependency injection."""

    def __init__(self, storage):
        """Initialize with injected storage."""
        self._storage = storage

    def save(self, user: User) -> None:
        """Save user to storage."""
        self._storage.save(user)

    def find_by_id(self, user_id: str) -> User:
        """Find user by ID."""
        return self._storage.get(user_id)


class UserService:
    """Business logic for users."""

    def __init__(self, repository: UserRepository):
        """Initialize with injected repository."""
        self.repository = repository

    def register_user(self, email: str, name: str) -> User:
        """Register new user."""
        user = User(
            user_id=self._generate_id(),
            email=email,
            name=name
        )
        self.repository.save(user)
        return user

    def _generate_id(self) -> str:
        """Generate unique ID."""
        import uuid
        return str(uuid.uuid4())
'''

# Coupling Score: Low (~0.1)
# - Only typing and dataclasses (stdlib)
# - Dependency injection pattern
# - Low fan-out


# ==============================================================================
# TEST CASE 5: Low Cohesion Class
# ==============================================================================

LOW_COHESION_CODE = '''
"""Class with low cohesion (unrelated methods)."""

class UserManager:
    """Manager doing too many unrelated things."""

    def __init__(self):
        self.users = {}
        self.orders = {}
        self.products = {}

    def add_user(self, user_id, name):
        """Add user."""
        self.users[user_id] = name

    def add_order(self, order_id, total):
        """Add order (unrelated to users)."""
        self.orders[order_id] = total

    def add_product(self, product_id, price):
        """Add product (unrelated to users/orders)."""
        self.products[product_id] = price

    def calculate_tax(self, amount):
        """Calculate tax (uses no instance data)."""
        return amount * 0.08

    def format_date(self, date):
        """Format date (uses no instance data)."""
        return date.strftime('%Y-%m-%d')
'''

# Cohesion: Very low (~0.2)
# - Methods use different attributes
# - No shared state between methods
# - Multiple responsibilities


# ==============================================================================
# TEST CASE 6: High Cohesion Class
# ==============================================================================

HIGH_COHESION_CODE = '''
"""Class with high cohesion (related methods)."""

from typing import Dict, Optional


class ShoppingCart:
    """Shopping cart with focused, cohesive methods."""

    def __init__(self):
        self.items = {}
        self.total = 0.0

    def add_item(self, product_id: str, price: float, quantity: int):
        """Add item to cart."""
        if product_id in self.items:
            self.items[product_id]['quantity'] += quantity
        else:
            self.items[product_id] = {'price': price, 'quantity': quantity}
        self._update_total()

    def remove_item(self, product_id: str):
        """Remove item from cart."""
        if product_id in self.items:
            del self.items[product_id]
            self._update_total()

    def update_quantity(self, product_id: str, quantity: int):
        """Update item quantity."""
        if product_id in self.items:
            self.items[product_id]['quantity'] = quantity
            self._update_total()

    def _update_total(self):
        """Update cart total (all methods use this)."""
        self.total = sum(
            item['price'] * item['quantity']
            for item in self.items.values()
        )

    def get_total(self) -> float:
        """Get cart total."""
        return self.total

    def clear(self):
        """Clear cart."""
        self.items = {}
        self.total = 0.0
'''

# Cohesion: Very high (~0.9)
# - All methods use self.items and self.total
# - Shared state across all methods
# - Single, focused responsibility


# ==============================================================================
# RUN TESTS
# ==============================================================================

def test_complexity():
    """Test cyclomatic complexity detection."""
    print("╔" + "=" * 78 + "╗")
    print("║" + "TEST 1: CYCLOMATIC COMPLEXITY".center(78) + "║")
    print("╚" + "=" * 78 + "╝\n")

    analyzer = EnhancedLJPWAnalyzer(quiet=True)

    print("🔴 HIGH COMPLEXITY CODE:")
    print("  (Nested ifs, complex branching)")
    high_result = analyzer.analyze_code(HIGH_COMPLEXITY_CODE)
    print(f"  Avg Complexity: {high_result.complexity.avg_complexity:.1f}")
    print(f"  Max Complexity: {high_result.complexity.max_complexity}")
    print(f"  Power Score: {high_result.power:.2f} ❌\n")

    print("🟢 LOW COMPLEXITY CODE:")
    print("  (Simple functions, clear structure)")
    low_result = analyzer.analyze_code(LOW_COMPLEXITY_CODE)
    print(f"  Avg Complexity: {low_result.complexity.avg_complexity:.1f}")
    print(f"  Max Complexity: {low_result.complexity.max_complexity}")
    print(f"  Power Score: {low_result.power:.2f} ✅\n")

    print("📊 IMPROVEMENT:")
    print(f"  Complexity: {high_result.complexity.avg_complexity:.1f} → {low_result.complexity.avg_complexity:.1f}")
    print(f"  Power: {high_result.power:.2f} → {low_result.power:.2f}")


def test_coupling():
    """Test coupling analysis."""
    print("\n\n╔" + "=" * 78 + "╗")
    print("║" + "TEST 2: COUPLING ANALYSIS".center(78) + "║")
    print("╚" + "=" * 78 + "╝\n")

    analyzer = EnhancedLJPWAnalyzer(quiet=True)

    print("🔴 HIGH COUPLING CODE:")
    print("  (Many external dependencies)")
    high_result = analyzer.analyze_code(HIGH_COUPLING_CODE)
    print(f"  Total Imports: {high_result.coupling.total_imports}")
    print(f"  External Deps: {len(high_result.coupling.external_dependencies)}")
    print(f"  Coupling Score: {high_result.coupling.coupling_score:.2f} ❌")
    print(f"  Wisdom Score: {high_result.wisdom:.2f} ❌\n")

    print("🟢 LOW COUPLING CODE:")
    print("  (Dependency injection, minimal imports)")
    low_result = analyzer.analyze_code(LOW_COUPLING_CODE)
    print(f"  Total Imports: {low_result.coupling.total_imports}")
    print(f"  External Deps: {len(low_result.coupling.external_dependencies)}")
    print(f"  Coupling Score: {low_result.coupling.coupling_score:.2f} ✅")
    print(f"  Wisdom Score: {low_result.wisdom:.2f} ✅\n")

    print("📊 IMPROVEMENT:")
    print(f"  Coupling: {high_result.coupling.coupling_score:.2f} → {low_result.coupling.coupling_score:.2f}")
    print(f"  Wisdom: {high_result.wisdom:.2f} → {low_result.wisdom:.2f}")


def test_cohesion():
    """Test cohesion analysis."""
    print("\n\n╔" + "=" * 78 + "╗")
    print("║" + "TEST 3: COHESION ANALYSIS (LCOM)".center(78) + "║")
    print("╚" + "=" * 78 + "╝\n")

    analyzer = EnhancedLJPWAnalyzer(quiet=True)

    print("🔴 LOW COHESION CODE:")
    print("  (Unrelated methods, multiple responsibilities)")
    low_result = analyzer.analyze_code(LOW_COHESION_CODE)
    print(f"  Avg Cohesion: {low_result.cohesion.avg_cohesion:.2f}")
    print(f"  LCOM Score: {low_result.cohesion.lcom_score:.2f} ❌")
    print(f"  Wisdom Score: {low_result.wisdom:.2f} ❌\n")

    print("🟢 HIGH COHESION CODE:")
    print("  (All methods use shared state)")
    high_result = analyzer.analyze_code(HIGH_COHESION_CODE)
    print(f"  Avg Cohesion: {high_result.cohesion.avg_cohesion:.2f}")
    print(f"  LCOM Score: {high_result.cohesion.lcom_score:.2f} ✅")
    print(f"  Wisdom Score: {high_result.wisdom:.2f} ✅\n")

    print("📊 IMPROVEMENT:")
    print(f"  Cohesion: {low_result.cohesion.avg_cohesion:.2f} → {high_result.cohesion.avg_cohesion:.2f}")
    print(f"  Wisdom: {low_result.wisdom:.2f} → {high_result.wisdom:.2f}")


def test_full_comparison():
    """Full comparison of bad vs good code."""
    print("\n\n╔" + "=" * 78 + "╗")
    print("║" + "TEST 4: FULL ENHANCED ANALYSIS".center(78) + "║")
    print("╚" + "=" * 78 + "╝\n")

    analyzer = EnhancedLJPWAnalyzer(quiet=True)

    print("=" * 80)
    print("BAD CODE: High complexity + coupling, low cohesion")
    print("=" * 80)
    bad_result = analyzer.analyze_code(HIGH_COMPLEXITY_CODE + HIGH_COUPLING_CODE + LOW_COHESION_CODE)
    analyzer.print_detailed_report(bad_result, HIGH_COMPLEXITY_CODE + HIGH_COUPLING_CODE + LOW_COHESION_CODE)

    print("\n\n" + "=" * 80)
    print("GOOD CODE: Low complexity + coupling, high cohesion")
    print("=" * 80)
    good_result = analyzer.analyze_code(LOW_COMPLEXITY_CODE + LOW_COUPLING_CODE + HIGH_COHESION_CODE)
    analyzer.print_detailed_report(good_result, LOW_COMPLEXITY_CODE + LOW_COUPLING_CODE + HIGH_COHESION_CODE)

    print("\n\n" + "=" * 80)
    print("COMPARISON SUMMARY")
    print("=" * 80)

    print(f"\n  {'Metric':<30} {'Bad':>10} {'Good':>10} {'Delta':>10}")
    print("-" * 80)

    metrics = [
        ("Harmony", bad_result.harmony, good_result.harmony),
        ("Complexity (avg)", bad_result.complexity.avg_complexity, good_result.complexity.avg_complexity),
        ("Coupling", bad_result.coupling.coupling_score, good_result.coupling.coupling_score),
        ("Cohesion", bad_result.cohesion.avg_cohesion, good_result.cohesion.avg_cohesion),
        ("Power", bad_result.power, good_result.power),
        ("Wisdom", bad_result.wisdom, good_result.wisdom),
    ]

    for name, bad_val, good_val in metrics:
        if name == "Complexity (avg)":
            # Lower is better for complexity
            delta = bad_val - good_val
            delta_str = f"-{delta:.1f}"
        else:
            # Higher is better for others
            delta = good_val - bad_val
            delta_str = f"+{delta:.2f}"

        print(f"  {name:<30} {bad_val:>10.2f} {good_val:>10.2f} {delta_str:>10}")

    print("\n✨ Enhanced metrics show clear quality improvements!")


if __name__ == "__main__":
    test_complexity()
    test_coupling()
    test_cohesion()
    test_full_comparison()
