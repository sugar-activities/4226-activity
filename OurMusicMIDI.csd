; OurMusic (2009) for Sugar and Sugar-on-a-Stick - by Arthur B. Hunkins
; OurMusicMIDI.csd - requires MIDI device with 8 - 11 pots/sliders,
;  alternatively, 8 - 10 pots/sliders with 10 MIDI notes

<CsoundSynthesizer>
<CsOptions>

-odac -+rtaudio=alsa -+rtmidi=alsa -M hw:1,0 -m0d --expression-opt -b128 -B2048 -+raw_controller_mode=1

</CsOptions>
<CsInstruments>

sr      = 32000
ksmps   = 100
nchnls  = 2

        massign 0, 0
        seed 0

gichan  chnexport "chan", 1
gictrl1 chnexport "ctrl", 1
giharm  chnexport "harm", 1
gihctrl chnexport "harctrl", 1
gihmidi chnexport "harmidi", 1
gipan   chnexport "pan", 1
gipctrl chnexport "panctrl", 1
gidepth chnexport "depth", 1
gidctrl chnexport "depctrl", 1

ga1     init 0
ga2     init 0
gkharm  init 1

	instr 1, 2, 3, 4, 5, 6, 7, 8

        if (gidepth == 0) || (p1 > 1) goto skip
        event_i "i", 9, 0, 3600
skip:
        if (giharm != 3) || (p1 > 1) || (gichan == 0) goto skip2
kstat,kchan,kd1,kd2 midiin
        if kchan != gichan goto skip2                                 
        if ((kstat != 144) || (kd2 == 0)) goto skip2
	  if ((kd1 < gihmidi) || (kd1 > (gihmidi + 9))) goto skip2
gkharm  =          kd1 - gihmidi + 1
skip2:
kpan    init       0
kold    init       0
indx    =          p1 - 1
ictrl   =          gictrl1 + indx
kamp2   ctrl7      (gichan > 0? gichan: p1), (gichan > 0? ictrl: 7), 0, 1
kamp    table      kamp2 * 512, 1
kamp	  =	       (kamp2 == 0? 0: kamp)
kamp    port       kamp, .01
ktrig   trigger    kamp2, .01, 0
        if ktrig == 0 goto skip3
        if giharm == 1 goto back
        if giharm == 2 goto skip4
        if giharm == 3 goto skip5
imult   tab_i      indx, 3
kmult   =          imult
        kgoto skip6
back:
kmult   random     1, 10.99
kmult   =          (p1 == 1? 1: int(kmult))
        if (kmult == kold) && (p1 > 1) goto back
kold    =          kmult
        kgoto skip6
skip4:
kmult   ctrl7      (gichan > 0? gichan: 9), (gichan > 0? gihctrl: 7), 1, 10.99
kmult   =          (p1 == 1? 1: int(kmult))
        kgoto skip6
skip5:
kmult   =          (p1 == 1? 1: gkharm)
gkharm  =          kmult
skip6:
        if gipan == 1 goto skip7
kpan    rnd31      .5, .7
kpan    =          (p1 > 1? kpan: 0)
	  kgoto skip8
skip7:
gkpan   ctrl7      (gichan > 0? gichan: 10), (gichan > 0? gipctrl: 7), -.5, .5
        if p1 > 1 goto skip9
kpan    =          0
gkpan2  =          gkpan
gkflag  =          1
        kgoto skip8
skip9:
kpan    =          (((gkpan2 == gkpan) && (gkflag == 1))? 0: gkpan) 
gkpan2  =          gkpan
gkflag  =          (kpan == 0? 1: 0)
skip8:
        if gidepth == 0 goto skip3
	  if gidepth == 1 goto skip10
gkdepth ctrl7      (gichan > 0? gichan: 11), (gichan > 0? gidctrl: 7), 0, .9
        if p1 > 1 goto skip11
kdepth  =          0
gkdep2  =          gkdepth
gkflag2 =          1
        kgoto skip3
skip11:
kdepth  =          (((gkdep2 == gkdepth) && (gkflag2 == 1))? 0: gkdepth) 
gkdep2  =          gkdepth
gkflag2 =          (kdepth == 0? 1: 0)
	  kgoto skip3
skip10:
kdepth  unirand    .9
kdepth  =          (p1 > 1? kdepth: 0)
skip3:        
kmod2   rspline    1.4, 2, 1.5, 2.5
kmod    rspline    .85, 1, 20, 25
kfreq   jspline    .25, 1, 2
kpw     jspline    p7, 1, 2
        if (gidepth == 0) || (p1 == 1) goto skip12
kamp	  =    	 kamp * (1 - (kdepth * .3))
skip12:
aout    vco2       p4 * kamp * kmod * kmod2, (kmult * 55) + (p1 > 1? kfreq: 0), p5, p6 + kpw 
kamp2   port       kamp2, .01
a1,a2,a3,a4 pan    aout, .5 + (kamp2 * kpan), 1, 2, 1
        if (gidepth == 0) || (p1 == 1) goto skip13
ga1     =          ga1 + (a1 * kdepth)    
ga2     =          ga2 + (a2 * kdepth)    
a1a     =          a1 * (1 - kdepth)
a2a     =          a2 * (1 - kdepth)
        outs       a1a - (.02 * a2a), a2a - (.02 * a1a)
        goto fin            
skip13:
        outs       a1 - (.02 * a2), a2 - (.02 * a1)
   
fin:    endin

        instr 9
        
aL, aR  reverbsc   ga1, ga2, .95, 800, sr, .25
        outs       aL * .4, aR * .4
        
ga1     =    0
ga2     =    0

        endin

</CsInstruments>

<CsScore>

f1 0 512 16 1 511 2.2 1000
f2 0 8193 7 0 8193 1
f3 0 8 -2 1 2 3 5 7 8 9 10 
i1 0 3600 6000 4 .5 .015
i2 0 3600 800 2 .6 .02
i3 0 3600 1400 2 .7 .02
i4 0 3600 1400 2 .8 .02
i5 0 3600 3100 4 .6 .028
i6 0 3600 3500 4 .7 .028
i7 0 3600 2800 4 .8 .028
i8 0 3600 2400 4 .9 .028

e

</CsScore>
</CsoundSynthesizer>
