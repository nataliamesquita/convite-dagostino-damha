import base64,re,os,shutil
ADDRESS="Rua José Arlindo de Melo Silva, 1486, Parque São Miguel"
s=open('src.html').read()
b=lambda f,m:'data:%s;base64,%s'%(m,base64.b64encode(open(f,'rb').read()).decode())
s=s.replace('{{LOGO}}',b('logo.png','image/png')).replace('{{LEO}}',b('leo.webp','image/webp'))
ics='\r\n'.join(['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//DAgostino//Convite//PT','BEGIN:VEVENT','UID:coquetel-damha-20261126@grupodagostino.com.br','DTSTAMP:20261106T120000Z','DTSTART:20261126T220000Z','DTEND:20261127T010000Z',"SUMMARY:Inauguração Dagostino Papelaria e Brinquedo · Damha",'LOCATION:'+(ADDRESS+', São José do Rio Preto - SP').replace(',','\\,'),'DESCRIPTION:Comida e drinks\\, monitoras para as crianças e manobrista no local.','BEGIN:VALARM','TRIGGER:-PT3H','ACTION:DISPLAY','DESCRIPTION:Inauguração Dagostino Papelaria e Brinquedo hoje às 19h','END:VALARM','END:VEVENT','END:VCALENDAR'])+'\r\n'
for d in ('out/site','out/artifact'): os.makedirs(d,exist_ok=True)
for d in ('out/site','out/artifact'):
    open(d+'/coquetel-dagostino-damha.ics','w').write(ics)
    for f in ('porta.mp4','porta-inicio.jpg','porta-final.jpg','og.png'):
        if os.path.exists(f): shutil.copy(f,d)
open('out/site/index.html','w').write(s)
a=s
a=re.sub(r'<!doctype html>\s*<html[^>]*>\s*<head>','',a,flags=re.I)
a=a.replace('</head>','').replace('<body>','').replace('</body>','').replace('</html>','')
a=re.sub(r'<meta charset="utf-8">\s*<meta name="viewport"[^>]*>','<meta name="claude:viewport-fit-sides" content="cover">',a)
a=re.sub(r'<title>[^<]*</title>','',a,count=1)
a='<title>Convite de Inauguração Dagostino Papelaria e Brinquedo</title>\n'+a.lstrip()
open('out/artifact/index.html','w').write(a)
