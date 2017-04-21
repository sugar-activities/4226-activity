; OurMusic (2009) for Sugar and Sugar-on-a-Stick - by Arthur B. Hunkins
; MyMusicASCII.csd - performed on 1 or more ASCII keyboards (no MIDI).

<CsoundSynthesizer>
<CsOptions>

-odac -+rtaudio=alsa -m0d --expression-opt -b128 -B2048

</CsOptions>
<CsInstruments>

sr      = 32000
ksmps   = 100
nchnls  = 2

        seed 0

gipan   chnexport "pan", 1
gkasc   chnexport "ascii", 1

gkpan   init 0
gkasc   init    0
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
        goto end
skip10:
        if (gkasc != 120) goto skip11
gkpan   =     -.4
        goto end
skip11:
        if (gkasc != 99) goto skip12
gkpan   =     -.3
        goto end
skip12:
        if (gkasc != 118) goto skip13
gkpan   =     -.2
        goto end
skip13:
        if (gkasc != 98) goto skip14
gkpan   =     -.1
        goto end
skip14:
        if (gkasc != 110) goto skip15
gkpan   =     .1
        goto end
skip15:
        if (gkasc != 109) goto skip16
gkpan   =     .2
        goto end
skip16:
        if (gkasc != 44) goto skip17
gkpan   =     .3
        goto end
skip17:
        if (gkasc != 46) goto skip18
gkpan   =     .4
        goto end
skip18:
        if (gkasc != 47) goto skip19
gkpan   =     .5
        goto end
skip19:
        if (gkasc != 45) goto end
gkoff   =     1
end:
gkasc	=     0
	
        endin

	instr 2, 3, 4, 5, 6, 7, 8, 9

k1      init       0
indx    =          p1 - 2
        if p1 != gkinst goto skip
ktime   =          gktime
k1      =          (k1 == 0? 1: 0)
skip:
        if gkoff == 0 goto skip2
k1      =          0
ktime   =          gktime
skip2:
kamp2   lineto     k1, ktime
kamp    table      kamp2 * 512, 1
kamp	  =	       (kamp2 < .007? 0: kamp)
kamp    port       kamp, .01
ktrig   trigger    kamp2, .01, 0
        if ktrig == 0 goto skip3
        if gipan == 1 goto skip4
kpan    rnd31      .5, .7
kpan    =          (p1 > 2? kpan: 0)
gkpan   =          kpan
	  kgoto skip3
skip4:
gkpan   =          (p1 == 2? 0: gkpan)
kpan    =          gkpan
skip3:        
kmod2   rspline    1.4, 2, 1.5, 2.5
kmod    rspline    .85, 1, 20, 25
kfreq   jspline    .25, 1, 2
kpw     jspline    p7, 1, 2
aout    vco2       p4 * kamp * kmod * kmod2, 440 + kfreq, p5, p6 + kpw 
kamp2   port       kamp2, .01
a1,a2,a3,a4 pan    aout, .5 + (kamp2 * kpan), 1, 2, 1
        outs       a1 - (.02 * a2), a2 - (.02 * a1)
   
        endin

</CsInstruments>

<CsScore>

f1 0 512 16 1 511 2.2 1000
f2 0 8193 7 0 8193 1
i1 0 3600
i2 0 3600 6000 4 .5 .015
i3 0 3600 3000 4 .7 .02
i4 0 3600 4200 4 .8 .017
i5 0 3600 2000 4 .95 .01
i6 0 3600 1300 2 .6 .02
i7 0 3600 1500 2 .7 .02
i8 0 3600 2100 2 .8 .02
i9 0 3600 2200 2 .95 .014

e

</CsScore>
</CsoundSynthesizer>
