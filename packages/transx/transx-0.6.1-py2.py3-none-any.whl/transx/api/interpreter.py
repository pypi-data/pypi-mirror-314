#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Text interpretation functionality."""

# Import built-in modules
import os
import re

# Import local modules
from transx.constants import DEFAULT_ENCODING
from transx.internal.compat import binary_type
from transx.internal.compat import text_type
from transx.internal.logging import get_logger


class TextInterpreter(object):
    """Base interpreter class for text processing."""
    name = "base"
    description = "Base interpreter class"

    def interpret(self, text, context=None):
        """Interpret the text with given context.

        Args:
            text: Text to interpret
            context: Optional context dictionary

        Returns:
            Interpreted text
        """
        raise NotImplementedError()


class TranslationInterpreter(TextInterpreter):
    """Interpreter for text translation."""
    name = "translation"
    description = "Translates text using a translator instance"

    def __init__(self, translator):
        """Initialize with translator instance.

        Args:
            translator: Translator instance to use
        """
        self.translator = translator

    def interpret(self, text, context=None):
        """Interpret text by translating it.

        Args:
            text: Text to translate
            context: Not used

        Returns:
            Translated text
        """
        return self.translator.translate(text)


class DollarSignInterpreter(TextInterpreter):
    """Interpreter for handling dollar signs."""
    name = "dollar_sign"
    description = "Handles dollar sign escaping"

    def __init__(self):
        """Initialize patterns."""
        self._pattern = re.compile(r"\$\$(?!\{)(\w+|\$)?")  # Match $$ not followed by { and optionally followed by word or $
        self._placeholder = "__DOLLAR_SIGN_PLACEHOLDER_9527__"

    def interpret(self, text, context=None):
        """Interpret text by handling dollar signs.

        Args:
            text: Text to process
            context: Dictionary of parameters to substitute (unused)

        Returns:
            Text with dollar signs processed
        """
        if not text:
            return text

        # Replace $$ with placeholder
        def repl(match):
            suffix = match.group(1) or ""
            return self._placeholder + suffix

        result = self._pattern.sub(repl, text)
        return result


class DollarSignRestoreInterpreter(TextInterpreter):
    """Interpreter for restoring dollar signs."""
    name = "dollar_sign_restore"
    description = "Restores escaped dollar signs"

    def __init__(self):
        """Initialize patterns."""
        self._placeholder = "__DOLLAR_SIGN_PLACEHOLDER_9527__"

    def interpret(self, text, context=None):
        """Interpret text by restoring dollar signs.

        Args:
            text: Text to process
            context: Dictionary of parameters to substitute (unused)

        Returns:
            Text with dollar signs restored
        """
        if not text:
            return text

        # Replace placeholder with $
        result = text.replace(self._placeholder, "$")
        return result


class EnvironmentVariableInterpreter(TextInterpreter):
    """Interpreter for environment variable expansion."""
    name = "environment_variable"
    description = "Handles environment variable expansion"

    def __init__(self):
        """Initialize patterns."""
        self._pattern = re.compile(r"(?:__DOLLAR_SIGN_PLACEHOLDER_9527__|\$)(?!\$|\{)(\w+)")  # Match placeholder or $ not followed by $ or {
        self._placeholder = "__DOLLAR_SIGN_PLACEHOLDER_9527__"

    def interpret(self, text, context=None):
        """Interpret text by expanding environment variables.

        Args:
            text: Text to process
            context: Dictionary of parameters to substitute (unused)

        Returns:
            Text with environment variables expanded
        """
        if not text:
            return text

        result = text
        matches = list(self._pattern.finditer(text))
        for match in matches:
            var_name = match.group(1)

            # Get environment variable value, keep original if not found
            value = os.environ.get(var_name)
            if value is None:
                continue

            if isinstance(value, str):
                value = text_type(value)

            # Replace in text
            if match.group(0).startswith(self._placeholder):
                result = result.replace(match.group(0), self._placeholder + value)
            else:
                result = result.replace(match.group(0), value)

        return result


class DollarVariableInterpreter(TextInterpreter):
    """Interpreter for $var and ${var} style variables."""
    name = "dollar_var"
    description = "Handles $var and ${var} style variables"

    def __init__(self):
        self._var_pattern = re.compile(r"\${(\w+)}")

    def interpret(self, text, context=None):
        """Interpret text by replacing $var and ${var} with {var}.

        Args:
            text: Text to process
            context: Dictionary of parameters to substitute

        Returns:
            Text with $var and ${var} converted to {var}
        """
        if not context or "$" not in text:
            return text

        result = text

        # Handle ${var} format
        result = self._var_pattern.sub(r"{\1}", result)

        # Handle $var format (without braces)
        for key in context:
            result = result.replace("$" + key, "{" + key + "}")

        return result


class ParameterSubstitutionInterpreter(TextInterpreter):
    """Interpreter for parameter substitution using str.format()."""
    name = "parameter"
    description = "Substitutes parameters using str.format()"

    def __init__(self):
        self._numeric_pattern = re.compile(r"{(\d+)}")

    def interpret(self, text, context=None):
        """Interpret text by substituting parameters.

        Args:
            text: Text to process
            context: Dictionary of parameters to substitute

        Returns:
            Text with parameters substituted
        """
        if not context:
            return text

        try:
            # For single parameter, try both {0} and {name} formats
            if len(context) == 1:
                param_value = next(iter(context.values()))

                # If text contains {0}, use positional format
                if self._numeric_pattern.search(text):
                    return text.format(param_value)
                # Otherwise use named format
                return text.format(**context)
            # For multiple parameters, use named format
            return text.format(**context)
        except (KeyError, ValueError, IndexError):
            return text


class NestedTemplateInterpreter(TextInterpreter):
    """Interpreter for handling nested template syntax."""
    name = "nested_template"
    description = "Handles nested template syntax like $${var} and {{var}}"

    def __init__(self):
        """Initialize patterns."""
        self._nested_dollar_pattern = re.compile(r"\$\${(\w+)}")
        self._nested_brace_pattern = re.compile(r"\{\{(\w+)\}\}")

    def interpret(self, text, context=None):
        """Interpret text by handling nested template syntax.

        Args:
            text: Text to process
            context: Dictionary of parameters to substitute

        Returns:
            Text with nested templates processed
        """
        if not text or not context:
            return text

        result = text

        # Handle $${var} -> $value
        if "$${" in result:
            def dollar_repl(match):
                key = match.group(1)
                if key not in context:
                    return match.group(0)  # Keep original if key not found
                value = context[key]
                if isinstance(value, str):
                    value = text_type(value)
                return text_type("$") + text_type(value)
            result = self._nested_dollar_pattern.sub(dollar_repl, result)

        # Handle {{var}} -> {value}
        if "{{" in result:
            def brace_repl(match):
                key = match.group(1)
                if key not in context:
                    return match.group(0)  # Keep original if key not found
                value = context[key]
                if isinstance(value, str):
                    value = text_type(value)
                return text_type("{") + text_type(value) + text_type("}")
            result = self._nested_brace_pattern.sub(brace_repl, result)

        return result


class TextTypeInterpreter(TextInterpreter):
    """Ensure text is of the correct type."""

    def interpret(self, text, context=None):
        """Interpret text by ensuring correct text type.

        Args:
            text: Text to process
            context: Not used

        Returns:
            Text converted to correct type
        """
        try:
            if not isinstance(text, text_type):
                if isinstance(text, binary_type):
                    return text.decode(DEFAULT_ENCODING)
                return text_type(text)
            return text
        except UnicodeDecodeError:
            # If DEFAULT_ENCODING decode fails, try with error handling
            if isinstance(text, binary_type):
                return text.decode(DEFAULT_ENCODING, errors="replace")
            return text_type(text)


class InterpreterExecutor(object):
    """Executes a chain of interpreters in configured order."""

    def __init__(self, interpreters=None):
        """Initialize with optional list of interpreters.

        Args:
            interpreters: List of interpreter instances to use. If None, an empty chain is created.
        """
        self.interpreters = interpreters or []
        self.logger = get_logger(__name__)

    def add_interpreter(self, interpreter):
        """Add an interpreter to the chain.

        Args:
            interpreter: Interpreter instance to add

        Returns:
            self for method chaining
        """
        self.interpreters.append(interpreter)
        return self

    def remove_interpreter(self, interpreter_name):
        """Remove an interpreter from the chain by name.

        Args:
            interpreter_name: Name of the interpreter to remove

        Returns:
            self for method chaining
        """
        self.interpreters = [i for i in self.interpreters if i.name != interpreter_name]
        return self

    def clear_interpreters(self):
        """Clear all interpreters from the chain.

        Returns:
            self for method chaining
        """
        self.interpreters = []
        return self

    def execute(self, text, context=None):
        """Execute all interpreters in the chain.

        Args:
            text: Input text to process
            context: Optional context dictionary passed to each interpreter

        Returns:
            Processed text after running through all interpreters
        """
        result = text
        for interpreter in self.interpreters:
            try:
                next_result = interpreter.interpret(result, context)
                if next_result is not None:  # Only update if interpreter returned a result
                    result = next_result
            except Exception as e:
                self.logger.warning("Interpreter {0} failed: {1}".format(
                    interpreter.name, str(e)))
                # Continue with current result even if interpreter fails
                continue
        return result

    def execute_safe(self, text, context=None, fallback_interpreters=None):
        """Execute interpreters with fallback chain on failure.

        Args:
            text: Input text to process
            context: Optional context dictionary passed to each interpreter
            fallback_interpreters: Optional list of interpreters to use if main chain fails

        Returns:
            Processed text, or original text if all interpreters fail
        """
        try:
            return self.execute(text, context)
        except Exception as e:
            self.logger.warning("Main interpreter chain failed: {0}".format(str(e)))
            if fallback_interpreters:
                try:
                    result = text
                    for interpreter in fallback_interpreters:
                        result = interpreter.interpret(result, context)
                    return result
                except Exception as e:
                    self.logger.warning(
                        "Fallback interpreter chain failed: {0}".format(str(e)))
            return text_type(text)


class InterpreterFactory(object):
    """Factory for creating common interpreter configurations."""

    @staticmethod
    def create_translation_chain(translator):
        """Create a standard translation interpreter chain.

        Args:
            translator: Translator instance to use

        Returns:
            Configured InterpreterExecutor
        """
        return InterpreterExecutor([
            TextTypeInterpreter(),
            TranslationInterpreter(translator),
            NestedTemplateInterpreter(),  # First handle nested templates
            DollarSignInterpreter(),  # Then handle $$ -> placeholder
            EnvironmentVariableInterpreter(),  # Then expand environment variables
            DollarVariableInterpreter(),  # Then handle regular variables
            ParameterSubstitutionInterpreter(),  # Finally do parameter substitution
            DollarSignRestoreInterpreter(),  # Restore $ from placeholder
            TextTypeInterpreter()
        ])

    @staticmethod
    def create_parameter_only_chain():
        """Create an interpreter chain for parameter substitution only.

        Returns:
            Configured InterpreterExecutor
        """
        return InterpreterExecutor([
            TextTypeInterpreter(),
            NestedTemplateInterpreter(),  # First handle nested templates
            DollarSignInterpreter(),  # Then handle $$ -> placeholder
            EnvironmentVariableInterpreter(),  # Then expand environment variables
            DollarVariableInterpreter(),  # Then handle regular variables
            ParameterSubstitutionInterpreter(),  # Finally do parameter substitution
            DollarSignRestoreInterpreter(),  # Restore $ from placeholder
            TextTypeInterpreter()
        ])
