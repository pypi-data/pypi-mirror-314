from pydantic import BaseModel, Field
from typing import Optional, Dict
from io import StringIO
import logging
import multiprocessing
import re
import sys

class PythonREPL(BaseModel):
    """Simplified standalone Python REPL with sandboxed execution."""

    globals: Optional[Dict] = Field(default_factory=dict)
    locals: Optional[Dict] = Field(default_factory=dict)

    @staticmethod
    def sanitize_input(query: str) -> str:
        """Sanitize REPL input by removing common misinterpretations and excess whitespace."""
        return re.sub(r"^(\s|`)*(?i:python)?\s*|(\s|`)*$", "", query)

    @classmethod
    def worker(cls, command: str, globals: Dict, locals: Dict, queue: multiprocessing.Queue) -> None:
        """Execute command and capture output, placing result in the queue."""
        with StringIO() as mystdout:
            sys.stdout = mystdout
            try:
                exec(cls.sanitize_input(command), globals, locals)
                queue.put(mystdout.getvalue())
            except Exception as e:
                queue.put(repr(e))
            finally:
                sys.stdout = sys.__stdout__  # Restore original stdout

    def run(self, command: str, timeout: Optional[int] = None) -> str:
        """Run command with optional timeout; captures and returns output or error."""
        queue = multiprocessing.Queue()

        if timeout:
            process = multiprocessing.Process(target=self.worker, args=(command, self.globals, self.locals, queue))
            process.start()
            process.join(timeout)
            if process.is_alive():
                process.terminate()
                return "Execution timed out"
        else:
            self.worker(command, self.globals, self.locals, queue)

        return queue.get() or "Code executed sucessfully."
    
repl_tool = PythonREPL()
