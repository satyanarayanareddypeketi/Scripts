import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
project_name="JenkinsServer"
r=requests.get("http://52.49.55.109:8080/jenkins/job/"+project_name+"/api/json")
total_info=r.json()
count=0
total_builds=len(total_info['builds'])
r.close()
import yaml
with open('config.yml','r') as f:
    doc=yaml.load(f)
test_p=doc['TestEnv']['percentage']
preprod_p=doc['PreProdEnv']['percentage']
prod_p=doc['ProdEnv']['percentage']
msg = MIMEMultipart('alternative')

ht="<center><h2>Last 10 Build Results from "+project_name+"</h2>"
ht+="<table style='border:1px solid grey;'>"
ht+="<tr><th style='width:100px;height:35px'>#Build</th><th style='width:100px'>#Success</th><th style='width:100px'>#Fail</th><th style='width:100px;height:35px'>PassPercent</th><th>Deploy to TestEnv</th></tr>"
while(total_builds):
    if count==10:
        break
    fst= total_info['builds'][count]['url']
    r=requests.get(fst+"/api/json")
    data=r.json()
    r.close()
    if data['result']!='FAILURE':
        total_count=data['actions'][-1]['totalCount']
        fail=data['actions'][-1]['failCount']
        succ=total_count-fail
        perc = "%.1f"%((succ/float(total_count))*100)
        if float(perc)>=test_p:
            comment='Yes'
        else:
            comment='No'
        if count%2==0:
            ht+="<tr style='background:#F4F4F4;height:25px;text-align:center'><td >"+str(total_info['builds'][count]['number'])+"</td><td>"+str(succ)+"</td><td>"+str(fail)+"</td><td>"+"%.1f"%((succ/float(total_count))*100)+"</td><td>"+comment+"</td></tr>"
        else:
            ht+="<tr style='height:25px;text-align:center'><td >"+str(total_info['builds'][count]['number'])+"</td><td>"+str(succ)+"</td><td>"+str(fail)+"</td><td>"+"%.1f"%((succ/float(total_count))*100)+"</td><td>"+comment+"</td></tr>"
    else:
        ht+="<tr style='background:#F98C7E;height:25px;text-align:center;'><td>"+str(total_info['builds'][count]['number'])+"</td><td colspan=4>BUILD FAILED</td></tr>"
    count+=1
ht+="</table></center>"
sender="bvrmdevops@gmail.com"
rec="devopsbvrm@gmail.com"
pas="rgukt123"
msg['Subject']=project_name+" Build Report"
msg['From'] = sender
msg['To'] = rec
part1 = MIMEText(ht, 'html')
msg.attach(part1)
se=smtplib.SMTP('smtp.gmail.com:587')
se.starttls()
se.login(sender,pas)
se.sendmail(sender,rec,msg.as_string())
se.quit()
