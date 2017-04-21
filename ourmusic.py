# OUR MUSIC - Sonic Environments for Children (2009)
# Art Hunkins (www.arthunkins.com)
#   
#    OurMusic is licensed under the Creative Commons Attribution-Share
#    Alike 3.0 Unported License. To view a copy of this license, visit
#    http://creativecommons.org/licenses/by-sa/3.0/ or send a letter to
#    Creative Commons, 171 Second Street, Suite 300, San Francisco,
#    California, 94105, USA.
#
#    It is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# version 7  11/3/11  Cosmetic change only
#
#    Notes:
#
#    Of the four Versions of OurMusic, 1 and 2 are similar, as are 3
#    and 4. The only significant difference is the control mechanism;
#    2 and 4 are played solely on ASCII keyboard(s) (multiple  keyboards;
#    the native and additional USB keyboards can be played simultaneously).
#    Collaborative performance is encouraged. Versions 3/4 are somewhat
#    more involved than 1/2; their textures are richer and they offer
#    enhanced options.
#
#    Versions 1 and 3 require a USB MIDI controller with 8+ knobs
#    and/or sliders. The 8 knobs/sliders must have *contiguous* controller
#    #'s, or all be continuous controller 7 on channels 1-8(11). Please note
#    with respect to the latter arrangement: in MyMusicMIDI, pan (if actively
#    controlled) is on channel 9; in OurMusicMIDI, *harmonics* are assigned
#    channel 9; pan, channel 10; and depth, channel 11 (these assignments are
#    fixed). When "MIDI notes" is selected to control harmonics with this
#    option, the "harmonics channel" is thus actually #9. 
#
#    Important: The controller must be attached AFTER boot, and BEFORE
#    the version is selected. It is assumed that the controller is a USB
#    device. The inexpensive Korg nanoKontrol is one appropriate
#    controller choice; it can nicely handle either 8- or 9-slider
#    renditions (but not those requiring more than 9 sliders). Choose
#    Scene 4 on the Korg, and Channel "0" in the performance window.
#
#    If you get audio glitching, open Sugar's Control Panel, and turn off
#    Extreme power management (under Power) or Wireless radio (under
#    Network). Stereo headphones (an inexpensive set will work fine) or
#    external amplifier/speaker system are highly recommended.
#
#    The font display of this activity can be resized in csndsugui.py,
#    using any text editor. Further instructions are found toward the
#    beginning of csndsugui.py.

import csndsugui
from sugar.activity import activity
import gtk
import os

class OurMusic(activity.Activity):

 def __init__(self, handle):
  
   activity.Activity.__init__(self, handle)

   red = (0xDDDD, 0, 0)
   brown = (0x6600, 0, 0)
   green = (0, 0x5500, 0)

   win = csndsugui.CsoundGUI(self)
   width = gtk.gdk.screen_width()
   height = gtk.gdk.screen_height()
   if os.path.exists("/etc/olpc-release") or os.path.exists("/sys/power/olpc-pm"):
     tall = 1
     adjust = 78
   else:
     adjust = 57
     if (height * 1.35) > width:
       tall = 1
     else:
       tall = 0
   screen = win.box()
   screen.set_size_request(width, height - adjust)
   scrolled = gtk.ScrolledWindow()
   scrolled.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
   screen.pack_start(scrolled)
   all = gtk.VBox()
   all.show()
   scrolled.add_with_viewport(all)
   scrolled.show()

   win.text("<big><b><big><u>OUR MUSIC</u> - Sonic Environments for Children \
(2009)</big></b>\n\
                           Art Hunkins (www.arthunkins.com)</big>", all)

   if tall:
     win.text("A Creation Story:\n\
<i>      On the sixth day I was created.\n\
         God said I was very good.\n\
      On the sixth day We were created - my friends and I.\n\
         God said We were very good.\n\
      On the sixth day my Family was created - my loved ones and I,\n\
            together with all the other creatures.\n\
         God said my Family was very good.\n\
      God saw that everything He made was very good.\n\
      He was so pleased He decided to take a holiday,\n\
            and joined us in play.</i>", all, green)
   else:
     win.text("<small><b>A Creation Story:</b>  <i>On the sixth day I was created. \
God said I was very good.\n\
  On the sixth day We were created - my friends and I. \
God said We were very good.\n\
  On the sixth day my Family was created - my loved ones and I, \
together with all the other creatures. \
God said my Family was very good.\n\
  God saw that everything He made was very good. \
He was so pleased He decided to take a holiday, \
and joined us in play.</i></small>", all, green)

   win.text("\
<b>1 - MyMusicMIDI</b>  Simple; MIDI controller with 8-9 knobs/sliders\n\
<b>2 - MyMusicASCII</b>  Simple; 1 or more ASCII keyboards\n\
<b>3 - OurMusicMIDI</b>  \
Advanced; MIDI controller with 8-11 knobs/sliders, or 8-10 \
knobs/sliders and 10 MIDI notes\n\
<b>4 - OurMusicASCII</b>  Advanced; 1 or more ASCII keyboards\n\
<i><b>MIDI</b>: plug in controller AFTER boot &amp; BEFORE selecting; \
zero controls before start.  \
<b>ASCII</b>: press keys AFTER start.</i>", all, brown)
   nbox = win.box(False, all)
   win.text("", nbox)
   but1 = win.cbbutton(nbox, self.version1, " 1 MyMusicMIDI ")
   but1.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(0, 0x7700, 0))
   but1.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.Color(0, 0x7700, 0))
   but2 = win.cbbutton(nbox, self.version2, " 2 MyMusicASCII")
   but2.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(0, 0x7700, 0))
   but2.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.Color(0, 0x7700, 0))
   but3 = win.cbbutton(nbox, self.version3, "3 OurMusicMIDI ")
   but3.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(0, 0x7700, 0))
   but3.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.Color(0, 0x7700, 0))
   but4 = win.cbbutton(nbox, self.version4, "4 OurMusicASCII")
   but4.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(0, 0x7700, 0))
   but4.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.Color(0, 0x7700, 0))
   win.text("  <b>MIDI DEVICE REQUIRED</b> for 1 &amp; 3", nbox, brown)
   bbox = win.box(False, all)
   self.bb = bbox
   self.w = win
   self.r = red
   self.g = green
   self.br = brown
   self.ver = 0

 def onKeyPress(self, widget, event):
   if (self.p):
     if (self.ver == 2) or (self.ver == 4):
       self.w.set_channel("ascii", event.keyval)
       if event.hardware_keycode == 82:
         self.w.set_channel("ascii", 45)

 def playcsd(self, widget):
   if self.p == False:
     self.p = True
     self.w.play()
     self.but.child.set_label("STOP !")
     self.but.child.set_use_markup(True)
     self.but.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(0xFFFF, 0, 0))
     self.but.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.Color(0xFFFF, 0, 0))
     if (self.ver == 2) or (self.ver == 4):
       self.connect("key-press-event", self.onKeyPress)
   else:
     self.p = False
     self.w.recompile()
     self.w.channels_reinit()
     self.but.child.set_label("START !")
     self.but.child.set_use_markup(True)
     self.but.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(0, 0x7700, 0))
     self.but.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.Color(0, 0x7700, 0))

 def version1(self, widget):
   if self.ver != 0:
     self.box1.destroy()
     self.box2.destroy()
   self.ver = 1
   self.box1 = self.w.box(True, self.bb)
   self.w.text("", self.box1)
   self.box2 = self.w.box(True, self.bb)
   self.f = self.w.framebox(" <b>1 - MyMusicMIDI</b> ", False, self.box2, self.r)
   self.b1 = self.w.box(True, self.f)
   self.b2 = self.w.box(True, self.f)
   self.b3 = self.w.box(True, self.f)
   self.w.reset()
   self.w.csd("MyMusicMIDI.csd")
   self.w.spin(0, 0, 16, 1, 1, self.b1, 0, "chan", "Channel #  [0=CC7,\n  \
channels 1-8(9)]")
   self.w.spin(20, 0, 120, 1, 1, self.b1, 0, "ctrl", "1st Controller #")
   self.w.button(self.b2, "pan", "Pan Control ?")
   self.w.text("", self.b2)
   self.w.spin(7, 0, 127, 1, 1, self.b2, 0, "panctrl", "Pan Controller #") 
   self.p = False
   self.w.text("\n<i>Select options first </i>", self.b3, self.g)
   self.but = self.w.cbbutton(self.b3, self.playcsd, "START !")
   self.but.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(0, 0x7700, 0))
   self.but.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.Color(0, 0x7700, 0))

 def version2(self, widget):
   if self.ver != 0:
     self.box1.destroy()
     self.box2.destroy()
   self.ver = 2
   self.box1 = self.w.box(True, self.bb)
   self.w.text("\t\t\t     ", self.box1)
   self.box2 = self.w.box(True, self.bb)
   self.f = self.w.framebox(" <b>2 - MyMusicASCII</b> ", False, self.box2, self.r)
   self.b1 = self.w.box(True, self.f)
   self.b2 = self.w.box(True, self.f)
   self.w.reset()
   self.w.csd("MyMusicASCII.csd")
   self.w.text("   <b>Active Keys:</b>\n1-10(0)  fade secs\nQ-I  \
tones (8) on/off\n\
[Z-/ pan position]\n- (minus) = all off\n", self.b1, self.br)
   self.w.button(self.b2, "pan", "Pan Control ?")
   self.p = False
   self.w.text("\n<i>Select option first </i>", self.b2, self.g)
   self.but = self.w.cbbutton(self.b2, self.playcsd, "START !")
   self.but.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(0, 0x7700, 0))
   self.but.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.Color(0, 0x7700, 0))

 def version3(self, widget):
   if self.ver != 0:
     self.box1.destroy()
     self.box2.destroy()
   self.ver = 3
   self.box1 = self.w.box(True, self.bb)
   self.w.text("", self.box1)
   self.box2 = self.w.box(True, self.bb)
   self.f = self.w.framebox(" <b>3 - OurMusicMIDI</b> ", False, self.box2, self.r)
   self.b1 = self.w.box(True, self.f)
   self.b2 = self.w.box(True, self.f)
   self.b3 = self.w.box(True, self.f)
   self.b4 = self.w.box(True, self.f)
   self.b5 = self.w.box(True, self.f)
   self.b6 = self.w.box(True, self.f)
   self.w.reset()
   self.w.csd("OurMusicMIDI.csd")
   self.w.spin(0, 0, 16, 1, 1, self.b1, 0, "chan", "Channel #  [0=CC7,\n  \
channels 1-8(11)]")
   self.w.spin(20, 0, 120, 1, 1, self.b1, 0, "ctrl", "1st Controller #")
   self.w.spin(0, 0, 3, 1, 1, self.b2, 0, "harm", "Harmonics 0=normal\n\
1=random 2=knob/\nslider  3=MIDI notes")
   self.w.spin(7, 0, 127, 1, 1, self.b3, 0, "harctrl", "Harm Control #")
   self.w.spin(60, 0, 118, 1, 1, self.b3, 0, "harmidi", "1st MIDI Note #\n\
(for harmonics)")
   self.w.button(self.b4, "pan", "Pan Control ?")
   self.w.spin(7, 0, 127, 1, 1, self.b4, 0, "panctrl", "Pan Control #") 
   self.w.text("    If channel='0',\n\
pan=<u>10</u> depth=<u>11</u>", self.b4)
   self.w.spin(0, 0, 2, 1, 1, self.b5, 7, "depth", "   Depth 0=none\n\
1=random 2=cont")
   self.w.spin(7, 0, 127, 1, 1, self.b5, 0, "depctrl", "Depth Control #")
   self.p = False
   self.w.text("\n<i>Select options first </i>", self.b6, self.g)
   self.but = self.w.cbbutton(self.b6, self.playcsd, "START !")
   self.but.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(0, 0x7700, 0))
   self.but.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.Color(0, 0x7700, 0))

 def version4(self, widget):
   if self.ver != 0:
     self.box1.destroy()
     self.box2.destroy()
   self.ver = 4
   self.box1 = self.w.box(True, self.bb)
   self.w.text("\t\t\t\t\t\t\t\t\t\t\t", self.box1)
   self.box2 = self.w.box(True, self.bb)
   self.f = self.w.framebox(" <b>4 - OurMusicASCII</b> ", False, self.box2, 
self.r)
   self.b1 = self.w.box(True, self.f)
   self.b2 = self.w.box(True, self.f)
   self.b3 = self.w.box(True, self.f)
   self.w.reset()
   self.w.csd("OurMusicASCII.csd")
   self.w.text("   <b>Active Keys:</b>\n1-10(0)  fade secs\n\
Q-I  tones (8) on/off\n[A-;  harmonics (10)]\n[Z-/  pan position]\n\
[SHIFT 0(`)-9  depth]\n- (minus) = all off", self.b1, self.br)
   self.w.spin(0, 0, 2, 1, 1, self.b2, 0, "harm", "Harmonics 0=normal\n\
1=random 2=control\n")
   self.w.button(self.b2, "pan", "Pan Control ?")
   self.w.spin(0, 0, 2, 1, 1, self.b3, 0, "depth", "     Depth  0=none\n1\
=random 2=control")
   self.p = False
   self.w.text("<i>Select options first </i>", self.b3, self.g)
   self.but = self.w.cbbutton(self.b3, self.playcsd, "START !")
   self.but.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(0, 0x7700, 0))
   self.but.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.Color(0, 0x7700, 0))

