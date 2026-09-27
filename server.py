from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import json, sqlite3, os
from pathlib import Path
ROOT=Path(__file__).parent
DB=ROOT/'kaizen.sqlite3'
seed={
 'profile': {'name':'Aarav Sharma','degree':'B.Sc. Data Science','branch':'Data Science','year':'3','institution':'Pune Institute of Technology','location':'Pune','email':'aarav@example.com','interest':'Data & Analytics','preferredRole':'Data Analyst','bio':'Curious about turning real-world data into meaningful decisions. Building my skills in analytics and visualization.'},
 'skills':{'Python':65,'SQL':42,'Excel':82,'Statistics':58,'Power BI':35,'GIS':20,'Communication':72,'Teamwork':64,'Problem Solving':84},
 'applications':[], 'completed':[], 'assessmentTaken':False,
 'projects':[{'name':'Rainfall Prediction','description':'Exploratory analysis and a Python model using synthetic weather data.','skills':['Python','Statistics'],'status':'Self-reported'},{'name':'Attendance Analytics','description':'An Excel dashboard that makes student attendance patterns easier to understand.','skills':['Excel'],'status':'Self-reported'}],
 'opportunities':[
 {'id':1,'title':'Data Analytics Intern','company':'Lumina Labs','initials':'L','color':'purple','type':'Internship','location':'Pune','mode':'Hybrid','stipend':'₹18,000 / month','duration':'3 months','category':'Data & Analytics','requirements':{'Python':60,'SQL':65,'Excel':60,'Statistics':60},'description':'Work alongside our analytics team to explore datasets, write SQL queries, and build reports that inform product decisions.','education':['B.Sc. Data Science','B.Tech','BCA'],'posted':'2 days ago'},
 {'id':2,'title':'Environmental Data Intern','company':'Terra Insights','initials':'ti','color':'green','type':'Internship','location':'Remote','mode':'Remote','stipend':'₹15,000 / month','duration':'6 months','category':'Data & Analytics','requirements':{'Python':60,'Excel':60,'Statistics':60,'GIS':50},'description':'Help our research team understand environmental trends through geospatial data and accessible visualizations.','education':['B.Sc. Data Science','B.Tech','BCA'],'posted':'1 day ago'},
 {'id':3,'title':'Business Intelligence Intern','company':'Orbit Works','initials':'o','color':'blue','type':'Internship','location':'Bengaluru','mode':'On-site','stipend':'₹22,000 / month','duration':'3 months','category':'Data & Analytics','requirements':{'SQL':70,'Excel':70,'Power BI':65},'description':'Create business dashboards, document reporting processes, and translate stakeholder questions into useful metrics.','education':['B.Sc. Data Science','B.Tech','BCA'],'posted':'3 days ago'},
 {'id':4,'title':'Junior Data Analyst','company':'Lumina Labs','initials':'L','color':'purple','type':'Job','location':'Pune','mode':'Hybrid','stipend':'₹5–7 LPA','duration':'Full-time','category':'Data & Analytics','requirements':{'Python':75,'SQL':80,'Excel':75,'Statistics':70,'Power BI':65},'description':'Join a small team building dependable analytics for growing businesses. Own data quality, weekly reports, and exploratory analysis.','education':['B.Sc. Data Science','B.Tech'],'posted':'Today'}],
 'mentorshipRequests':[], 'audit':[]}
con=sqlite3.connect(DB);con.execute('CREATE TABLE IF NOT EXISTS app_state (id INTEGER PRIMARY KEY, data TEXT NOT NULL)');con.execute('INSERT OR IGNORE INTO app_state VALUES (1,?)',(json.dumps(seed),));con.commit();con.close()
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT/'static'),**kw)
 def send_json(self,data,status=200):
  body=json.dumps(data).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
 def do_GET(self):
  if self.path=='/api/state':
   with sqlite3.connect(DB) as db: data=json.loads(db.execute('SELECT data FROM app_state WHERE id=1').fetchone()[0])
   return self.send_json(data)
  return super().do_GET()
 def do_POST(self):
  if self.path!='/api/state':return self.send_json({'error':'Not found'},404)
  try:
   n=int(self.headers.get('Content-Length',0))
   if n>200000:return self.send_json({'error':'Request too large'},413)
   patch=json.loads(self.rfile.read(n))
   if not isinstance(patch,dict) or any(k not in seed for k in patch):raise ValueError('Invalid state')
   with sqlite3.connect(DB) as db:
    state=json.loads(db.execute('SELECT data FROM app_state WHERE id=1').fetchone()[0]);state.update(patch)
    db.execute('UPDATE app_state SET data=? WHERE id=1',(json.dumps(state),))
   self.send_json({'ok':True})
  except Exception:return self.send_json({'error':'Invalid request'},400)
if __name__=='__main__':ThreadingHTTPServer(('0.0.0.0',3000),Handler).serve_forever()
