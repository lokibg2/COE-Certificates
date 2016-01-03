import PIL, MySQLdb, os, smtplib, easygui
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email import Encoders

def SendMail(ImgFileName,To,name):
    img_data = open(ImgFileName, 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = 'Certificate'
    msg['From'] = 'lokibg2@gmail.com'
    msg['To'] = To
    From = 'lokibg2@gmail.com'    
    text = MIMEText("Dear " + name.split()[0] + ",\nYour certificate for the IOS developement coaching has been attached with this email.")
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    msg.attach(image)
    s = smtplib.SMTP('smtp.gmail.com:587')
    s.starttls()
    s.login("lokibg2@gmail.com", "Appoyy1!")
    s.sendmail(From, To, msg.as_string())
    s.quit()


font = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf",90)

db = MySQLdb.connect("localhost","loki","appoyy","coe" )
cursor = db.cursor()
sql = "SELECT * FROM stud"
cursor.execute(sql)
results = cursor.fetchall()
c = 0
for row in results:
    name,email,coll = row
    img = Image.open('Sample Certificate Image.jpg')
    draw = ImageDraw.Draw(img)
    draw.text((1650-10*len(name), 830),name,(0,0,0),font=font)
    if coll[-1] == 'y':
        draw.text((700, 1100),coll,(0,0,0),font=font)
    else:
        draw.text((1300, 1100),coll,(0,0,0),font=font)
    draw = ImageDraw.Draw(img)
    img.save(name + ".png")
    img.show()
    c += 1
    if(easygui.ynbox('Email the certificate ?', 'Confirm Certificate', ('Yes', 'No'))):
        SendMail(name + ".png", email,name)
        print str(c) + ") Sent to " + name
    else:
        print str(c) + ") Not Sent to " + name
db.close()

