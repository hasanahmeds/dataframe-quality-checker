"""Run from the repository root: python scripts/benchmark.py --rows 100000"""
import argparse
from pathlib import Path
import sys
import time
import tracemalloc
import numpy as np
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from dataframe_quality_checker import validate

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rows',type=int,default=100000)
    args=parser.parse_args()
    if args.rows<1:parser.error('rows must be positive')
    rng=np.random.default_rng(42)
    frame=pd.DataFrame({'id':np.arange(args.rows),'value':rng.normal(100,10,args.rows)})
    schema={'version':1,'columns':{'id':{'type':'integer','unique':True},'value':{'type':'number','outlier':{'method':'iqr'}}}}
    tracemalloc.start();start=time.perf_counter()
    result=validate(frame,schema)
    elapsed=time.perf_counter()-start
    print(f"rows={args.rows} seconds={elapsed:.3f} peak_validation_bytes={tracemalloc.get_traced_memory()[1]} passed={result['passed']}")

if __name__=='__main__':main()
