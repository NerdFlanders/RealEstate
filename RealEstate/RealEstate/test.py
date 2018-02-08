import re

line = "Eigentumswohnung in bester Lage in Nordhausen - Oberstadt, 2=85 <https://www.immobilienscout24.de/expose/102720755?PID=3D72190153&CCWID=3D$CWID_CONTACT$&utm_medium=3Demail&utm_source=3Dsystem&utm_campaign=3Ddefault_fulfillment_2&utm_content=3Ddefault_expose_redesign_mobileWithTitle>4,45 km | Barf=FCsser Str. 24, Nordhausen, Nordhausen (Kreis)"

matchObj = re.search( r'<https://www\.immobilienscout24\.de/expose/(.*)_mobileWithTitle>', line)

if matchObj:
   print ("matchObj.group() : ", matchObj.group())
#    print ("matchObj.group(1) : ", matchObj.group(1))
#    print ("matchObj.group(2) : ", matchObj.group(2))
else:
   print ("No match!!")