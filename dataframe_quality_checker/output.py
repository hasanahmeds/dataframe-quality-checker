from contextlib import contextmanager
import os
from pathlib import Path
import tempfile
from typing import Iterator,TextIO

@contextmanager
def atomic_output(path: Path) -> Iterator[TextIO]:
    fd,name=tempfile.mkstemp(prefix='.df-quality-',dir=path.parent)
    temporary=Path(name)
    try:
        with os.fdopen(fd,'w',encoding='utf-8',newline='') as stream:
            yield stream
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary,path)
    finally:
        temporary.unlink(missing_ok=True)

def protect(output: Path,inputs: list[Path]) -> None:
    for path in inputs:
        if output.resolve()==path.resolve() or (output.exists() and path.exists() and output.samefile(path)):
            raise ValueError('output cannot overwrite an input or schema file')
