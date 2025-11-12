#!/usr/bin/env python3
"""
Module Name: generate_module_header.py
Description: Utility script to generate standardized Python module headers

This script helps developers create consistent module headers following the
GacetaChat project standards. It can generate headers for different module
types and validate existing headers.

Key Features:
- Template generation for different module types
- Interactive prompts for module information
- Header validation for existing files
- Batch processing for multiple files

Usage Example:
    ```python
    # Generate header interactively
    python scripts/generate_module_header.py --interactive

    # Generate header for specific module type
    python scripts/generate_module_header.py --type=model --name=user_model.py

    # Validate existing headers
    python scripts/generate_module_header.py --validate src/
    ```

Dependencies:
    - argparse: Command-line argument parsing
    - pathlib: Path handling
    - datetime: Date and time operations

Author: GacetaChat Development Team
Created: 2024-07-18
Last Modified: 2024-07-18
Version: 1.0.0

License: MIT License
Copyright (c) 2024-2025 GacetaChat Team

Notes:
    - Run from project root directory
    - Follows PEP 8 and project coding standards
    - Templates are based on established project patterns

See Also:
    - docs/development/python-module-header-standards.md: Header standards documentation
    - scripts/validate_headers.py: Header validation utility
"""

# Standard library imports
import argparse
from datetime import datetime
from pathlib import Path
from typing import List

# Module metadata
__version__ = "1.0.0"
__author__ = "GacetaChat Development Team"
__status__ = "Development"

# Module constants
HEADER_TEMPLATES = {
    "main": """#!/usr/bin/env python3
\"\"\"
Module Name: {module_name}
Description: {description}

{detailed_description}

Key Features:
{features}

Usage Example:
    ```python
    {usage_example}
    ```

Dependencies:
{dependencies}

Author: GacetaChat Development Team
Created: {created_date}
Last Modified: {modified_date}
Version: {version}

License: MIT License
Copyright (c) 2024-2025 GacetaChat Team

Notes:
{notes}

See Also:
{see_also}
\"\"\"

# Standard library imports
{std_imports}

# Third-party imports
{third_party_imports}

# Local application imports
{local_imports}

# Module metadata
__version__ = "{version}"
__author__ = "GacetaChat Development Team"
__status__ = "{status}"

{constants}
""",
    "model": """\"\"\"
Module Name: {module_name}
Description: {description}

{detailed_description}

Key Features:
{features}

Usage Example:
    ```python
    {usage_example}
    ```

Dependencies:
{dependencies}

Author: GacetaChat Development Team
Created: {created_date}
Last Modified: {modified_date}
Version: {version}

License: MIT License
Copyright (c) 2024-2025 GacetaChat Team

Notes:
{notes}

See Also:
{see_also}
\"\"\"

# Standard library imports
from datetime import datetime
from enum import Enum
from typing import Optional

# Third-party imports
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Local application imports
from db import Base

# Module metadata
__version__ = "{version}"
__author__ = "GacetaChat Development Team"
__status__ = "{status}"
""",
    "test": """#!/usr/bin/env python3
\"\"\"
Module Name: {module_name}
Description: {description}

{detailed_description}

Key Features:
{features}

Usage Example:
    ```python
    {usage_example}
    ```

Dependencies:
{dependencies}

Author: GacetaChat Development Team
Created: {created_date}
Last Modified: {modified_date}
Version: {version}

License: MIT License
Copyright (c) 2024-2025 GacetaChat Team

Notes:
{notes}

See Also:
{see_also}
\"\"\"

# Standard library imports
from unittest.mock import MagicMock, patch

# Third-party imports
import pytest
from sqlalchemy.orm import Session

# Local application imports
{local_imports}

# Module metadata
__version__ = "{version}"
__author__ = "GacetaChat Development Team"
__status__ = "Development"
""",
    "util": """\"\"\"
Module Name: {module_name}
Description: {description}

{detailed_description}

Key Features:
{features}

Usage Example:
    ```python
    {usage_example}
    ```

Dependencies:
{dependencies}

Author: GacetaChat Development Team
Created: {created_date}
Last Modified: {modified_date}
Version: {version}

License: MIT License
Copyright (c) 2024-2025 GacetaChat Team

Notes:
{notes}

See Also:
{see_also}
\"\"\"

# Standard library imports
{std_imports}

# Third-party imports
{third_party_imports}

# Local application imports
{local_imports}

# Module metadata
__version__ = "{version}"
__author__ = "GacetaChat Development Team"
__status__ = "{status}"

# Logging setup
import logging
logger = logging.getLogger(__name__)

{constants}
""",
}


def get_module_type(file_path: str) -> str:
    """Determine module type based on file path and name."""
    path = Path(file_path)

    if path.name.startswith("test_"):
        return "test"
    elif "test" in path.parts:
        return "test"
    elif path.name in ["models.py", "model.py"]:
        return "model"
    elif path.name in ["fastapp.py", "streamlit_app.py", "download_gaceta.py"]:
        return "main"
    elif "util" in path.name or "helper" in path.name:
        return "util"
    else:
        return "util"


def generate_header(module_name: str, module_type: str, **kwargs) -> str:
    """Generate a standardized module header."""
    template = HEADER_TEMPLATES.get(module_type, HEADER_TEMPLATES["util"])

    # Default values
    defaults = {
        "module_name": module_name,
        "description": kwargs.get("description", "Brief description of the module"),
        "detailed_description": kwargs.get(
            "detailed_description",
            "This module provides functionality for the GacetaChat application.",
        ),
        "features": kwargs.get("features", "- Feature 1\n- Feature 2\n- Feature 3"),
        "usage_example": kwargs.get(
            "usage_example",
            f'from {module_name.replace(".py", "")} import main_function\nresult = main_function()',
        ),
        "dependencies": kwargs.get(
            "dependencies", "- dependency1: Purpose of dependency"
        ),
        "created_date": datetime.now().strftime("%Y-%m-%d"),
        "modified_date": datetime.now().strftime("%Y-%m-%d"),
        "version": kwargs.get("version", "1.0.0"),
        "status": kwargs.get("status", "Development"),
        "notes": kwargs.get("notes", "- Important note about the module"),
        "see_also": kwargs.get(
            "see_also", "- related_module.py: Description of relationship"
        ),
        "std_imports": kwargs.get(
            "std_imports", "import os\nimport sys\nfrom datetime import datetime"
        ),
        "third_party_imports": kwargs.get(
            "third_party_imports", "# Add third-party imports here"
        ),
        "local_imports": kwargs.get("local_imports", "from config import config"),
        "constants": kwargs.get(
            "constants", '# Module-level constants\nDEFAULT_VALUE = "default"'
        ),
    }

    return template.format(**defaults)


def interactive_generation():
    """Interactive header generation with user prompts."""
    print("=== GacetaChat Module Header Generator ===")

    module_name = input("Module name (e.g., user_model.py): ")
    module_type = input("Module type (main/model/test/util): ") or get_module_type(
        module_name
    )
    description = input("Brief description: ")

    print("\\nEnter detailed description (press Enter twice when done):")
    detailed_lines = []
    while True:
        line = input()
        if line == "" and detailed_lines and detailed_lines[-1] == "":
            break
        detailed_lines.append(line)
    detailed_description = "\\n".join(detailed_lines[:-1])  # Remove last empty line

    features = input("\\nKey features (comma-separated): ")
    if features:
        features = "\\n".join(f"- {f.strip()}" for f in features.split(","))

    dependencies = input("\\nMain dependencies (comma-separated): ")
    if dependencies:
        deps_list = []
        for dep in dependencies.split(","):
            dep = dep.strip()
            purpose = input(f"Purpose of {dep}: ")
            deps_list.append(f"- {dep}: {purpose}")
        dependencies = "\\n".join(deps_list)

    version = input("\\nVersion (default 1.0.0): ") or "1.0.0"

    header = generate_header(
        module_name=module_name,
        module_type=module_type,
        description=description,
        detailed_description=detailed_description,
        features=features,
        dependencies=dependencies,
        version=version,
    )

    print("\\n=== Generated Header ===")
    print(header)

    save_path = input("\\nSave to file (press Enter to skip): ")
    if save_path:
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(header)
        print(f"Header saved to {save_path}")


def validate_header(file_path: str) -> List[str]:
    """Validate that a file has a proper header."""
    issues = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return [f"Could not read file: {e}"]

    lines = content.split("\\n")

    # Check for docstring
    if not ('"""' in content[:500] or "'''" in content[:500]):
        issues.append("Missing module docstring")

    # Check for required sections in docstring
    required_sections = ["Module Name:", "Description:", "Author:", "Version:"]
    for section in required_sections:
        if section not in content[:1000]:
            issues.append(f"Missing required section: {section}")

    # Check for proper import organization
    import_started = False
    std_imports = []
    third_party_imports = []
    local_imports = []

    for i, line in enumerate(lines[:50]):  # Check first 50 lines
        if line.startswith("import ") or line.startswith("from "):
            import_started = True
            if line.startswith("from ") and (
                "." in line.split()[1]
                or line.split()[1] in ["config", "models", "crud"]
            ):
                local_imports.append(i)
            elif any(
                pkg in line
                for pkg in ["pandas", "numpy", "requests", "fastapi", "streamlit"]
            ):
                third_party_imports.append(i)
            else:
                std_imports.append(i)

    # Check import order
    if import_started:
        all_imports = std_imports + third_party_imports + local_imports
        if all_imports != sorted(all_imports):
            issues.append(
                "Imports not organized properly (should be: standard, third-party, local)"
            )

    return issues


def main():
    """Main function to handle command-line arguments and execution."""
    parser = argparse.ArgumentParser(
        description="Generate standardized Python module headers"
    )
    parser.add_argument(
        "--interactive", "-i", action="store_true", help="Interactive mode"
    )
    parser.add_argument(
        "--type", "-t", choices=["main", "model", "test", "util"], help="Module type"
    )
    parser.add_argument("--name", "-n", help="Module name")
    parser.add_argument("--validate", "-v", help="Validate headers in directory")
    parser.add_argument("--output", "-o", help="Output file path")

    args = parser.parse_args()

    if args.interactive:
        interactive_generation()
    elif args.validate:
        validate_path = Path(args.validate)
        if validate_path.is_file():
            files = [validate_path]
        else:
            files = list(validate_path.rglob("*.py"))

        print(f"Validating {len(files)} Python files...")
        total_issues = 0

        for file_path in files:
            issues = validate_header(str(file_path))
            if issues:
                print(f"\\n{file_path}:")
                for issue in issues:
                    print(f"  - {issue}")
                total_issues += len(issues)

        if total_issues == 0:
            print("\\n✅ All files have valid headers!")
        else:
            print(
                f"\\n❌ Found {total_issues} issues across {len([f for f in files if validate_header(str(f))])} files"
            )

    elif args.name:
        module_type = args.type or get_module_type(args.name)
        header = generate_header(args.name, module_type)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(header)
            print(f"Header generated and saved to {args.output}")
        else:
            print(header)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
