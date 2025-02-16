import pandas as pd

def profile(frame: pd.DataFrame) -> dict:
    return {'rows':len(frame),'columns':[
        {'name':str(name),'dtype':str(frame[name].dtype),
         'missing':int(frame[name].isna().sum()),'nonmissing':int(frame[name].notna().sum())}
        for name in frame.columns]}
