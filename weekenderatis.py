import discord
import os
import requests
import datetime
from datetime import timezone

atisletters=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
lastdatetime=datetime.datetime.utcnow()
atisepoch=datetime.datetime.utcnow()

walterbussettimes=["200545","200555","200615","200655"]
meadowsettimes=["200500","200515","200625","200645","200715","200716","200720","200810","200815","200825","200830","200831","200835","200845","200915","201015"]
campsitesettimes=["200500","200615","200625","200645","200715"]
shalasettimes=["200500","200610","200615","200635","200640","200645","200715"]
gorgesettimes=["200555","200650","200655","200715","200720","200725","200730","200735","200740","200745","200800","200805","200810","200815","200820","200825","200835"]

walterbusartists=["Above & Beyond and Friends","Artist Meet & Greets","A&R Demo Drop w/Anjunabeats","Artist Meet & Greets"]
meadowartists=["Naz","Rodg","Nourey","Bexxie","Chris Giuliano","A&B Classics perf. by Soundwave Barbershop Quartet","Daybreaker","Jono Grant speaks to Andrew Bayer & Alison May","We're All In This Together Climate Q&A","A&B Classics perf. by Soundwave Barbershop Quartet",\
"Anjuna Pub Quiz w/ Anjuna HQ","Acro Yoga by Daybreaker","Flow State Meditation w/ Paavo & Elena Brower","Leave the Bones Film Preview & Haitian Rhythm & Dance Workshop","Genix 199X Album Chill Set","Qrion Ambient Set"]
campsiteartists=["Anjunafamily Room pres by The Instigators","Trance Classics Food Truck Aftershow","Anjunafamily Room pres by The Instigators","Anjunafamily Room pres by The Instigators","Anjunafamily Room pres by The Instigators"]
shalaartists=["Anjunafamily Room pres by The Instigators","Eurodance Food Truck Aftershow w/ Fatum","Anjunafamily Room pres by The Instigators","Euphoria Effect Yoga w/ Katelyn Means","Yin Yang Yoga w/ Fitzjoy & Joan","Euphoria Effect Yoga w/ Katelyn Means",\
"Self Care Sunday w/ Dru West & Stephanie Bard"]
gorgeartists=["Nourey","Bexxie","Amy Wiles","aname","Fatum","Oliver Smith","Andrew Bayer","Mat Zo","Above & Beyond","Genix","Lakou Mizik & Joseph Ray pres Leave The Bones","OLAN","Qrion","Franky Wah","Marsh","James Grant & Jody Wisternoff","Eli & Fur","Ben Bohmer"]



currentwalterbusartist="UNDEFINED"
currentmeadowartist="UNDEFINED"
currentcampsiteartist="UNDEFINED"
currentshalaartist="UNDEFINED"
currentgorgeartist="UNDEFINED"

client=discord.Client()

@client.event
async def on_ready():
    print('ATIS ONLINE'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('atis'):
      global lastdatetime

      #get current time
      currentdatetime=datetime.datetime.utcnow()
      #get METAR
      c_atis=requests.get('https://aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&stationString=KMWH&hoursBeforeNow=2')
      atisoutput = (c_atis.text)
      begin=atisoutput.find("Z ")
      end=atisoutput.find("</raw_text>")

      timediff=currentdatetime-atisepoch
      hourdiff=timediff.total_seconds()/3600
      currentatisindex = int((hourdiff) % 26)


      for idx, x in reversed(list(enumerate(walterbussettimes))):
        if (int(currentdatetime.strftime("%d%H%M")) > int(walterbussettimes[idx])):
          currentwalterbusartist=walterbusartists[idx]
          break
        else:
          currentwalterbusartist="EMPTY"

      for idx, x in reversed(list(enumerate(meadowsettimes))):
        if (int(currentdatetime.strftime("%d%H%M")) > int(meadowsettimes[idx])):
          currentmeadowartist=meadowartists[idx]
          break
        else:
          currentmeadowartist="EMPTY"

      for idx, x in reversed(list(enumerate(campsitesettimes))):
        if (int(currentdatetime.strftime("%d%H%M")) > int(campsitesettimes[idx])):
          currentcampsiteartist=campsiteartists[idx]
          break
        else:
          currentcampsiteartist="EMPTY"

      for idx, x in reversed(list(enumerate(shalasettimes))):
        if (int(currentdatetime.strftime("%d%H%M")) > int(shalasettimes[idx])):
          currentshalaartist=shalaartists[idx]
          break
        else:
          currentshalaartist="EMPTY"

      for idx, x in reversed(list(enumerate(gorgesettimes))):
        if (int(currentdatetime.strftime("%d%H%M")) > int(gorgesettimes[idx])):
          currentgorgeartist=gorgeartists[idx]
          break
        else:
          currentgorgeartist="EMPTY"

      combined = "GORGE ATIS INFO " + atisletters[currentatisindex] + " " + currentdatetime.strftime("%d%H%M") + "Z " + atisoutput[begin+2:end] + "\n\nREMARKS \nWALTERBUS: " + currentwalterbusartist + "\nMEADOW: " + currentmeadowartist + \
        "\nCAMPSITE: " + currentcampsiteartist + "\nSHALA: " + currentshalaartist + "\nAMPHI: " + currentgorgeartist
      await message.channel.send(combined)


    if message.content.startswith('taf'):
      #get current time
      currentdatetime=datetime.datetime.utcnow()

      c_taf=requests.get('https://aviationweather.gov/adds/dataserver_current/httpparam?dataSource=tafs&requestType=retrieve&format=xml&stationString=KMWH&hoursBeforeNow=4')
      tafoutput = (c_taf.text)
      begin=tafoutput.find("Z ")
      end=tafoutput.find("</raw_text>")


      for idx, x in reversed(list(enumerate(walterbussettimes))):
        if (int(currentdatetime.strftime("%d%H%M")) > int(walterbussettimes[idx])):
          if (idx == len(walterbussettimes)-1):
            nextwalterbusartist="NONE"
            break
          else:
            nextwalterbusartist=walterbusartists[idx+1]
            nextwalterbussettime=walterbussettimes[idx+1]
            break
        elif (int(currentdatetime.strftime("%d%H%M")) < int(walterbussettimes[0])):
          nextwalterbusartist=walterbusartists[0]
          nextwalterbussettime=walterbussettimes[0]
          break
        else:
          continue

      for idx, x in reversed(list(enumerate(meadowsettimes))):
        if (int(currentdatetime.strftime("%d%H%M")) > int(meadowsettimes[idx])):
          if (idx == len(meadowsettimes)-1):
            nextmeadowartist="NONE"
            break
          else:
           nextmeadowartist=meadowartists[idx+1]
           nextmeadowsettime=meadowsettimes[idx+1]
           break
        elif (int(currentdatetime.strftime("%d%H%M")) < int(meadowsettimes[0])):
          nextmeadowartist=meadowartists[0]
          nextmeadowsettime=meadowsettimes[0]
          break
        else:
          continue

      for idx, x in reversed(list(enumerate(campsitesettimes))):
        if (int(currentdatetime.strftime("%d%H%M")) > int(campsitesettimes[idx])):
          if (idx == len(campsitesettimes)-1):
            nextcampsiteartist="NONE"
            break
          else:
           nextcampsiteartist=campsiteartists[idx+1]
           nextcampsitesettime=campsitesettimes[idx+1]
           break
        elif (int(currentdatetime.strftime("%d%H%M")) < int(campsitesettimes[0])):
          nextcampsiteartist=campsiteartists[0]
          nextcampsitesettime=campsitesettimes[0]
          break
        else:
          continue

      for idx, x in reversed(list(enumerate(shalasettimes))):
        if (int(currentdatetime.strftime("%d%H%M")) > int(shalasettimes[idx])):
          if (idx == len(shalasettimes)-1):
            nextshalaartist="NONE"
            break
          else:
           nextshalaartist=shalaartists[idx+1]
           nextshalasettime=shalasettimes[idx+1]
           break
        elif (int(currentdatetime.strftime("%d%H%M")) < int(shalasettimes[0])):
          nextshalaartist=shalaartists[0]
          nextshalasettime=shalasettimes[0]
          break
        else:
          continue

      for idx, x in reversed(list(enumerate(gorgesettimes))):
        if (int(currentdatetime.strftime("%d%H%M")) > int(gorgesettimes[idx])):
          if (idx == len(gorgesettimes)-1):
            nextgorgeartist="NONE"
            break
          else:
           nextgorgeartist=gorgeartists[idx+1]
           nextgorgesettime=gorgesettimes[idx+1]
           break
        elif (int(currentdatetime.strftime("%d%H%M")) < int(gorgesettimes[0])):
          nextgorgeartist=gorgeartists[0]
          nextgorgesettime=gorgesettimes[0]
          break
        else:
          continue

      combined = "GORGE TAF " + currentdatetime.strftime("%d%H%M") + "Z " + tafoutput[begin+2:end] + "\n\nREMARKS"
      if (nextwalterbusartist != "NONE"):
        combined+="\nWALTERBUS: FM" + nextwalterbussettime + " " + nextwalterbusartist
      if (nextmeadowartist != "NONE"):
        combined+="\nMEADOW: FM" + nextmeadowsettime + " " + nextmeadowartist
      if (nextcampsiteartist != "NONE"):
        combined+="\nCAMPSITE: FM" + nextcampsitesettime + " " + nextcampsiteartist
      if (nextshalaartist != "NONE"):
        combined+="\nSHALA: FM" + nextshalasettime + " " + nextshalaartist
      if (nextgorgeartist != "NONE"):
        combined+="\nAMPHI: FM" + nextgorgesettime + " " + nextgorgeartist
      await message.channel.send(combined)


client.run("")
