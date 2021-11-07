from mido import MidiFile
import mido
import glob
import os

#outport = mido.open_output()
 
for file in glob.glob("./Data/Songs/*.midi"):
    mid = mido.MidiFile(file)
    try:
        track = mid.tracks[4]
    except IndexError:
        continue
    iTime = 0
    stopTime = 0
    i=0
    idxMel = 0
    timing = []
    currentnode=[]
   
    for i in range(0,len(track)):
        if(track[i].type == 'note_on'):
            currentnode.append(track[i].note % 12)
            iTime= track[i].time
            i +=1
            for i in range(i, len(track)):
               
                iTime = iTime + track[i].time
                if track[i].type == 'note_on':
                    break
                 
                      
            timing.append(iTime)
            
    
    timing2 = timing
   
    BigstopTime=0
    BigstartTime=0
    idxMel =[0, 0, 0, 0, 0]
   
    for timingIndex in range(0,len(timing2)):
        timing = timing2[timingIndex]
        mid2 = mido.MidiFile()
        print("Starting song")
        try:
            for k in range(1,5):
                melTrack = mid.tracks[k]
                stopTime=BigstopTime
                startTime=BigstartTime
                t = mido.MidiTrack()
                mid2.tracks.append(t)
               
                stopTime = timing
                if timingIndex == 0:
                    startTime = 0
                else:
                    startTime = timing2[timingIndex-1]
                if timingIndex == len(timing2):
                    for j in range(idxMel[k], len(melTrack)):
                        t.append(melTrack[j])
                      
            
                else:
                    while startTime<stopTime:
                        t.append(melTrack[idxMel[k]])
                        startTime = startTime + melTrack[idxMel[k]].time
                        idxMel[k] +=1
        except:
            continue
        BigstopTime=stopTime
        BigstartTime = startTime
        if not os.path.exists('./Data/' + str(currentnode[timingIndex]) + str("/")):
            os.makedirs('./Data/' + str(currentnode[timingIndex]) + str("/"))
        path = './Data/' + str(currentnode[timingIndex]) + str("/")  + file.replace("./Data/Songs/", "")
        print(f"SAVING {path}")   
        mid2.save(path)

print("Done")