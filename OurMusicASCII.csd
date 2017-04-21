; OurMusic (2009) for Sugar and Sugar-on-a-Stick - by Arthur B. Hunkins
; OurMusicASCII.csd - performed on 1 or more ASCII keyboards (no MIDI).

<CsoundSynthesizer>
<CsOptions>

-odac -+rtaudio=alsa -m0d --expression-opt -b128 -B2048

</CsOptions>
<CsInstruments>

sr      = 32000
ksmps   = 100
nchnls  = 2

        seed 0

giharm  chnexport "harm", 1
gipan   chnexport "pan", 1
gidepth chnexport "depth", 1
gkasc   chnexport "ascii", 1

ga1     init 0
ga2     init 0
gkpan   init 0
gkasc   init    0
gkharm  init    1
gkdepth init    0
gktime  init    6

	instr 1

gkoff   =       0
        if gkasc > 0 goto next
gkinst  =       0
        kgoto end
next:        
	  if ((gkasc < 48) || (gkasc > 57)) goto skip
gktime  =     gkasc - 48
gktime  =     (gkasc == 48? gktime + 10: gktime)
        kgoto end
skip:
        if (gkasc != 113) goto skip2
gkinst  =     2
        kgoto end
skip2:
        if (gkasc != 119) goto skip3
gkinst  =     3
        kgoto end
skip3:
        if (gkasc != 101) goto skip4
gkinst  =     4
        kgoto end
skip4:
        if (gkasc != 114) goto skip5
gkinst  =     5
        kgoto end
skip5:
        if (gkasc != 116) goto skip6
gkinst  =     6
        kgoto end
skip6:
        if (gkasc != 121) goto skip7
gkinst  =     7
        kgoto end
skip7:
        if (gkasc != 117) goto skip8
gkinst  =     8
        kgoto end
skip8:
        if (gkasc != 105) goto skip9
gkinst  =     9
        kgoto end
skip9:
	  if gipan == 0 goto skip19
        if (gkasc != 122) goto skip10
gkpan   =     -.5
        kgoto end
skip10:
        if (gkasc != 120) goto skip11
gkpan   =     -.4
        kgoto end
skip11:
        if (gkasc != 99) goto skip12
gkpan   =     -.3
        kgoto end
skip12:
        if (gkasc != 118) goto skip13
gkpan   =     -.2
        kgoto end
skip13:
        if (gkasc != 98) goto skip14
gkpan   =     -.1
        kgoto end
skip14:
        if (gkasc != 110) goto skip15
gkpan   =     .1
        kgoto end
skip15:
        if (gkasc != 109) goto skip16
gkpan   =     .2
        kgoto end
skip16:
        if (gkasc != 44) goto skip17
gkpan   =     .3
        kgoto end
skip17:
        if (gkasc != 46) goto skip18
gkpan   =     .4
        kgoto end
skip18:
        if (gkasc != 47) goto skip19
gkpan   =     .5
        kgoto end
skip19:
        if (gkasc != 45) goto skip20
gkoff   =     1
	  kgoto end
skip20:
	  if giharm < 2 goto skip30
        if (gkasc != 97) goto skip21
gkharm  =     1
        kgoto end                
skip21:
        if (gkasc != 115) goto skip22
gkharm  =     2
        kgoto end                
skip22:
        if (gkasc != 100) goto skip23
gkharm  =     3
        kgoto end                
skip23:
        if (gkasc != 102) goto skip24
gkharm  =     4
        kgoto end                
skip24:
        if (gkasc != 103) goto skip25
gkharm  =     5
        kgoto end                
skip25:
        if (gkasc != 104) goto skip26
gkharm  =     6
        kgoto end                
skip26:
        if (gkasc != 106) goto skip27
gkharm  =     7
        kgoto end                
skip27:
        if (gkasc != 107) goto skip28
gkharm  =     8
        kgoto end                
skip28:
        if (gkasc != 108) goto skip29
gkharm  =     9
        kgoto end                
skip29:
        if (gkasc != 59) goto skip30
gkharm  =     10
        kgoto end                
skip30:
	  if gidepth < 2 goto end
        if (gkasc != 33) goto skip31
gkdepth =     .1
        goto end                
skip31:
        if (gkasc != 64) goto skip32
gkdepth =     .2
        goto end                
skip32:
        if (gkasc != 35) goto skip33
gkdepth =     .3
        goto end                
skip33:
        if (gkasc != 36) goto skip34
gkdepth =     .4
        goto end                
skip34:
        if (gkasc != 37) goto skip35
gkdepth =     .5
        goto end                
skip35:
        if (gkasc != 94) goto skip36
gkdepth =     .6
        goto end                
skip36:
        if (gkasc != 38) goto skip37
gkdepth =     .7
        goto end                
skip37:
        if (gkasc != 42) goto skip38
gkdepth =     .8
        goto end                
skip38:
        if (gkasc != 40) goto skip39
gkdepth =     .9
        goto end                
skip39:
        if ((gkasc != 41) && (gkasc != 96) && (gkasc != 126)) goto end
gkdepth =     0
end:
gkasc	  =     0
	
        endin

	instr 2, 3, 4, 5, 6, 7, 8, 9

        if (gidepth == 0) || (p1 > 2) goto skip
        event_i   "i", 10, 0, 3600
skip:
k1      init       0
kold    init       0
indx    =          p1 - 2
        if p1 != gkinst goto skip2
ktime   =          gktime
k1      =          (k1 == 0? 1: 0)
skip2:
        if gkoff == 0 goto skip3
k1      =          0
ktime   =          gktime
skip3:
kamp2   lineto     k1, ktime
kamp    table      kamp2 * 512, 1
kamp	  =	       (kamp2 < .007? 0: kamp)
kamp    port       kamp, .01
ktrig   trigger    kamp2, .01, 0
        if ktrig == 0 goto skip4
        if giharm == 1 goto back
        if giharm == 2 goto skip5
imult   tab_i      indx, 3
kmult   =          imult
        kgoto skip6
back:
kmult   random     1, 10.99
kmult   =          (p1 == 2? 1: int(kmult))
        if (kmult == kold) && (p1 > 2) goto back
kold    =          kmult
        kgoto skip6
skip5:
kmult   =          (p1 == 2? 1: gkharm)
skip6:
        if gipan == 1 goto skip7
kpan    rnd31      .5, .7
kpan    =          (p1 > 2? kpan: 0)
gkpan   =          kpan
	  kgoto skip8
skip7:
gkpan   =          (p1 == 2? 0: gkpan)
kpan    =          gkpan
skip8:
        if gidepth == 0 goto skip4
	  if gidepth == 1 goto skip10
gkdepth =          (p1 == 2? 0: gkdepth)
kdepth  =          gkdepth
	  kgoto skip4
skip10:
kdepth  unirand    .9
kdepth  =          (p1 == 2? 0: kdepth)
gkdepth =          kdepth
skip4:        
kmod2   rspline    1.4, 2, 1.5, 2.5
kmod    rspline    .85, 1, 20, 25
kfreq   jspline    .25, 1, 2
kpw     jspline    p7, 1, 2
        if (gidepth == 0) || (p1 == 2) goto skip11
kamp	  =    	 kamp * (1 - (kdepth * .3))
skip11:
aout    vco2       p4 * kamp * kmod * kmod2, (kmult * 55) + kfreq, p5, p6 + kpw 
kamp2   port       kamp2, .01
a1,a2,a3,a4 pan    aout, .5 + (kamp2 * kpan), 1, 2, 1
        if (gidepth == 0) || (p1 == 2) goto skip12
ga1     =          ga1 + (a1 * kdepth)    
ga2     =          ga2 + (a2 * kdepth)    
a1a     =          a1 * (1 - kdepth)
a2a     =          a2 * (1 - kdepth)
        outs       a1a - (.02 * a2a), a2a - (.02 * a1a)
        goto fin            
skip12:
        outs       a1 - (.02 * a2), a2 - (.02 * a1)
   
fin:    endin

        instr 10
        
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
i1 0 3600
i2 0 3600 6000 4 .5 .015
i3 0 3600 800 2 .6 .02
i4 0 3600 1400 2 .7 .02
i5 0 3600 1400 2 .8 .02
i6 0 3600 3100 4 .6 .028
i7 0 3600 3500 4 .7 .028
i8 0 3600 2800 4 .8 .028
i9 0 3600 2400 4 .9 .028

e

</CsScore>
</CsoundSynthesizer>
