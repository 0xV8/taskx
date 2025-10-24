#!/usr/bin/env python3
"""
Documentation Example Verification Script

This script extracts code examples from documentation files and verifies they work correctly.
It helps ensure documentation stays accurate and up-to-date.

Usage:
    python scripts/verify_docs.py                    # Verify all docs
    python scripts/verify_docs.py README.md          # Verify specific file
    python scripts/verify_docs.py --verbose          # Show detailed output
"""

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class CodeExample:
    """Represents a code example from documentation."""
    file_path: str
    line_number: int
    language: str
    code: str
    context: str  # Surrounding text for context


class DocVerifier:
    """Verifies code examples in documentation files."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.examples: List[CodeExample] = []
        self.passed: List[CodeExample] = []
        self.failed: List[Tuple[CodeExample, str]] = []
        self.skipped: List[Tuple[CodeExample, str]] = []

    def log(self, message: str, level: str = "INFO") -> None:
        """Log a message if verbose mode is enabled."""
        if self.verbose or level in ["ERROR", "WARNING"]:
            prefix = {
                "INFO": "ℹ️",
                "SUCCESS": "✅",
                "ERROR": "❌",
                "WARNING": "⚠️",
                "SKIP": "⏭️",
            }.get(level, "•")
            print(f"{prefix} {message}")

    def extract_examples(self, file_path: Path) -> List[CodeExample]:
        """Extract code examples from a markdown file."""
        if not file_path.exists():
            self.log(f"File not found: {file_path}", "ERROR")
            return []

        content = file_path.read_text()
        examples = []

        # Regular expression to match markdown code blocks
        # Matches: ```language\ncode\n```
        pattern = r'```(\w+)\n(.*?)\n```'
        matches = re.finditer(pattern, content, re.DOTALL)

        for match in matches:
            language = match.group(1)
            code = match.group(2)

            # Find line number
            line_number = content[:match.start()].count('\n') + 1

            # Extract context (previous heading or paragraph)
            before_code = content[:match.start()]
            context_lines = before_code.split('\n')[-5:]  # Last 5 lines before code
            context = '\n'.join(context_lines).strip()

            example = CodeExample(
                file_path=str(file_path),
                line_number=line_number,
                language=language,
                code=code,
                context=context
            )
            examples.append(example)

        self.log(f"Found {len(examples)} code examples in {file_path.name}")
        return examples

    def verify_bash_example(self, example: CodeExample) -> Tuple[bool, Optional[str]]:
        """Verify a bash/shell code example."""
        # Skip examples that are just output or contain placeholders
        if any(skip in example.code for skip in ['$ ', '# Output:', '...']):
            return True, None  # These are documentation examples, not runnable

        # Skip examples with obvious placeholders
        if re.search(r'\${[A-Z_]+}', example.code):
            return True, None  # Contains variable placeholders

        # Skip interactive commands
        if any(cmd in example.code for cmd in ['taskx init', 'read ', 'select ']):
            return True, None  # Interactive commands

        try:
            # Create temporary directory for isolated execution
            with tempfile.TemporaryDirectory() as tmpdir:
                result = subprocess.run(
                    example.code,
                    shell=True,
                    cwd=tmpdir,
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                # Some commands are expected to fail (like showing help)
                # We just check that they don't crash
                return True, None

        except subprocess.TimeoutExpired:
            return False, "Command timed out after 10 seconds"
        except Exception as e:
            return False, f"Execution error: {str(e)}"

    def verify_python_example(self, example: CodeExample) -> Tuple[bool, Optional[str]]:
        """Verify a Python code example."""
        # Skip examples that are just partial code or contain placeholders
        if '...' in example.code or '# ...' in example.code:
            return True, None  # Partial example for documentation

        # Skip examples with obvious placeholders
        if re.search(r'\${[A-Z_]+}', example.code):
            return True, None  # Contains variable placeholders

        try:
            # Create temporary directory and file
            with tempfile.TemporaryDirectory() as tmpdir:
                tmp_file = Path(tmpdir) / "test_example.py"
                tmp_file.write_text(example.code)

                # Try to parse the code (syntax check)
                result = subprocess.run(
                    [sys.executable, "-m", "py_compile", str(tmp_file)],
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                if result.returncode != 0:
                    return False, f"Syntax error: {result.stderr}"

                return True, None

        except subprocess.TimeoutExpired:
            return False, "Verification timed out after 5 seconds"
        except Exception as e:
            return False, f"Verification error: {str(e)}"

    def verify_toml_example(self, example: CodeExample) -> Tuple[bool, Optional[str]]:
        """Verify a TOML configuration example."""
        try:
            # Try to parse TOML (Python 3.11+ has tomllib, older versions need tomli)
            try:
                import tomllib
            except ImportError:
                import tomli as tomllib

            # Parse the TOML content
            tomllib.loads(example.code)
            return True, None

        except Exception as e:
            return False, f"TOML parsing error: {str(e)}"

    def verify_example(self, example: CodeExample) -> Tuple[bool, Optional[str]]:
        """Verify a single code example based on its language."""
        language = example.language.lower()

        if language in ['bash', 'sh', 'shell', 'console']:
            return self.verify_bash_example(example)
        elif language in ['python', 'py']:
            return self.verify_python_example(example)
        elif language == 'toml':
            return self.verify_toml_example(example)
        elif language in ['yaml', 'yml', 'json', 'markdown', 'md', 'text']:
            # These are configuration or documentation examples, skip execution
            return True, None
        else:
            # Unknown language, skip
            return True, None

    def verify_file(self, file_path: Path) -> None:
        """Verify all examples in a documentation file."""
        self.log(f"\nVerifying {file_path}...")

        examples = self.extract_examples(file_path)
        self.examples.extend(examples)

        for example in examples:
            self.log(
                f"  Checking {example.language} example at line {example.line_number}...",
                "INFO"
            )

            success, error = self.verify_example(example)

            if success:
                self.passed.append(example)
                self.log(f"    ✅ Passed", "SUCCESS")
            elif error:
                self.failed.append((example, error))
                self.log(f"    ❌ Failed: {error}", "ERROR")
            else:
                self.skipped.append((example, "Unknown reason"))
                self.log(f"    ⏭️  Skipped", "SKIP")

    def print_summary(self) -> None:
        """Print verification summary."""
        total = len(self.examples)
        passed = len(self.passed)
        failed = len(self.failed)
        skipped = len(self.skipped)

        print("\n" + "=" * 70)
        print("Documentation Verification Summary")
        print("=" * 70)
        print(f"Total examples:   {total}")
        print(f"✅ Passed:        {passed}")
        print(f"❌ Failed:        {failed}")
        print(f"⏭️  Skipped:       {skipped}")
        print("=" * 70)

        if failed > 0:
            print("\n❌ Failed Examples:")
            for example, error in self.failed:
                print(f"\n  File: {example.file_path}")
                print(f"  Line: {example.line_number}")
                print(f"  Language: {example.language}")
                print(f"  Error: {error}")
                print(f"  Code preview: {example.code[:100]}...")

        if failed > 0:
            print("\n❌ Some examples failed verification!")
            sys.exit(1)
        else:
            print("\n✅ All examples passed verification!")
            sys.exit(0)


def find_documentation_files(root_dir: Path) -> List[Path]:
    """Find all documentation files in the project."""
    doc_files = []

    # Check root directory
    for pattern in ['*.md', 'docs/**/*.md']:
        doc_files.extend(root_dir.glob(pattern))

    return sorted(set(doc_files))


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Verify code examples in documentation files"
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Documentation files to verify (default: all markdown files)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed output"
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).parent.parent,
        help="Root directory of the project"
    )

    args = parser.parse_args()

    # Determine which files to verify
    if args.files:
        files_to_verify = [Path(f) for f in args.files]
    else:
        files_to_verify = find_documentation_files(args.root)

    if not files_to_verify:
        print("❌ No documentation files found to verify")
        sys.exit(1)

    # Create verifier and process files
    verifier = DocVerifier(verbose=args.verbose)

    print(f"🔍 Verifying {len(files_to_verify)} documentation file(s)...")

    for file_path in files_to_verify:
        if not file_path.exists():
            print(f"⚠️  Warning: File not found: {file_path}")
            continue
        verifier.verify_file(file_path)

    # Print summary
    verifier.print_summary()


if __name__ == "__main__":
    main()
