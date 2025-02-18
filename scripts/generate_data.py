"""Usage: python scripts/generate_data.py --rows 1000 --dirty > synthetic.csv"""
import argparse
import csv
import random
import sys

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rows',type=int,default=1000)
    parser.add_argument('--seed',type=int,default=42)
    parser.add_argument('--dirty',action='store_true')
    args=parser.parse_args()
    if args.rows<1:
        parser.error('rows must be positive')
    rng=random.Random(args.seed)
    writer=csv.writer(sys.stdout)
    writer.writerow(['customer_id','age','email','country','spend'])
    for index in range(1,args.rows+1):
        row=[index,rng.randint(18,85),f'person{index}@example.invalid',rng.choice(['US','IN','GB']),round(rng.uniform(50,150),2)]
        if args.dirty and index%10==0:
            row[1]=200
            row[2]='invalid'
        if args.dirty and index%17==0:
            row[4]=10000
        writer.writerow(row)

if __name__=='__main__':
    main()
