import argparse
from contextlib import nullcontext
import logging
from pathlib import Path
import sys
import pandas as pd
from . import __version__
from .output import atomic_output,protect
from .reader import read_csv
from .reporting import write_report
from .schema import Schema
from .validator import validate

def main(argv: list[str] | None=None) -> int:
    parser=argparse.ArgumentParser(description='Validate CSV data with a JSON schema')
    parser.add_argument('input',type=Path)
    parser.add_argument('--schema',type=Path,required=True)
    parser.add_argument('--format',choices=['json','csv'],default='json')
    parser.add_argument('--output',type=Path)
    parser.add_argument('--max-rows',type=int,default=1000000)
    parser.add_argument('--fail-on-warning',action='store_true')
    parser.add_argument('--verbose',action='store_true')
    parser.add_argument('--version',action='version',version=__version__)
    args=parser.parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.WARNING,
                        format='%(levelname)s: %(message)s',force=True)
    try:
        if args.output:
            protect(args.output,[args.input,args.schema])
        schema=Schema.load(args.schema)
        frame=read_csv(args.input,args.max_rows)
        report=validate(frame,schema)
        with atomic_output(args.output) if args.output else nullcontext(sys.stdout) as stream:
            write_report(report,stream,args.format)
        return 1 if not report['passed'] or (args.fail_on_warning and report['failed_warning_checks']) else 0
    except (OSError,ValueError,TypeError,pd.errors.ParserError) as exc:
        logging.error('%s',exc)
        return 2
