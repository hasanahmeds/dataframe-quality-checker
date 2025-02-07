from dataclasses import asdict,dataclass
import numpy as np

@dataclass(frozen=True)
class Check:
    rule: str
    column: str | None
    severity: str
    failed_count: int
    evaluated_count: int
    sample_positions: list[int]
    message: str

    def to_dict(self) -> dict:
        return {**asdict(self),"passed":self.failed_count==0}

def row_check(rule: str,column: str | None,mask,limit: int,message: str,
              severity: str='error') -> Check:
    flags=np.asarray(mask,dtype=bool)
    return Check(rule,column,severity,int(flags.sum()),len(flags),
                 np.flatnonzero(flags)[:limit].astype(int).tolist(),message)
