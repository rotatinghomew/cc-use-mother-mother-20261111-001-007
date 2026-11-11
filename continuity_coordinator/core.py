from __future__ import annotations
import hashlib,json,re
from collections import defaultdict,deque
from typing import Any,Mapping
def stable(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def digest(v): return hashlib.sha256(stable(v).encode()).hexdigest()
class BusinessError(ValueError): pass

from continuity_coordinator.calendar.sqlite_calendar import process_fixture
def run(raw,database):
 p=raw.get('payload',raw); day=int(p.get('day',0)); due=[]; missed=[]; future=[]
 for plan in [dict(x) for x in p.get('plans',[])]:
  next_due=int(plan.get('next_due',0)); quiet=set(int(x) for x in plan.get('quiet_days',[]))
  while next_due in quiet: next_due+=1
  plan['next_due']=next_due
  if not plan.get('active',True) or next_due>day: future.append(plan)
  elif next_due<day: missed.append(plan)
  else: due.append(plan)
 due.sort(key=lambda x:(-int(x.get('priority',0)),x.get('plan_id',''))); responses=[dict(x) for x in p.get('responses',[])]; inconsistent=[x for x in responses if x.get('submitted_day',day)<x.get('scheduled_day',0)]
 escalations=[{'plan_id':x.get('plan_id'),'reason':'missed_window','level':min(5,1+int(x.get('missed_count',0)))} for x in missed]
 result={'due':due,'missed':missed,'future':future,'inconsistent_responses':inconsistent,'escalations':escalations,'next_day':min((x['next_due'] for x in future),default=None),'calendar_hash':digest([due,missed,future])}
 stored=process_fixture(database,{'subject_id':str(p.get('cohort_id','cohort-demo')),'request_key':result['calendar_hash'],'payload':result})
 return {'followup':result,'stored':stored}
