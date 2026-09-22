"""Supplied Lab 1 scaffolding. Analytical answers belong to each pair."""
from pathlib import Path
import hashlib,json
import numpy as np
import pandas as pd
RANDOM_SEED=414
KEYS=['season','round','driver_id']
YEARS={'train':{2019,2020,2021},'calibration':{2022},'test':{2023,2024}}

def root_from(start=None):
    p=Path(start or Path.cwd()).resolve()
    for candidate in (p,*p.parents):
        if (candidate/'data/samples/lab01_v1/lab01_manifest_v1.json').exists():return candidate
    raise FileNotFoundError('Extract the complete Lab 1 ZIP and run inside its folder.')

def validate_sources(q,r,role):
    if role not in YEARS:raise ValueError('Unknown temporal role')
    for df,extra in [(q,['qualifying_position']),(r,['position'])]:
        if df.empty or not set(KEYS+extra).issubset(df.columns):raise ValueError('Empty data or missing schema')
        if df[KEYS].isna().any().any() or df.duplicated(KEYS).any():raise ValueError('Null or duplicate key')
        if set(df.season.unique())!=YEARS[role]:raise ValueError('Unexpected or missing seasons')
        if not df['round'].gt(0).all():raise ValueError('Invalid round')
    for series in [q.qualifying_position.dropna(),r.position]:
        if series.isna().any() or not ((series>=1)&(series%1==0)).all():raise ValueError('Invalid position')

def synthetic_sources(role):
    """Deterministic fictional data for practice only; never a silent fallback."""
    rng=np.random.default_rng(RANDOM_SEED+min(YEARS[role]))
    qr=[];rr=[]
    for year in sorted(YEARS[role]):
        for race in range(1,4):
            positions=rng.permutation(np.arange(1,21))
            for i in range(20):
                common=dict(season=year,round=race,driver_id=f'fictional_{i:02}',race_name=f'Fictional race {race}',constructor_id=f'fictional_team_{i//2}')
                rr.append(dict(**common,position=int(positions[i]),status='Fictional',points=0,laps=1))
                if i!=19:qr.append(dict(**common,qualifying_position=i+1))
    return pd.DataFrame(qr),pd.DataFrame(rr)

def load_sources(role,root=None,mode='snapshot',frozen=False):
    if role not in YEARS:raise ValueError('Unknown temporal role')
    if role=='test' and not frozen:raise ValueError('Freeze and document decisions before opening test.')
    if mode=='synthetic':q,r=synthetic_sources(role)
    elif mode=='snapshot':
        d=root_from(root)/'data/samples/lab01_v1'
        manifest=json.loads((d/'lab01_manifest_v1.json').read_text())
        frames={}
        for endpoint in ('qualifying','results'):
            name=f'{role}_{endpoint}_v1.csv'
            meta=next(f for f in manifest['files'] if f['file']==name)
            p=d/name
            if hashlib.sha256(p.read_bytes()).hexdigest()!=meta['sha256']:raise ValueError('Snapshot hash mismatch: '+name)
            df=pd.read_csv(p)
            if len(df)!=meta['rows']:raise ValueError('Row count mismatch')
            frames[endpoint]=df
        q,r=frames['qualifying'],frames['results']
    else:raise ValueError('Choose snapshot or explicit synthetic practice')
    validate_sources(q,r,role)
    return q,r

def merge_sources(q,r):
    for df in (q,r):
        if df[KEYS].isna().any().any() or df.duplicated(KEYS).any():raise ValueError('Null or duplicate key')
    merged=r.merge(q[KEYS+['qualifying_position']],on=KEYS,how='left',validate='one_to_one',indicator='qualifying_match')
    assert len(merged)==len(r)
    merged['target_top10']=merged.position.between(1,10).astype(int)
    return merged

def binary(values):
    a=np.asarray(values)
    if a.ndim!=1 or len(a)==0 or not np.isin(a,[0,1]).all():raise ValueError('Nonempty binary vector required')
    return a.astype(int)

def majority_from_train(train):
    if set(train.season.unique())!=YEARS['train']:raise ValueError('Fit the majority on train only')
    y=binary(train.target_top10)
    return int(y.mean()>0.5) # Exact ties predict 0.

def baseline_predictions(frame,majority):
    if majority not in (0,1):raise ValueError('Binary majority required')
    q=frame.qualifying_position
    return pd.DataFrame({'majority':np.full(len(frame),majority,dtype=int),
        'qualifying_top10':np.where(q.isna(),majority,q.le(10).astype(int)).astype(int)},index=frame.index)

def metrics(y_true,y_pred):
    y,p=binary(y_true),binary(y_pred)
    if len(y)!=len(p):raise ValueError('Lengths differ')
    tn=int(((y==0)&(p==0)).sum());fp=int(((y==0)&(p==1)).sum())
    fn=int(((y==1)&(p==0)).sum());tp=int(((y==1)&(p==1)).sum())
    ba=((tp/(tp+fn))+(tn/(tn+fp)))/2 if tp+fn and tn+fp else float('nan')
    return dict(n=len(y),TN=tn,FP=fp,FN=fn,TP=tp,accuracy=(tp+tn)/len(y),balanced_accuracy=ba)

def evaluate(frame,majority):
    pred=baseline_predictions(frame,majority)
    return pd.DataFrame({name:metrics(frame.target_top10,pred[name]) for name in pred}).T
