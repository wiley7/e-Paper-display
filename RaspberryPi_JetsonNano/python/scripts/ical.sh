cd ~/source/e-Paper/RaspberryPi_JetsonNano/python/scripts && /usr/local/bin/icalBuddy -npn -nc -iep 'title,datetime' -ic "我的日历（钉钉）,Todoist" -n eventsToday+2 > txt/display.txt && git ci -am 'update' && git push
ssh pi@192.168.1.221 "cd /home/pi/source/e-Paper/RaspberryPi_JetsonNano/python/scripts && git pull &&  /usr/bin/python txt.py  -f txt/display.txt"
