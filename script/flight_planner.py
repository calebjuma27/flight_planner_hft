#Creation of a flight Planning tool

# Author:      Caleb juma
# Tool:        Flight planning tool
# Created:     17-09-2019
# Copyright:   (c) juma 2019
# Licence:     <Academic DEMO>
#-------------------------------------------------------------------------------
from tkinter import *
import os
from math import ceil
from math import sqrt
LARGE_FONT= ('Bodoni MT Black', 12)
Font1=('Copperplate Gothic Bold',11)
Font2=('Times New Roman',12)


##backend
def Calculate():
    ms=float(Entry.get(Ise)) #image scale
    fL=float(Entry.get(cfe))#focal length
    q=(float(Entry.get(sope)))/100# Side overlap and making it into a decimal
    p=(float(Entry.get(fope)))/100# forward overlap and making it into a decimal
    v=float(Entry.get(Ase))# speed of aircraft
    ns=(float(Entry.get(NSe)))*1000# North south length in km
    ew=(float(Entry.get(EWe)))*1000# East west length in km
    Uns=float(Entry.get(Ushe))# unsharpness
    HG=float(Entry.get(HGe))# mountain top height
    HTv=float(Entry.get(HTve))# valley bottom height
    HK=float(Entry.get(HKe))# height of Church


    fh=round((fL*ms)/1000) #flying height in metres
    stripsizeI=23*(1-q) #in image in centimetres
    stripsizeG=(stripsizeI*ms)/100 # on ground in metres
    nofstrip=ceil(ns/stripsizeG) # rounding it up

    mbase=(((1-p)*23)*ms)/100 #modelbase in metres
    nofmodels=ceil(ew/mbase)# number of models per strip rounded to up
    nofphotos=nofmodels+1 #number of photos per strip
    Ls=round((nofmodels*mbase),2) #length of 1 strip in metres
    fd=(Ls*nofstrip)# flying distance in metres
    t=round((fd/1000)/v,3)#time of flight

    nta=round((mbase*stripsizeG)/1000000,3) #net terrain area in sqkm
    gta=round(((((p*23)*ms)/100)*((23*ms)/100))/1000000,3) #gross terrain area in sqkm

    #480 exposures=120m=1 film roll, 1 exposure=0.25m
    tnofmodels=round(nofmodels*nofstrip) #total no of models
    tnofphotos=round(nofphotos*nofstrip) #total no of photos
    Lof=round((tnofphotos*0.25),2) #length of film
    fr=round(Lof/120,2)# filmroll needed

    #time between expoures
    vmet=(v*1000)/3600#speed in m/s
    te=round(mbase*(1/vmet),3) #te is time between exposures

    #exposure time to restrict unsharpness
    Tau=(1/(vmet*1000000))*Uns*ms


    #scale at valley top
    #height of mt above sea level=HG
    #height of valley bottom in relation to sea level=HT
    fhM=fh+HG #flying height at mountain top
    fhV=fhM-HTv
    MT=round(1/(fL/(fhV*1000)),3)

    #forward overlap of valley bottom in relation to mountain top
    PV=round((1-(mbase/((23*MT)/100)))*100,3)

    #relief displacement
    drGr=(((fh/1000)* sqrt(13))/((fh/1000)-(HK/1000)))-sqrt(13)#on ground in kilometres
    dr=round((drGr/ms)*1000000,4) #on photo in mm

    #dr for SWA (camera constant or focal length 8.85cm)
    #using flying height fh
    newms=1/(0.0885/fh)
    drw1=round((drGr/newms)*1000000,4) #on photo in mm

    #using image scale ms
    newfh=ms*0.0885
    newdrGR=(((newfh/1000)*sqrt(13))/((newfh/1000)-(HK/1000)))-sqrt(13)#on ground in kilometres
    drw2=round((newdrGR/ms)*1000000,2) #on photo in mm

    #Acceptable Terrain differences dh at corners with tolerance o.2 mm
    #distance to image corner is a half the diagonal of a 23by23cm photo
    #using scale newfh
    DistE=ms*((sqrt((23**2)+(23**2)))/2)#dist to image corner in cm
    # will have to add the distance to corner to specified tolerance
    Adr=ms*(0.2/1000000)#acceptable tolerance on ground in km
    Adr2=DistE/100000# distance to image corner on ground in km
    dh=round(((newfh/1000)-((newfh/1000)*Adr2)/(Adr2+Adr))*1000,4) #Acceptable terrain displacement in m


    ##inserting answers into window(and also deletting previous entries)

    Entry.delete(fhe,0,END)
    Entry.insert(fhe,0,fh)


    Entry.delete(fte,0,END)
    Entry.insert(fte,0,t)

    Entry.delete(nstripe,0,END)
    Entry.insert(nstripe,0,nofstrip)

    Entry.delete(nphotose,0,END)
    Entry.insert(nphotose,0,nofphotos)

    Entry.delete(nmodelse,0,END)
    Entry.insert(nmodelse,0,nofmodels)

    Entry.delete(tfpe,0,END)
    Entry.insert(tfpe,0,fd)

    Entry.delete(ntge,0,END)
    Entry.insert(ntge,0,nta)


    Entry.delete(gtge,0,END)
    Entry.insert(gtge,0,gta)

    Entry.delete(fme,0,END)
    Entry.insert(fme,0,Lof)

    Entry.delete(texe,0,END)
    Entry.insert(texe,0,te)

    Entry.delete(taue,0,END)
    Entry.insert(taue,0,Tau)

    Entry.delete(MTe,0,END)
    Entry.insert(MTe,0,MT)

    Entry.delete(PVe,0,END)
    Entry.insert(PVe,0,PV)

    Entry.delete(dre,0,END)
    Entry.insert(dre,0,dr)

    Entry.delete(drw1e,0,END)
    Entry.insert(drw1e,0,drw1)

    Entry.delete(drw2e,0,END)
    Entry.insert(drw2e,0,drw2)

    Entry.delete(dhe,0,END)
    Entry.insert(dhe,0,dh)




#Frontend

window=Tk()
window.title('FLIGHT PLANNER')

#labels
heading=Label(window, text='INPUT',font=LARGE_FONT).grid(row=1,column=2)
##Aoi=Label(window, text='',).grid(row=1,column=0)
NS=Label(window, text='North-South length').grid(row=2,column=0)
NSunits=Label(window, text='Kilometres').grid(row=2,column=2)
EW=Label(window, text='East-West length (Flight direction)').grid(row=3,column=0)
EWunits=Label(window, text='Kilometres').grid(row=3,column=2)

Is=Label(window, text='Image Scale (MB)     1: ').grid(row=5,column=0)#Image scale
cf=Label(window, text='Camera Focal Length').grid(row=6,column=0)# Camera focal length
cfunits=Label(window, text='millimetres').grid(row=6,column=2)

##Op=Label(window, text='').grid(row=8,column=0)
fop=Label(window, text='Forward Overlap').grid(row=8,column=0) #forward overlap
fopunits=Label(window, text='%').grid(row=8,column=2)
sop=Label(window, text='Side Overlap').grid(row=9,column=0) #side overlap
sopunits=Label(window, text='%').grid(row=9,column=2)

As=Label(window, text='aircraft speed (V)').grid(row=10,column=0)
Asunits=Label(window, text='Km/hr').grid(row=10,column=2)

Ush=Label(window, text='Unsharpness (d)').grid(row=2,column=4)
Ushunits=Label(window, text='micrometres').grid(row=2,column=6)

HeigtM=Label(window, text='Mountain top (HG)').grid(row=3,column=4)
HeightMunits=Label(window, text='metres').grid(row=3,column=6)

Heightv=Label(window, text='Valley bottom (HT)').grid(row=4,column=4)
Heightvunits=Label(window, text='metres').grid(row=4,column=6)

HeightK=Label(window, text='Church Tower (HK)').grid(row=5,column=4)
HeightKunits=Label(window, text='metres').grid(row=5,column=6)

Note=Label(window, text="UNLESS OTHERWISE STATED:",font=Font2).grid(row=7,column=5)
Note1=Label(window, text="Camera constant c= 153 mm:",font=Font1).grid(row=8,column=5)
Note2=Label(window, text="image dimensions s= 23cm by 23cm",font=Font1).grid(row=9,column=5)

#entries
NSe=Entry(window, bd=5)
NSe.grid(row=2,column=1)

EWe=Entry(window, bd=5)
EWe.grid(row=3,column=1)

Ise=Entry(window,bd=5)
Ise.grid(row=5, column=1)

cfe=Entry(window,bd=5)
cfe.grid(row=6,column=1)

fope=Entry(window,bd=5)
fope.grid(row=8,column=1)

sope=Entry(window,bd=5)
sope.grid(row=9, column=1)

Ase=Entry(window, bd=5)
Ase.grid(row=10, column=1)

Ushe=Entry(window, bd=5)
Ushe.grid(row=2, column=5)

HGe=Entry(window, bd=5)
HGe.grid(row=3, column=5)

HTve=Entry(window, bd=5)
HTve.grid(row=4, column=5)

HKe=Entry(window, bd=5)
HKe.grid(row=5, column=5)

blank=Label(window,text='',).grid(row=13,column=0)

ans=Button(window, text='Calculate', command=Calculate).grid(row=14,column=2)

blank2=Label(window,text='',).grid(row=15,column=0)



#####Results
resultss=Label(window, text='RESULT',font=LARGE_FONT,).grid(row=16, column=2)
fh=Label(window, text='Relative Flying Height (hg)',).grid(row=17,column=0)
fhunits=Label(window, text='metres').grid(row=17,column=2)
nstrip=Label(window, text='Number of Strips (n)',).grid(row=18, column=0)

nmodels=Label(window, text='Number of Models per strip (M)',).grid(row=19, column=0)
nphotos=Label(window, text='Number of Images per strip (A)',).grid(row=20, column=0)


tfp=Label(window, text='length of flight path without turns (L)',).grid(row=21, column=0)
tfpunits=Label(window, text='metres').grid(row=21,column=2)

ft=Label(window, text='Net Flying time (T)',).grid(row=22,column=0)
ftunits=Label(window, text='hrs').grid(row=22,column=2)

ntg=Label(window, text='Net area per model (FN)',).grid(row=23, column=0)
ntgunits=Label(window, text='sqKm').grid(row=23,column=2)
gtg=Label(window, text='Gross area per model (FG)',).grid(row=24, column=0)
gtgunits=Label(window, text='sqKm').grid(row=24,column=2)

fm=Label(window, text='length of film (FL)',).grid(row=25, column=0)
fmunits=Label(window, text='metres').grid(row=25,column=2)

tex=Label(window, text='Time btw exposures (TE)',).grid(row=26, column=0)
texunits=Label(window, text='seconds').grid(row=26,column=2)

Taug=Label(window, text='Time during Exposure (Tau)').grid(row=17,column=4)
Taugunits=Label(window, text='seconds').grid(row=17,column=6)

MTg=Label(window, text='Image Scale (MT)     1: ').grid(row=18,column=4)

PVg=Label(window, text='Forward Overlap (PV)').grid(row=19,column=4)
PVgunits=Label(window, text='%').grid(row=19,column=6)

drg=Label(window, text='Relief Displacement (dr)').grid(row=21,column=4)
drgunits=Label(window, text='milimetres').grid(row=21,column=6)

drw1g=Label(window, text='Relief Displacement SWA (drw1)').grid(row=22,column=4)
drw1gunits=Label(window, text='milimetres').grid(row=22,column=6)

drw2g=Label(window, text='Relief Displacement SWA (drw2)').grid(row=23,column=4)
drw2gunits=Label(window, text='milimetres').grid(row=23,column=6)

dhg=Label(window, text='Acceptable terrain height diff (dh)').grid(row=24,column=4)
dhgunits=Label(window, text='metres').grid(row=24,column=6)

end=Label(window,text="",).grid(row=37,column=0)


#computed entries
fhe=Entry(window,bd=5,)
fhe.grid(row=17,column=1)


nstripe=Entry(window,bd=5)
nstripe.grid(row=18,column=1)

nmodelse=Entry(window,bd=5)
nmodelse.grid(row=19,column=1)

nphotose=Entry(window,bd=5)
nphotose.grid(row=20,column=1)

tfpe=Entry(window,bd=5)
tfpe.grid(row=21,column=1)

fte=Entry(window, bd=5)
fte.grid(row=22,column=1)


ntge=Entry(window,bd=5)
ntge.grid(row=23,column=1)

gtge=Entry(window,bd=5)
gtge.grid(row=24,column=1)

fme=Entry(window,bd=5)
fme.grid(row=25,column=1)

texe=Entry(window,bd=5)
texe.grid(row=26,column=1)


taue=Entry(window,bd=5)
taue.grid(row=17,column=5)

MTe=Entry(window,bd=5)
MTe.grid(row=18,column=5)

PVe=Entry(window,bd=5)
PVe.grid(row=19,column=5)

dre=Entry(window,bd=5)
dre.grid(row=21,column=5)

drw1e=Entry(window,bd=5)
drw1e.grid(row=22,column=5)

drw2e=Entry(window,bd=5)
drw2e.grid(row=23,column=5)

dhe=Entry(window,bd=5)
dhe.grid(row=24,column=5)


window.mainloop()


