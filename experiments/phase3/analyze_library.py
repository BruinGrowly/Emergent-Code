#!/usr/bin/env python3
"""
LJPW Library Analyzer - Phase 3 Real-World Validation

Analyzes production Python libraries from GitHub to validate LJPW framework
on code that developers trust and love.

Usage:
    python analyze_library.py --repo https://github.com/psf/requests
    python analyze_library.py --repo requests --local /path/to/local/clone
    python analyze_library.py --repo flask --sample 20 --detailed

Features:
- Clones repository (or uses local clone)
- Analyzes all Python files with enhanced LJPW analyzer
- Generates detailed reports with actionable recommendations
- Exports results in JSON for further analysis
- Creates comparative visualizations
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from collections import defaultdict

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from experiments.phase2.enhanced_ljpw_analyzer import (
    EnhancedLJPWAnalyzer,
    EnhancedLJPWScore
)


@dataclass
class FileAnalysis:
    """Analysis result for a single file."""
    file_path: str
    lines_of_code: int
    harmony: float
    love: float
    justice: float
    power: float
    wisdom: float
    complexity_avg: float
    coupling_score: float
    cohesion_avg: float
    issues: List[str]


@dataclass
class LibraryAnalysis:
    """Complete analysis of a library."""
    library_name: str
    repository_url: str
    total_files: int
    total_lines: int
    overall_harmony: float
    dimension_averages: Dict[str, float]
    complexity_stats: Dict[str, float]
    coupling_stats: Dict[str, float]
    cohesion_stats: Dict[str, float]
    file_analyses: List[FileAnalysis]
    top_files: List[FileAnalysis]  # Highest harmony
    bottom_files: List[FileAnalysis]  # Lowest harmony
    recommendations: List[str]


class LibraryAnalyzer:
    """Analyzes Python libraries with LJPW framework."""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.analyzer = EnhancedLJPWAnalyzer()

    def log(self, message: str):
        # Auto-healed: Input validation for log
        if message is not None and not isinstance(message, str):
            raise TypeError(f'message must be str, got {type(message).__name__}')
        """Print message if verbose."""
        if self.verbose:
            print(message)

    def clone_repository(self, repo_url: str, target_dir: str) -> bool:
        # Auto-healed: Input validation for clone_repository
        if repo_url is not None and not isinstance(repo_url, str):
            raise TypeError(f'repo_url must be str, got {type(repo_url).__name__}')
        if target_dir is not None and not isinstance(target_dir, str):
            raise TypeError(f'target_dir must be str, got {type(target_dir).__name__}')
        """Clone a repository from GitHub."""
        self.log(f"📥 Cloning {repo_url}...")

        try:
            subprocess.run(
                ["git", "clone", "--depth", "1", repo_url, target_dir],
                check=True,
                capture_output=True,
                text=True
            )
            self.log(f"✅ Cloned to {target_dir}")
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"❌ Clone failed: {e.stderr}")
            return False

    def find_python_files(self, directory: str, exclude_tests: bool = False) -> List[Path]:
        # Auto-healed: Input validation for find_python_files
        if directory is not None and not isinstance(directory, str):
            raise TypeError(f'directory must be str, got {type(directory).__name__}')
        """Find all Python files in directory."""
        self.log(f"🔍 Finding Python files in {directory}...")

        python_files = []
        for path in Path(directory).rglob("*.py"):
            # Skip common non-package directories
            if any(part in path.parts for part in ['.git', '.tox', '.eggs', 'build', 'dist', '__pycache__']):
                continue

            # Skip tests if requested
            if exclude_tests and any(part in path.parts for part in ['test', 'tests']):
                continue

            python_files.append(path)

        self.log(f"📄 Found {len(python_files)} Python files")
        return python_files

    def analyze_file(self, file_path: Path) -> Optional[FileAnalysis]:
        """Analyze a single Python file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()

            # Skip empty files
            if not code.strip():
                return None

            # Count lines of code (non-empty, non-comment)
            lines = [line.strip() for line in code.split('\n')]
            loc = len([line for line in lines if line and not line.startswith('#')])

            # Analyze with enhanced analyzer
            result = self.analyzer.analyze_code(code)

            # Identify issues
            issues = []
            if result.justice < 0.3:
                issues.append("Low Justice: Add error handling and validation")
            if result.love < 0.3:
                issues.append("Low Love: Add docstrings and logging")
            if result.complexity.avg_complexity > 10:
                issues.append(f"High Complexity: Average {result.complexity.avg_complexity:.1f}")
            if result.coupling.coupling_score > 0.7:
                issues.append(f"High Coupling: {result.coupling.total_imports} imports")
            if result.cohesion.lcom_score > 0.7:
                issues.append("Low Cohesion: Consider splitting classes")

            return FileAnalysis(
                file_path=str(file_path),
                lines_of_code=loc,
                harmony=result.harmony,
                love=result.love,
                justice=result.justice,
                power=result.power,
                wisdom=result.wisdom,
                complexity_avg=result.complexity.avg_complexity,
                coupling_score=result.coupling.coupling_score,
                cohesion_avg=result.cohesion.lcom_score,
                issues=issues
            )

        except Exception as e:
            self.log(f"⚠️  Error analyzing {file_path}: {e}")
            return None

    def analyze_library(
        self,
        directory: str,
        library_name: str,
        repo_url: str,
        sample_size: Optional[int] = None,
        exclude_tests: bool = False
    ) -> LibraryAnalysis:
        """Analyze entire library."""
        self.log(f"\n{'='*80}")
        self.log(f"📊 ANALYZING LIBRARY: {library_name}")
        self.log(f"{'='*80}\n")

        # Find all Python files
        python_files = self.find_python_files(directory, exclude_tests)

        # Sample if requested
        if sample_size and len(python_files) > sample_size:
            self.log(f"📊 Sampling {sample_size} files from {len(python_files)} total")
            import random
            python_files = random.sample(python_files, sample_size)

        # Analyze all files
        file_analyses = []
        total_lines = 0

        for i, file_path in enumerate(python_files, 1):
            if self.verbose and i % 10 == 0:
                print(f"  Progress: {i}/{len(python_files)} files analyzed...", end='\r')

            analysis = self.analyze_file(file_path)
            if analysis:
                file_analyses.append(analysis)
                total_lines += analysis.lines_of_code

        if self.verbose:
            print()  # New line after progress

        self.log(f"✅ Analyzed {len(file_analyses)} files ({total_lines:,} lines)")

        # Calculate statistics
        if not file_analyses:
            raise ValueError("No files could be analyzed")

        overall_harmony = sum(f.harmony for f in file_analyses) / len(file_analyses)

        dimension_averages = {
            'Love': sum(f.love for f in file_analyses) / len(file_analyses),
            'Justice': sum(f.justice for f in file_analyses) / len(file_analyses),
            'Power': sum(f.power for f in file_analyses) / len(file_analyses),
            'Wisdom': sum(f.wisdom for f in file_analyses) / len(file_analyses),
        }

        complexity_stats = {
            'average': sum(f.complexity_avg for f in file_analyses) / len(file_analyses),
            'max': max(f.complexity_avg for f in file_analyses),
            'min': min(f.complexity_avg for f in file_analyses),
        }

        coupling_stats = {
            'average': sum(f.coupling_score for f in file_analyses) / len(file_analyses),
            'max': max(f.coupling_score for f in file_analyses),
            'min': min(f.coupling_score for f in file_analyses),
        }

        cohesion_stats = {
            'average': sum(f.cohesion_avg for f in file_analyses) / len(file_analyses),
            'max': max(f.cohesion_avg for f in file_analyses),
            'min': min(f.cohesion_avg for f in file_analyses),
        }

        # Find top and bottom files
        sorted_by_harmony = sorted(file_analyses, key=lambda f: f.harmony, reverse=True)
        top_files = sorted_by_harmony[:5]
        bottom_files = sorted_by_harmony[-5:]

        # Generate recommendations
        recommendations = self._generate_recommendations(
            dimension_averages, complexity_stats, coupling_stats, cohesion_stats, file_analyses
        )

        return LibraryAnalysis(
            library_name=library_name,
            repository_url=repo_url,
            total_files=len(file_analyses),
            total_lines=total_lines,
            overall_harmony=overall_harmony,
            dimension_averages=dimension_averages,
            complexity_stats=complexity_stats,
            coupling_stats=coupling_stats,
            cohesion_stats=cohesion_stats,
            file_analyses=file_analyses,
            top_files=top_files,
            bottom_files=bottom_files,
            recommendations=recommendations
        )

    def _generate_recommendations(
        self,
        dimensions: Dict[str, float],
        complexity: Dict[str, float],
        coupling: Dict[str, float],
        cohesion: Dict[str, float],
        file_analyses: List[FileAnalysis]
    ) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []

        # Find weakest dimension
        weakest_dim = min(dimensions.items(), key=lambda x: x[1])

        if weakest_dim[1] < 0.4:
            if weakest_dim[0] == 'Justice':
                recommendations.append(
                    "🎯 PRIORITY: Add error handling - Justice is critically low. "
                    "Add try/except blocks to all external calls (network, file I/O, parsing)."
                )
            elif weakest_dim[0] == 'Love':
                recommendations.append(
                    "🎯 PRIORITY: Improve observability - Love is critically low. "
                    "Add docstrings to public APIs and logging to critical paths."
                )
            elif weakest_dim[0] == 'Wisdom':
                recommendations.append(
                    "🎯 PRIORITY: Improve architecture - Wisdom is critically low. "
                    "Consider refactoring for better separation of concerns."
                )

        # Complexity recommendations
        if complexity['average'] > 10:
            high_complexity_files = [f for f in file_analyses if f.complexity_avg > 10]
            recommendations.append(
                f"⚠️  High Complexity: {len(high_complexity_files)} files have complexity > 10. "
                f"Consider extracting helper functions to reduce branching."
            )

        # Coupling recommendations
        if coupling['average'] > 0.6:
            high_coupling_files = [f for f in file_analyses if f.coupling_score > 0.6]
            recommendations.append(
                f"⚠️  High Coupling: {len(high_coupling_files)} files are highly coupled. "
                f"Consider dependency injection and interface abstraction."
            )

        # Cohesion recommendations
        if cohesion['average'] > 0.6:
            low_cohesion_files = [f for f in file_analyses if f.cohesion_avg > 0.6]
            recommendations.append(
                f"⚠️  Low Cohesion: {len(low_cohesion_files)} files have low cohesion. "
                f"Consider splitting classes with unrelated methods."
            )

        # Positive findings
        if all(score > 0.5 for score in dimensions.values()):
            recommendations.append("✅ Strong Balance: All dimensions above 0.5 - well-rounded codebase!")

        if complexity['average'] < 5:
            recommendations.append("✅ Low Complexity: Average complexity under 5 - maintainable code!")

        return recommendations or ["✅ No critical issues detected!"]

    def print_report(self, analysis: LibraryAnalysis):
        """Print human-readable analysis report."""
        print(f"\n{'='*80}")
        print(f"📊 LJPW ANALYSIS REPORT: {analysis.library_name}")
        print(f"{'='*80}\n")

        print(f"📦 Repository: {analysis.repository_url}")
        print(f"📄 Files Analyzed: {analysis.total_files:,}")
        print(f"📝 Total Lines: {analysis.total_lines:,}")
        print()

        # Overall Harmony
        harmony_status = (
            "✅ AUTOPOIETIC" if analysis.overall_harmony >= 0.6
            else "⚠️  EMERGENT" if analysis.overall_harmony >= 0.4
            else "❌ ENTROPIC"
        )
        print(f"🌟 Overall Harmony: {analysis.overall_harmony:.3f} {harmony_status}")
        print()

        # Dimensions
        print("📊 DIMENSION SCORES:")
        print("-" * 80)
        for dim, score in analysis.dimension_averages.items():
            bar = '█' * int(score * 40)
            status = "✅" if score >= 0.5 else "⚠️ " if score >= 0.3 else "❌"
            print(f"  {status} {dim:8s}: {score:.3f} {bar}")
        print()

        # Complexity
        print("🔢 COMPLEXITY METRICS:")
        print("-" * 80)
        print(f"  Average: {analysis.complexity_stats['average']:.2f}")
        print(f"  Maximum: {analysis.complexity_stats['max']:.2f}")
        print(f"  Status: ", end="")
        if analysis.complexity_stats['average'] < 5:
            print("✅ Low (maintainable)")
        elif analysis.complexity_stats['average'] < 10:
            print("⚠️  Medium (acceptable)")
        else:
            print("❌ High (needs refactoring)")
        print()

        # Coupling
        print("🔗 COUPLING METRICS:")
        print("-" * 80)
        print(f"  Average: {analysis.coupling_stats['average']:.3f}")
        print(f"  Status: ", end="")
        if analysis.coupling_stats['average'] < 0.3:
            print("✅ Low (loosely coupled)")
        elif analysis.coupling_stats['average'] < 0.6:
            print("⚠️  Medium (acceptable)")
        else:
            print("❌ High (tightly coupled)")
        print()

        # Cohesion
        print("🎯 COHESION METRICS:")
        print("-" * 80)
        print(f"  Average LCOM: {analysis.cohesion_stats['average']:.3f}")
        print(f"  Status: ", end="")
        if analysis.cohesion_stats['average'] < 0.3:
            print("✅ High cohesion (focused classes)")
        elif analysis.cohesion_stats['average'] < 0.6:
            print("⚠️  Medium cohesion (acceptable)")
        else:
            print("❌ Low cohesion (unfocused classes)")
        print()

        # Top Files
        print("🏆 TOP 5 FILES (Highest Harmony):")
        print("-" * 80)
        for i, file in enumerate(analysis.top_files, 1):
            rel_path = Path(file.file_path).name
            print(f"  {i}. {rel_path}")
            print(f"     H={file.harmony:.3f} | L={file.love:.2f} J={file.justice:.2f} P={file.power:.2f} W={file.wisdom:.2f}")
        print()

        # Bottom Files
        print("⚠️  BOTTOM 5 FILES (Lowest Harmony):")
        print("-" * 80)
        for i, file in enumerate(analysis.bottom_files, 1):
            rel_path = Path(file.file_path).name
            print(f"  {i}. {rel_path}")
            print(f"     H={file.harmony:.3f} | L={file.love:.2f} J={file.justice:.2f} P={file.power:.2f} W={file.wisdom:.2f}")
            if file.issues:
                for issue in file.issues:
                    print(f"       • {issue}")
        print()

        # Recommendations
        print("💡 RECOMMENDATIONS:")
        print("-" * 80)
        for i, rec in enumerate(analysis.recommendations, 1):
            print(f"  {i}. {rec}")
        print()

        print("="*80)

    def export_json(self, analysis: LibraryAnalysis, output_path: str):
        # Auto-healed: Input validation for export_json
        if output_path is not None and not isinstance(output_path, str):
            raise TypeError(f'output_path must be str, got {type(output_path).__name__}')
        """Export analysis to JSON."""
        # Convert to dict (dataclass asdict)
        data = {
            'library_name': analysis.library_name,
            'repository_url': analysis.repository_url,
            'total_files': analysis.total_files,
            'total_lines': analysis.total_lines,
            'overall_harmony': analysis.overall_harmony,
            'dimension_averages': analysis.dimension_averages,
            'complexity_stats': analysis.complexity_stats,
            'coupling_stats': analysis.coupling_stats,
            'cohesion_stats': analysis.cohesion_stats,
            'recommendations': analysis.recommendations,
            'top_files': [asdict(f) for f in analysis.top_files],
            'bottom_files': [asdict(f) for f in analysis.bottom_files],
        }

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)

        self.log(f"💾 Exported to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Python libraries with LJPW framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze from GitHub URL
  python analyze_library.py --repo https://github.com/psf/requests

  # Analyze local clone
  python analyze_library.py --repo requests --local /path/to/requests

  # Sample 50 files for faster analysis
  python analyze_library.py --repo flask --sample 50

  # Exclude test files
  python analyze_library.py --repo django --no-tests

  # Export to JSON
  python analyze_library.py --repo click --output results/click.json
        """
    )

    parser.add_argument('--repo', required=True, help='Repository name or URL')
    parser.add_argument('--local', help='Path to local clone (skip cloning)')
    parser.add_argument('--sample', type=int, help='Sample N files (for large repos)')
    parser.add_argument('--no-tests', action='store_true', help='Exclude test files')
    parser.add_argument('--output', help='Output JSON file path')
    parser.add_argument('--quiet', action='store_true', help='Suppress progress output')

    args = parser.parse_args()

    analyzer = LibraryAnalyzer(verbose=not args.quiet)

    # Determine repository details
    if args.repo.startswith('http'):
        repo_url = args.repo
        library_name = repo_url.rstrip('/').split('/')[-1]
    else:
        library_name = args.repo
        repo_url = f"https://github.com/psf/{library_name}"  # Assume PSF if no URL

    # Get directory to analyze
    if args.local:
        analysis_dir = args.local
    else:
        # Clone to temp directory
        temp_dir = tempfile.mkdtemp(prefix=f"ljpw_{library_name}_")
        if not analyzer.clone_repository(repo_url, temp_dir):
            print("❌ Failed to clone repository")
            sys.exit(1)
        analysis_dir = temp_dir

    # Analyze
    try:
        analysis = analyzer.analyze_library(
            directory=analysis_dir,
            library_name=library_name,
            repo_url=repo_url,
            sample_size=args.sample,
            exclude_tests=args.no_tests
        )

        # Print report
        analyzer.print_report(analysis)

        # Export JSON if requested
        if args.output:
            analyzer.export_json(analysis, args.output)

    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Cleanup temp directory
    if not args.local:
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == '__main__':
    main()
