# sugar-aware GUI classes
# with boxes, sliders, spinbuttons, buttons, etc
#
# (c) Victor Lazzarini, 2006-08
#   
#    This library is free software; you can redistribute it
#    and/or modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    csndsugui is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with csndsugui; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
#    02111-1307 USA
#
#    As a special exception, if other files instantiate templates or
#    use macros or inline functions from this file, this file does not
#    by itself cause the resulting executable or library to be covered
#    by the GNU Lesser General Public License. This exception does not
#    however invalidate any other reasons why the library or executable
#    file might be covered by the GNU Lesser General Public License.
#
#
#  version 0.1.3  06/08/08

import pygtk
pygtk.require('2.0')
from sugar.activity import activity
import gtk, gobject
import sys
import csnd
import math
import locale
import os
import sugar.logger
import time

class BasicGUI:
    """Basic GUI with boxes, sliders, spins, buttons etc
    using pygtk/sugar, from which GUI classes
    can be derived for Csound use."""
    
    def scale_font(self, widget):
      font = widget.get_pango_context().get_font_description()

# The FONT DISPLAY in this activity can be resized (smaller or larger)
# by changing the value of "resize" below. "Resize" can be positive
# or negative, and is not limited to integers. A value of 1 equals a
# point in font size.
      resize = 0

      font_size = font.get_size() + (resize * 1024)
      width = gtk.gdk.screen_width()
      mult = width * .00076
      if os.path.exists("/etc/olpc-release") or os.path.exists("/etc/power/olpc-pm"):
        mult = width * .00082
      elif os.path.exists("/etc/fedora-release"):
        release = open("/etc/fedora-release").read()
        if release.find("SoaS release 1 ") != -1:
          mult = width * .00132
        elif release.find("SoaS release 2 ") != -1:
          mult = width * .00085
        elif release.find("Fedora release ") != -1:
          mult = width * .00119
      font.set_size(int(font_size * mult))
      widget.modify_font(font)
  
    def set_channel(self,name, val):
       """basic bus channel setting method,
       should be overriden for full-functionality."""
       self.logger.debug("channel:%s, value:%.1f" % (name,val))

    def set_filechannel(self,chan,name):
        """basic filename channel setting method
        should be overriden for full-functionality."""
        self.logger.debug("channel:%s, filename:%s" % (chan,name))
    
    def set_message(self, mess):
        """basic message setting method
        should be overriden for full-functionality."""
        self.logger.debug(mess)

    def get_slider_value(self,name):
        """returns the slider value
          name: slider name (which should also be the attached bus channel name"""
        for i in self.sliders:
          if i[1] == name:
           return i[2]
        return 0

    def get_button_value(self,name):
        """returns the button value (0 or 1)
        name: button name (which should also be the attached bus channel name)"""
        for i in self.buttons:
          if i[1] == name:
           return i[2]
        return 0   

    def get_slider(self,name):
        """returns the slider widget instance
           name: slider name"""
        for i in self.sliders:
          if i[1] == name:
           return i[0]
        return 0
   
    def get_button(self,name):
        """returns the button widget instance
           name: button name"""
        for i in self.sliders:
          if i[1] == name:
           return i[0]
        return 0
    
    def set_focus(self):
        """ called whenever the focus changes """
        self.logger.debug(self.focus)

    def focus_out(self, widget, event):
        if(self.focus):
           self.focus = False
           self.set_focus()

    def focus_in(self, widget, event):
        if(not self.focus):
            self.focus = True
            self.set_focus()

    def focus_back(self, widget, event):
        self.window.disconnect(self.fback)
        self.focus_connect()

    def buttcallback(self, widget, data=None):
      for i in self.buttons:
         if i[0] == widget:
          if i[2]: 
            i[2] = 0
            i[0].modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(0x8000,0x8000,0x8000, 2))
            i[0].modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.Color(0x8000,0x8000,0x8000, 2))
          else:
            i[2] = 1
            i[0].modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(0xFFFF,0,0, 1))
            i[0].modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.Color(0xFFFF,0,0, 2))
          self.set_channel(i[1], i[2])  

    def button_setvalue(self, widget, value):
          if not value: 
            widget.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(0x0FFF,0,0x00FF, 2))
            widget.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.Color(0xFFFF,0,0xFFFF, 2))
          else:
            widget.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(0xFFFF,0,0, 1))
            widget.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.Color(0xFFFF,0,0, 2))

    def mbuttcallback(self, widget, data=None):
      for i in self.mbuttons:
         if i[0] == widget:
          self.set_message(i[2])  

    def slidcallback(self,adj,widget):
      for i in self.sliders:
         if i[0] == widget:
          i[2] = adj.value
          if i[4]:                
            self.set_channel(i[1],i[2])           
            i[3].set_text("%f" % i[2])
            pass
          else:
            value = i[5]*pow(i[6]/i[5], i[2]/i[6])
            self.set_channel(i[1], value)
            i[3].set_text("%.3f" % value)
            pass
    
    def spincallback(self,adj,widget):
      for i in self.spins:
         if i[0] == widget:
          i[2] = adj.value
          self.set_channel(i[1],i[2])
    
    def filecallback(self,widget):           
        name = self.curfile[0].get_filename()        
        self.set_filechannel(self.curfile[2], name)
        for i in self.buttons:
         if i[0] == self.curfile[1]:
           i[2] = name
        self.filenames.update({self.curfile[2] : name})
        self.curfile[0].destroy()
        self.fback = self.window.connect('focus_out_event', self.focus_back)     

    def destroy_chooser(self,widget):
        self.curfile[0].destroy()
        
    def fbuttcallback(self, widget, data=None):
      self.focus_disconnect()
      for i in self.buttons:
         if i[0] == widget:
          chooser = gtk.FileSelection(i[1])
          self.curfile = (chooser, i[0], i[1])
          chooser.set_filename(self.data_path)
          chooser.ok_button.connect("clicked", self.filecallback)
          chooser.cancel_button.connect("clicked", self.destroy_chooser)
          chooser.show()

    def cbbutton(self,box,callback,title=""):
       """Creates a callbackbutton
          box: parent box
          callback: click callback
          title: if given, the button name
          returns the widget instance"""
       self.cbbutts = self.cbbutts + 1
       butt = gtk.Button(title)
       self.scale_font(butt.child)
       box.pack_start(butt, False, False, 2)
       self.cbbuttons.append([butt,title,0])
       butt.connect("clicked", callback)
       butt.show()
       return butt
   
    def button(self,box, title="",label=""):
       """Creates a button (on/off)
           box: parent box
           title: if given, the button name,
             which will also be the bus channel
             name. Otherwise a default name is
             given, BN, where N is button number
             in order of creation.
           label: if given, an alternative button name,
             which will be displayed instead of title
           returns the widget instance"""
       self.butts = self.butts + 1
       if title == "":
         title = "B%d" % self.butts
       if label == "": name = title
       else: name = label
       butt = gtk.Button(" %s " % name)
       self.scale_font(butt.child)
       butt.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.Color(0x8000,0x8000,0x8000, 2))
       box.pack_start(butt, False, False, 1)
       self.buttons.append([butt,title,0])
       butt.connect("clicked", self.buttcallback)
       butt.show()
       return butt

    def mbutton(self,box,mess,title=""):
       """Creates a mbutton (for sending a message)
           box: parent box
           title: if given, the button name, otherwise a default name is
            given, BN, where N is button number
            in order of creation.
           mess: message to be sent when button is clicked
           returns the widget instance"""
       self.mbutts = self.mbutts + 1
       if title == "":
         title = "B%d" % self.mbutts
       butt = gtk.Button(title)
       butt.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(0x0FFF,0,0x00FF, 1))
       butt.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.Color(0xFFFF,0xFFFF,0x0000, 2))
       box.pack_start(butt, False, False, 5)
       self.mbuttons.append([butt,title,mess])
       butt.connect("clicked", self.mbuttcallback)
       butt.show()
       return butt
  
    def box(self,vert=True, parent=None, padding=3):
       """creates a box 
           vert: True, creates a vertical box; horiz.
            otherwise
           parent: parent box, None if this is a toplevel box
           padding: box padding
           returns the widget instance"""
       if vert:
         box = gtk.VBox()
       else:
         box = gtk.HBox()
       if parent:
         parent.pack_start(box, False, False, padding)
       else:
         self.outbox.pack_start(box, False, False, padding)
       self.boxes.append(box)
       box.show()     
       return box

    def filechooser(self,box,title,label=""):
        """Creates a filechooser button
           title: button name, also file bus channel name
           box: parent box
           label: if given, alternative name, for display purposes only
             otherwise button will display its title."""
        if label == "": name = title
        else: name = label
        butt = gtk.Button(name)
        box.pack_start(butt, False, False, 5)
        self.buttons.append([butt,title,"0"])
        butt.connect("clicked", self.fbuttcallback)
        self.set_filechannel(title,"0")
        self.filenames.update({title:"0"})
        butt.show()
        return butt

    def slider(self,init, start, end, x, y, box, title="",vert=True,linear=True,dwid=100,label=""):
       """Creates a slider
           init: initial value
           start, end: start and end of slider range
           x, y: x and y sizes of slider
           box: parent box
           title: if given, the slider name,
            which will also be the bus channel
            name. Otherwise a default name is
            given, SN, where N is slider number
            in order of creation.
           vert: vertical slider (True), else horiz.
           linear: linear response (True), else exponential (zero or negative
            ranges are not allowed)
           dwid:  display width in pixels
           label: if given, the alternative slider name, for display only 
           returns the widget instance"""
       self.slids = self.slids + 1
       if title == "":
          title = "S%d" % self.slids
       a = end - start 
       if vert:
          step = a/y
          adj = gtk.Adjustment(init,start,end,step,step,0) 
          slider = gtk.VScale(adj)
          slider.set_inverted(True)
       else:
          step = a/x
          adj = gtk.Adjustment(init,start,end,step,step,0)
          slider = gtk.HScale(adj)
       slider.set_draw_value(False)
       if step < 1.0:
        slider.set_digits(3)
       elif step < 10:
        slider.set_digits(2)
       elif step < 100:
        slider.set_digits(1)
       else:
        slider.set_digits(0)
       entry = gtk.Entry(5) 
       if vert: entry.set_size_request(dwid,50)
       else: entry.set_size_request(dwid,50)
       entry.set_editable(False)
       if not linear:
         if (init <= 0) or (start <= 0) or (end <= 0):
            linear = True
       if not linear:
         pos = end*math.log(1,end/start)
         slider.set_range(pos, end)
         pos = end*math.log(init/start,end/start)
         slider.set_value(pos)
       if label == "": name = title
       else: name = label
       entry.set_text("%f" % init)
       label = gtk.Label(name)
       slider.set_size_request(x,y)
       box.pack_start(slider, False, False, 5)
       box.pack_start(entry, False, False, 2)
       box.pack_start(label, False, False, 2)
       self.sliders.append([slider,title,init,entry,linear,start,end])
       adj.connect("value_changed", self.slidcallback, slider)
       slider.show()
       entry.show()
       label.show()
       self.set_channel(title, init)
       return slider
   
    def numdisplay(self,box,title="",init=0.0,label=""):
        self.ndispwids = self.ndispwids + 1
        entry = gtk.Entry()
        if label == "": name = title
        else: name = label
        entry.set_text("%f" % init)
        label = gtk.Label(name)
        box.pack_start(entry, False, False, 2)
        box.pack_start(label, False, False, 2)
        self.ndisps.append([entry,title,init])
        entry.show()
        label.show()
        self.set_channel(title,init)  
        return entry

    def setnumdisp(self,title,val):
        for i in self.ndisps:
            if i[1] == title:
               i[2] = val
               i[0].set_text("%f" % val)
               self.set_channel(title, val)
 
    def spin(self,init, start, end, step, page, box, accel=0,title="",label=""):
       """Creates a spin button
          init: initial value
          start, end: start and end of slider range
          step, page: small and large step sizes
          box: parent box
          accel: acceleration or 'climb rate' (0.0-1.0)
          title: if given, the spin button name,
            which will also be the bus channel
            name. Otherwise a default name is
            given, SPN, where N is spin number
            in order of creation.
          label: if given, the alternative name for the widget, for display only.
          returns the widget instance"""
       self.spinbs = self.spinbs + 1
       if title == "":
          title = "SP%d" % self.spinbs
       adj = gtk.Adjustment(init,start,end,step,page,0) 
       spin = gtk.SpinButton(adj,accel)      
       self.scale_font(spin)             
       spin.set_alignment(.5)
       if label == "": name = title
       else: name = label
       label = gtk.Label(name)
       self.scale_font(label)             
       box.pack_start(spin, False, False, 3)
       box.pack_start(label, False, False, 0)
       self.spins.append([spin,title,init])
       adj.connect("value_changed", self.spincallback, spin)
       spin.show()
       label.show()
       self.set_channel(title, init)
       return spin

    def text(self, name, box=None,colour=(0,0,0)): 
      """Creates a static text label
         name: text label
         box: parent box, None if text is to be placed toplevel
         colour: RGB values in a tuple (R,G,B)
         returns the widget instance"""
      label = gtk.Label(name)
      self.scale_font(label)             
      label.set_use_markup(True)
      label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color(colour[0],colour[1],colour[2], 0))
      if box:
       box.pack_start(label, False, False, 3)
      else:
       self.outbox.pack_start(label, False, False, 3)
      label.show()
      return label 

    def framebox(self, name, vert=True, parent=None, colour=(0,0,0), padding=5): 
      """Creates a frame box
         name: text label
         vert: vertical (True) box, else horiz.
         parent: parent box, if None, this is a toplevel box
         colour: RGB values in a tuple (R,G,B) 
         padding: padding space
         returns the box widget instance"""
      frame = gtk.Frame(name)
      self.scale_font(frame.get_label_widget())             
      frame.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(colour[0],colour[1],colour[2], 0))
      frame.get_label_widget().modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color(colour[0],colour[1],colour[2], 0))
      frame.get_label_widget().set_use_markup(True)
      if parent:
        parent.pack_start(frame, False, False, padding)
      else:
        self.outbox.pack_start(frame, False, False, padding)
      if vert:
        box = gtk.VBox()
      else:
        box = gtk.HBox()
      frame.add(box)
      frame.show()
      box.show()
      return box
      
    def vsliderbank(self,items,init, start, end, x, y, box):
        """Creates a vertical slider bank 
             items: number of sliders
             init: initial value
             start, end: start and end of slider range
             x, y: x and y sizes of slider
             box: parent box"""
        slid = self.slids
        for i in range(slid, slid+items):
           cbox = self.box(parent=box)
           self.slider(init,start,end,x,y,cbox)

    def hsliderbank(self,items,init, start, end, x, y, box):
        """Creates a horizontal slider bank 
           items: number of sliders
           init: initial value
           start, end: start and end of slider range
           x, y: x and y sizes of slider
           box: parent box"""
        slid = self.slids
        for i in range(slid, slid+items):
           cbox = self.box(False,box)
           self.slider(init,start,end,x,y,cbox,"",False)

    def buttonbank(self,items, box):
        """Creates a button bank 
           items: number of sliders
           box: parent box."""
        start = self.butts
        for i in range(start, start+items):
           self.button(box)

    def delete_event(self, widget, event, data=None):
       return False

    def get_toolbox(self):
        """Returns the Activity toolbox"""
        return self.toolbox

    def channels_reinit(self):
       """ resets channel to current widget values"""
       for j in self.buttons:
           if(j[1] != "pause"):
             if(j[1] != "play"):
               if(j[1] != "reset"):
                  self.set_channel(j[1],j[2])
       for j in self.sliders:
          if j[4]:                
            self.set_channel(j[1],j[2])           
            pass
          else:
            value = j[5]*pow(j[6]/j[5], j[2]/j[6])
            self.set_channel(j[1], value)
       for j in self.spins:
           self.set_channel(j[1],j[2])          
                
    def widgets_reset(self):
       """ resets widget to channel values""" 
       for j in self.buttons:
           self.button_setvalue(j[0], j[2])
           self.set_channel(j[1],j[2])
       for j in self.sliders:
           j[0].set_value(j[2])
           j[0].emit("value_changed")
       for j in self.spins:
           j[0].set_value(j[2])
           j[0].emit("value_changed")            
    
    def channels_save(self):
        """ Saves a list with channel names and current values.
            Returns a list of tuples (channel_name, channel_value)"""
        chan_list = []
        for i in self.channel_widgets:
          for j in i:
           if(j[1] != "pause"):
             if(j[1] != "play"):
               if(j[1] != "reset"):
                chan_list.append((j[1],j[2]));
        return chan_list

    def channels_load(self, chan_list):
        """ Loads a list with channel names and values into the
            current channel list """
        for i in self.channnel_widgets:
         for j in i:
           cnt = 0
           while(j[1] == chan_list[cnt][0]):
                j[1] = chann_list[cnt][0]
                j[2] = chan_list[cnt][1]
                cnt = cnt+1
        self.widgets_reset()

    def set_channel_metadata(self):
        """ Saves channel data as metadata. Can be called in
            write_file() to save channel/widget data """
        mdata = self.channels_save()
        for i in mdata:
           self.window.metadata['channel-'+i[0]] = str(i[1])

    def get_channel_metadata(self):
        """ Retrieves channel data from metadata. Can be called after
            widgets have been created to retrieve channel data and 
            reset widgets """
        for i in self.channel_widgets:
          for j in i:
           mdata = self.window.metadata.get('channel-'+j[1],'0')
           if mdata is None: continue
           else:
            try: j[2] = float(mdata)
            except: j[2] = mdata 
        self.widgets_reset()
         
             
    def nofocus(self):
       pass
   
    def focus_connect(self):
      if not self.connected:
       self.focus = True
       self.in_id = self.window.connect('focus_in_event', self.focus_in)
       self.out_id = self.window.connect('focus_out_event', self.focus_out)
       self.connected = True
 
    def focus_disconnect(self):
      if self.connected:
       self.window.disconnect(self.in_id)
       self.window.disconnect(self.out_id)
       self.connected = False

    def __init__(self,act,colour=(-1,-1,-1),vert=True,toolbox=None):
       """Constructor
         act:  activity object
         colour: bg colour RGB tuple (R,G, B)
         vert: True for vertical topmost arrangement, horiz. otherwise
         toolbox: activity toolbox object, if None (default) a
            standard toolbox will be supplied"""
       self.sliders = []
       self.slids = 0
       self.spins = []
       self.spinbs = 0
       self.buttons = []
       self.butts = 0
       self.cbbuttons = []
       self.cbbutts = 0
       self.mbuttons = []
       self.mbutts = 0
       self.boxes = []
       self.ndisps = []
       self.ndispwids = 0
       self.connected = False
       self.channel_widgets = [self.sliders, self.spins, self.buttons]
       self.filenames = dict()
       self.window = act
       if toolbox == None:
        self.toolbox = activity.ActivityToolbox(self.window)
       else: self.toolbox = toolbox
       self.window.set_toolbox(self.toolbox)
       self.toolbox.show()
       if colour[0] >= 0:
        self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(colour[0],colour[1],colour[2], 0))
       if vert: self.outbox = gtk.VBox()
       else: self.outbox = gtk.HBox()
       self.window.set_canvas(self.outbox)
       self.data_path = os.path.join(act.get_activity_root(),"data/")
       self.outbox.show()
       self.logger = sugar.logger.logging.getLogger('csndsugui')


class CsoundGUI(BasicGUI):
     """A class inheriting from BasicGUI containing a Csound instance and a performance 
     thread instance."""  

     def set_channel(self,name,val):
      """overrides the base method.
         sets the bus channel value, called by the widget callbacks
         channel names 'play', 'pause' and
         'reset' are reserved for these respective uses"""
      if not self.ready:
       if name == "play":
         self.play()
       elif name == "pause":
         self.pause()
       elif name == "reset":
         self.reset()     
       self.csound.SetChannel(name,val)
      else:
       BasicGUI.set_channel(self,name,val)

     def set_filechannel(self,chan,name):
      """overrides the base method, setting the channel string"""
      if not self.ready:
       self.csound.SetChannel(chan,name)
      else:
       BasicGUI.set_filechannel(self,chan,name)
      
     def set_message(self, mess):
        """overrides the base method, sends a score message"""
        self.perf.InputMessage(mess) 

     def set_focus(self): 
         """overrides the base class method, resetting/recompiling Csound"""
         if self.focus:
            self.compile()
            self.channels_reinit()
            if self.replay and not self.on:
             self.play()
             self.logger.debug("focus_off and playing")
         else:
            self.replay = self.on
            self.logger.debug("focus_out and stopping")
            self.reset()    
         return 1

     def play(self):
         """Starts a performance. """
         if not self.on:
          if self.paused: return
          self.on = True
          self.perf.Play()
         else:
          self.on = False
          self.perf.Pause()

     def pause(self):
         """Pauses a performance. """
         if self.on: 
          self.on = False
          self.paused = True
          self.perf.Pause()
         elif self.paused:
          self.on = True
          self.paused = False
          self.perf.Play()

     def csd(self, name):
         """Sets the source CSD and compiles it.
             name: CSD filename
             returns zero if successful"""
         path = activity.get_bundle_path()
         if self.ready:
            res = self.csound.Compile("%s/%s" % (path,name))
            if not res: 
             self.ready = False
             self.focus_connect()
            self.path = path
            self.name = name
            return res

     def recompile(self):
         """Recompiles the set CSD.
            returns zero if successful"""
         if not self.ready and self.name !=  "0":
            self.perf.Stop()
            self.perf.Join()
            self.on = False
            self.paused = False
            self.perf = csnd.CsoundPerformanceThread(self.csound)
            if self.arglist != None:
             res = self.csound.Compile(self.arglist.argc(),self.arglist.argv())
            else:
             res = self.csound.Compile("%s/%s" % (self.path,self.name))
            if(res): self.ready = True
            return res

     def compile(self,name=None,args=[]):
         """Compiles Csound code.
            name: CSD filename if given
            args: list of arguments (as strings)
            returns 0 if successful , non-zero if not."""
         if self.ready:
          if args != []:
           self.arglist = csnd.CsoundArgVList()
          self.path = activity.get_bundle_path()
          if name != None: self.name = name
          elif self.name == "0": return -1
          if self.arglist != None:
            if name != None:
             self.arglist.Append("csound")
             self.arglist.Append("%s/%s" % (self.path,self.name))
             for i in args: 
              self.arglist.Append(i)
            res = self.csound.Compile(self.arglist.argc(),self.arglist.argv())
          else: res = self.csound.Compile("%s/%s" % (self.path,self.name))
          if not res:
            self.ready = False
            self.focus_connect()
          else:
            self.arglist = None
          return res
            
     def reset(self):
         """Resets Csound, ready for a new CSD"""
         if not self.ready:
            self.perf.Stop()
            self.perf.Join()
            self.on = False
            self.paused = False
            self.perf = csnd.CsoundPerformanceThread(self.csound)
            self.ready = True

     def close(self, event):  
         self.reset()
         sys.exit(0)

     def tcallback(self,cbdata):
         if self.stopcb: return False
         if self.on and self.sync:
            self.tcb(cbdata)
         return True

     def set_timer(self,time,cb,cbdata,sync=True):
         """Sets a timer callback, called at time intervals. 
            Sync=True makes it start/stop with Csound performance"""
         if(self.stopcb == True):
           self.sync = sync
           self.tcb = cb
           self.stopcb = False
           gobject.timeout_add(time,self.tcallback,cbdata)

     def stop_timer(self):
         """Stops the timer"""
         self.stopcb = True

     def score_time(self):
         """Returns the current score time"""
         return self.csound.GetScoreTime()   

     def __init__(self,act,colour=(-1,-1,-1),vert=True):
         """constructor
            act:  activity object
            colour: bg colour RGB tuple (R,G, B)
            vert: True for vertical topmost arrangement, horiz. otherwise."""
         locale.setlocale(locale.LC_NUMERIC, 'C')
         self.csound  = csnd.Csound()
         self.perf = csnd.CsoundPerformanceThread(self.csound)
         BasicGUI.__init__(self,act,colour,vert)
         self.ready = True
         self.on = False
         self.paused = False
         self.name = "0"
         self.arglist = None
         self.replay = False
         self.stopcb = True

