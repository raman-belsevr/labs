"""
A keyboard controller that simulates the sticks
of a radio controller. Default configuration is in Mode 3,
with arrows and qzsd keys. Switch button is left alt.

Copyright (C) Kevin P (wazari972) 2015

Configuration
-------------

to adjust Keyboard.BINDINGS/INC_RATE/AUTO_DEC_RATE/SWITCHES:

> from quadstick.keyboard import Keyboard

> Keyboard.BINDING[pygame.locals.K_key] = +/-Keyboard.THROTTLE
> Keyboard.INC_RATE[Keyboard.THROTTLE] = ...
> Keyboard.AUTO_DEC_RATE[Keyboard.THROTTLE] = ...

> Keyboard.SWITCHES[pygame.locals.K_key] = Keyboard.SWITCH_1

The slowdown ration is to reduce the increase and decrease rate.
You may have to adjust it according to the pace of the simulator.

> Keyboard.SLOWDOWN_FACTOR = 2 # keys will be twice less sensitive
"""

from __future__ import print_function

import pygame
import pygame.locals
from sim.control.generic_controller import  GenericController

class Keyboard(GenericController):
    SLOWDOWN_FACTOR = 1

    _, THROTTLE, YAW, ROLL, PITCH = range(5) # value 0 not used
    
    SWITCHES = SWITCH_1,SWITCH_2,SWITCH_3 = range(3)

    INC_RATE = {
        THROTTLE: 0.01,
        YAW: 0.01,
        PITCH: 0.01,
        ROLL: 0.01
        }
    
    AUTO_DEC_RATE = {
        THROTTLE: 0,
        YAW: 0.005,
        PITCH: 0.005,
        ROLL: 0.005
        }
    
    BINDINGS = { 
        pygame.locals.K_UP   :  THROTTLE,
        pygame.locals.K_DOWN : -THROTTLE,
        pygame.locals.K_RIGHT:  YAW,
        pygame.locals.K_LEFT : -YAW,
        pygame.locals.K_w : -PITCH,
        pygame.locals.K_s :  PITCH,
        pygame.locals.K_d : -ROLL,
        pygame.locals.K_a :  ROLL
        }
    
    SWITCHES = {
        pygame.locals.K_LALT : SWITCH_1,
        pygame.locals.K_LCTRL : SWITCH_2, # not used
        pygame.locals.K_LMETA : SWITCH_3, # not used
        }
    
    def __init__(self, switch_labels):
        GenericController.__init__(self, 'Keyboard Controller', switch_labels)
        self.power = [None, 0, 0, 0, 0] # value 0 not used
        self.keysdown = {}
        # Support alt/pos-hold through repeated button clicsk
        self.switch_value = 0

    def _get_switchval(self):
        return self.switch_value

    def _get_axis(self, axis_index_asked):
        keys = pygame.event.get()
        
        # collect keys up and down
        for event in keys:
            is_switch = False
            try:
                key_binding = Keyboard.BINDINGS[event.key]
            except:
                try:
                    key_binding = Keyboard.SWITCHES[event.key]
                    is_switch = True
                except:
                    continue # not an interesting key
            
            if event.type == pygame.locals.KEYDOWN:
                self.keysdown[event.key] = key_binding, is_switch
            elif event.type == pygame.locals.KEYUP:
                del self.keysdown[event.key]
            else:
                assert "Key not up nor down ??" # should not come here
                continue

        # increase keys down
        for key, (axis_index, is_switch) in self.keysdown.items():
            if is_switch:
                if axis_index is None: # switch already hit
                    continue

                self.switch_value += 1
                self.switch_value %= 3

                self.keysdown[key] = (None, True) # do not repeat switch
                continue
            
            direction = 1 if axis_index > 0 else -1
            axis_index = abs(axis_index)
            
            axis_increase = Keyboard.INC_RATE[axis_index] * direction
            
            if axis_index != Keyboard.THROTTLE:
                power = self.power[axis_index]

                #reset stick if push on the other way
                if axis_increase > 0 and power < 0:
                    self.power[axis_index] = 0
                if axis_increase < 0 and power > 0:
                    self.power[axis_index] = 0
            
            axis_increase *= Keyboard.SLOWDOWN_FACTOR
                
            self.power[axis_index] += axis_increase
            
        # decrease keys up and check boundaries
        for dec_axis_index in (Keyboard.YAW, Keyboard.PITCH, Keyboard.ROLL):
            power = self.power[dec_axis_index]
            dec = Keyboard.AUTO_DEC_RATE[dec_axis_index]
            if power < 0:
                dec *= -1
                
            dec *= Keyboard.SLOWDOWN_FACTOR
                
            self.power[dec_axis_index] -= dec

            # check boundaries -1 < ... < 1
            self.power[dec_axis_index] = max(self.power[dec_axis_index], -1)
            self.power[dec_axis_index] = min(self.power[dec_axis_index], 1)
            
        # check throttle boundaries 0 < ... < 1
        self.power[Keyboard.THROTTLE] = max(self.power[Keyboard.THROTTLE], 0)
        self.power[Keyboard.THROTTLE] = min(self.power[Keyboard.THROTTLE], 1)
        
        return self.power[axis_index_asked]
    
    def _startup_message(self):

        return 'Please cycle throttle to begin.'

    def _get_pitch(self):
    
        return self._get_axis(Keyboard.PITCH)

    def _get_roll(self):
    
        return self._get_axis(Keyboard.ROLL)

    def _get_yaw(self):

        return self._get_axis(Keyboard.YAW)

    def _get_throttle(self):
        return self._get_axis(Keyboard.THROTTLE)

