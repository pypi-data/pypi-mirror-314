import os
import re
import shlex
import subprocess
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions

server = Server("cli-mcp-server")


class CommandSecurityError(Exception):
    """
    Custom exception for command security violations
    """

    pass


@dataclass
class SecurityConfig:
    """
    Security configuration for command execution
    """

    allowed_commands: set[str]
    allowed_flags: set[str]
    allowed_patterns: List[str]
    max_command_length: int
    command_timeout: int


class CommandExecutor:
    def __init__(self, allowed_dir: str, security_config: SecurityConfig):
        if not allowed_dir or not os.path.exists(allowed_dir):
            raise ValueError("Valid ALLOWED_DIR is required")
        self.allowed_dir = os.path.abspath(os.path.realpath(allowed_dir))
        self.security_config = security_config

    def validate_command(self, command_string: str) -> tuple[str, List[str]]:
        """
        Validates and parses a command string for security and formatting.

        Checks the command string for unsupported shell operators and splits it into
        command and arguments. Only single commands without shell operators are allowed.

        Args:
            command_string (str): The command string to validate and parse.

        Returns:
            tuple[str, List[str]]: A tuple containing:
                - The command name (str)
                - List of command arguments (List[str])

        Raises:
            CommandSecurityError: If the command contains unsupported shell operators.
        """

        # Check for shell operators that we don't support
        shell_operators = ["&&", "||", "|", ">", ">>", "<", "<<", ";"]
        for operator in shell_operators:
            if operator in command_string:
                raise CommandSecurityError(
                    f"Shell operator '{operator}' is not supported. "
                    "Only single commands are allowed."
                )

        try:
            parts = shlex.split(command_string)
            if not parts:
                raise CommandSecurityError("Empty command")

            command, args = parts[0], parts[1:]

            # Validate command
            if command not in self.security_config.allowed_commands:
                raise CommandSecurityError(f"Command '{command}' is not allowed")

            # Validate arguments
            for arg in args:
                if arg.startswith("-"):
                    if arg not in self.security_config.allowed_flags:
                        raise CommandSecurityError(f"Flag '{arg}' is not allowed")
                    continue

                # Validate path if argument looks like a path
                if "/" in arg or "\\" in arg or os.path.isabs(arg):
                    full_path = os.path.abspath(os.path.join(self.allowed_dir, arg))
                    if not self._is_path_safe(full_path):
                        raise CommandSecurityError(f"Path '{arg}' is not allowed")

                # Check patterns
                if not any(
                        re.match(pattern, arg)
                        for pattern in self.security_config.allowed_patterns
                ):
                    raise CommandSecurityError(
                        f"Argument '{arg}' doesn't match allowed patterns"
                    )

            return command, args
        except ValueError as e:
            raise CommandSecurityError(f"Invalid command format: {str(e)}")

    def _is_path_safe(self, path: str) -> bool:
        """
        Checks if a given path is safe to access within allowed directory boundaries.

        Validates that the absolute resolved path is within the allowed directory
        to prevent directory traversal attacks.

        Args:
            path (str): The path to validate.

        Returns:
            bool: True if path is within allowed directory, False otherwise.
                Returns False if path resolution fails for any reason.

        Private method intended for internal use only.
        """
        try:
            abs_path = os.path.abspath(os.path.realpath(path))
            return abs_path.startswith(self.allowed_dir)
        except Exception:
            return False

    def execute(self, command_string: str) -> subprocess.CompletedProcess:
        """
        Executes a command string in a secure, controlled environment.

        Runs the command after validating it against security constraints including length limits
        and shell operator restrictions. Executes with controlled parameters for safety.

        Args:
            command_string (str): The command string to execute.

        Returns:
            subprocess.CompletedProcess: The result of the command execution containing
                stdout, stderr, and return code.

        Raises:
            CommandSecurityError: If the command:
                - Exceeds maximum length
                - Contains invalid shell operators
                - Fails security validation
                - Fails during execution

        Notes:
            - Executes with shell=False for security
            - Uses timeout and working directory constraints
            - Captures both stdout and stderr
        """
        if len(command_string) > self.security_config.max_command_length:
            raise CommandSecurityError("Command string too long")

        try:

            command, args = self.validate_command(command_string)
            return subprocess.run(
                [command] + args,
                shell=False,
                text=True,
                capture_output=True,
                timeout=self.security_config.command_timeout,
                cwd=self.allowed_dir,
            )
        except Exception as e:
            if isinstance(e, CommandSecurityError):
                raise
            raise CommandSecurityError(f"Command execution failed: {str(e)}")


# Load security configuration from environment
def load_security_config() -> SecurityConfig:
    """
    Loads security configuration from environment variables with default fallbacks.

    Creates a SecurityConfig instance using environment variables to configure allowed
    commands, flags, patterns, and execution constraints. Uses predefined defaults if
    environment variables are not set.

    Returns:
        SecurityConfig: Configuration object containing:
            - allowed_commands: Set of permitted command names
            - allowed_flags: Set of permitted command flags/options
            - allowed_patterns: List of regex patterns for valid inputs
            - max_command_length: Maximum length of command string
            - command_timeout: Maximum execution time in seconds

    Environment Variables:
        ALLOWED_COMMANDS: Comma-separated list of allowed commands (default: "ls,cat,pwd")
        ALLOWED_FLAGS: Comma-separated list of allowed flags (default: "-l,-a,--help")
        ALLOWED_PATTERNS: Comma-separated list of patterns (default: "*.txt,*.log,*.md")
        MAX_COMMAND_LENGTH: Maximum command string length (default: 1024)
        COMMAND_TIMEOUT: Command timeout in seconds (default: 30)
    """
    return SecurityConfig(
        allowed_commands=set(os.getenv("ALLOWED_COMMANDS", "ls,cat,pwd").split(",")),
        allowed_flags=set(os.getenv("ALLOWED_FLAGS", "-l,-a,--help").split(",")),
        allowed_patterns=[
            r"^[\w\-. ]+$",  # Basic filename pattern
            *os.getenv("ALLOWED_PATTERNS", "*.txt,*.log,*.md").split(","),
        ],
        max_command_length=int(os.getenv("MAX_COMMAND_LENGTH", "1024")),
        command_timeout=int(os.getenv("COMMAND_TIMEOUT", "30")),
    )


executor = CommandExecutor(
    allowed_dir=os.getenv("ALLOWED_DIR", ""), security_config=load_security_config()
)


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="run_command",
            description=(
                f"Allows command (CLI) execution in the directory: {executor.allowed_dir}\n\n"
                f"Available commands: {', '.join(executor.security_config.allowed_commands)}\n"
                f"Available flags: {', '.join(executor.security_config.allowed_flags)}\n\n"
                "Note: Shell operators (&&, |, >, >>) are not supported."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Single command to execute (example: 'ls -l' or 'cat file.txt')"
                    }
                },
                "required": ["command"],
            },
        ),
        types.Tool(
            name="show_security_rules",
            description=(
                "Show what commands and operations are allowed in this environment.\n"
            ),
            inputSchema={
                "type": "object",
                "properties": {},
            },
        )
    ]


@server.call_tool()
async def handle_call_tool(
        name: str, arguments: Optional[Dict[str, Any]]
) -> List[types.TextContent]:
    if name == "run_command":
        if not arguments or "command" not in arguments:
            return [
                types.TextContent(type="text", text="No command provided", error=True)
            ]

        try:
            result = executor.execute(arguments["command"])

            response = []
            if result.stdout:
                response.append(types.TextContent(type="text", text=result.stdout))
            if result.stderr:
                response.append(
                    types.TextContent(type="text", text=result.stderr, error=True)
                )

            response.append(
                types.TextContent(
                    type="text",
                    text=f"\nCommand completed with return code: {result.returncode}",
                )
            )

            return response

        except CommandSecurityError as e:
            return [
                types.TextContent(
                    type="text", text=f"Security violation: {str(e)}", error=True
                )
            ]
        except subprocess.TimeoutExpired:
            return [
                types.TextContent(
                    type="text",
                    text=f"Command timed out after {executor.security_config.command_timeout} seconds",
                    error=True,
                )
            ]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error: {str(e)}", error=True)]

    elif name == "show_security_rules":
        security_info = (
            "Security Configuration:\n"
            f"==================\n"
            f"Working Directory: {executor.allowed_dir}\n"
            f"\nAllowed Commands:\n"
            f"----------------\n"
            f"{', '.join(sorted(executor.security_config.allowed_commands))}\n"
            f"\nAllowed Flags:\n"
            f"-------------\n"
            f"{', '.join(sorted(executor.security_config.allowed_flags))}\n"
            f"\nAllowed Patterns:\n"
            f"----------------\n"
            f"{', '.join(executor.security_config.allowed_patterns)}\n"
            f"\nSecurity Limits:\n"
            f"---------------\n"
            f"Max Command Length: {executor.security_config.max_command_length} characters\n"
            f"Command Timeout: {executor.security_config.command_timeout} seconds\n"
        )
        return [types.TextContent(type="text", text=security_info)]

    raise ValueError(f"Unknown tool: {name}")


async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="cli-mcp-server",
                server_version="0.1.1",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
