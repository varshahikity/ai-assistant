import ast
import re


# Keywords used to estimate complexity for Java/C++ code.
LOOP_KEYWORDS = ["for", "while", "do"]
CONDITION_KEYWORDS = ["if", "switch"]


def analyze_code(code, language):
    """
    Analyze user code and return beginner-friendly insights.
    """
    language = (language or "").lower().strip()

    syntax_result = check_syntax(code, language)
    complexity = analyze_complexity(code, language)
    documentation = generate_documentation(code, language, complexity)
    suggestions = generate_improvement_suggestions(
        code, language, syntax_result, complexity)
    test_cases = generate_test_case_suggestions(code, language)

    return {
        "errors": syntax_result,
        "complexity": complexity,
        "documentation": documentation,
        "suggestions": suggestions,
        "test_cases": test_cases,
    }


def check_syntax(code, language):
    """
    Perform a simple syntax check.
    Python uses `ast.parse`.
    Java/C++ use lightweight brace and token checks.
    """
    if language == "python":
        try:
            ast.parse(code)
            return {"has_error": False, "message": "No syntax errors found."}
        except SyntaxError as err:
            return {
                "has_error": True,
                "message": "Syntax error on line {0}: {1}".format(err.lineno, err.msg),
            }

    if language in {"java", "cpp", "c++"}:
        balanced, message = has_balanced_symbols(code)
        if not balanced:
            return {"has_error": True, "message": message}

        # Very simple semicolon check for non-block lines.
        lines = [line.strip() for line in code.splitlines() if line.strip()]
        suspicious_lines = []
        for idx, line in enumerate(lines, start=1):
            if line.startswith("//"):
                continue
            if line.endswith(("{", "}", ";")):
                continue
            if line.startswith(("if", "for", "while", "switch", "else", "do")):
                continue
            suspicious_lines.append(idx)

        if suspicious_lines:
            return {
                "has_error": False,
                "message": "No critical syntax issues found. Some lines may be missing semicolons.",
            }

        return {"has_error": False, "message": "No obvious syntax issues found."}

    return {
        "has_error": True,
        "message": "Unsupported language. Choose Python, Java, or C++.",
    }


def has_balanced_symbols(code):
    """
    Check if brackets and braces are balanced.
    """
    pairs = {")": "(", "]": "[", "}": "{"}
    openers = set(pairs.values())
    stack = []

    for char in code:
        if char in openers:
            stack.append(char)
        elif char in pairs:
            if not stack or stack[-1] != pairs[char]:
                return False, "Unbalanced brackets/braces detected."
            stack.pop()

    if stack:
        return False, "Missing closing brackets/braces detected."

    return True, "Symbols are balanced."


def analyze_complexity(code, language):
    """
    Count lines, loops, functions, and estimate a basic complexity score.
    """
    lines = [line for line in code.splitlines() if line.strip()]
    line_count = len(lines)

    if language == "python":
        loop_count = len(re.findall(r"\b(for|while)\b", code))
        function_count = len(re.findall(r"\bdef\s+\w+\s*\(", code))
        condition_count = len(re.findall(r"\b(if|elif)\b", code))
    else:
        loop_pattern = r"\b(" + "|".join(LOOP_KEYWORDS) + r")\b"
        loop_count = len(re.findall(loop_pattern, code))

        # Works for many beginner-level function signatures in Java/C++.
        function_count = len(
            re.findall(
                r"\b(?:public|private|protected|static|final|virtual|inline|int|void|double|float|char|bool|string)\b[^\n;{}]*\([^\n;{}]*\)\s*\{",
                code,
                flags=re.IGNORECASE,
            )
        )

        condition_pattern = r"\b(" + "|".join(CONDITION_KEYWORDS) + r")\b"
        condition_count = len(re.findall(condition_pattern, code))

    complexity_score = loop_count * 2 + condition_count + function_count

    if complexity_score <= 3:
        rating = "Low"
    elif complexity_score <= 7:
        rating = "Medium"
    else:
        rating = "High"

    return {
        "line_count": line_count,
        "loop_count": loop_count,
        "function_count": function_count,
        "condition_count": condition_count,
        "complexity_score": complexity_score,
        "rating": rating,
    }


def generate_documentation(code, language, complexity):
    """
    Generate a simple explanation for beginners.
    """
    summary_parts = [
        "This {0} code has {1} non-empty lines".format(
            language.title(), complexity["line_count"]),
        "{0} function(s)".format(complexity["function_count"]),
        "{0} loop(s)".format(complexity["loop_count"]),
        "and {0} conditional statement(s).".format(
            complexity["condition_count"]),
    ]

    summary = ", ".join(summary_parts)

    if complexity["rating"] == "Low":
        detail = "The logic is relatively simple and should be easy to maintain."
    elif complexity["rating"] == "Medium":
        detail = "The logic has moderate complexity. Consider breaking large blocks into smaller functions."
    else:
        detail = "The logic is complex. Refactoring into smaller functions can improve readability and testing."

    return "{0}. {1}".format(summary, detail)


def generate_improvement_suggestions(code, language, syntax_result, complexity):
    """
    Create simple and practical improvement suggestions.
    """
    suggestions = []

    if syntax_result.get("has_error"):
        suggestions.append(
            "Fix syntax errors first before making optimizations.")

    if complexity["line_count"] > 80:
        suggestions.append(
            "Consider splitting the code into smaller modules or files.")

    if complexity["function_count"] == 0:
        suggestions.append(
            "Wrap logic into functions to improve reuse and testability.")

    if complexity["rating"] == "High":
        suggestions.append(
            "Reduce nested loops/conditions to lower complexity.")

    if language == "python" and "#" not in code:
        suggestions.append(
            "Add comments for key logic blocks to improve readability.")

    if language in {"java", "cpp", "c++"} and "//" not in code and "/*" not in code:
        suggestions.append("Add comments to explain important sections.")

    if "print(" in code or "System.out.println" in code or "cout <<" in code:
        suggestions.append(
            "Remove or limit debug output before production use.")

    if not suggestions:
        suggestions.append(
            "Code looks clean. Next step: add more test coverage for edge cases.")

    return suggestions


def generate_test_case_suggestions(code, language):
    """
    Provide generic test ideas that beginners can start with.
    """
    tests = [
        "Test with valid/expected input values.",
        "Test with empty input or null-equivalent values.",
        "Test with boundary values (minimum and maximum).",
        "Test with invalid input types to verify error handling.",
    ]

    if language == "python" and "def " in code:
        tests.append(
            "Write unit tests for each function using pytest or unittest.")

    if language in {"java", "cpp", "c++"}:
        tests.append(
            "Test each public function independently with sample and edge-case data.")

    return tests
