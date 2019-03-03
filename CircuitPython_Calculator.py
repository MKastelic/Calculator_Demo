# The MIT License (MIT)
#
# Copyright (c) 2018 ladyada for adafruit
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_matrixkeypad`
====================================================

#  Including above copyright and permission notice for the import and use of the
#  adafruit_matrixkeypad library.

from digitalio import Direction, DigitalInOut, Pull
import time
import board
import adafruit_matrixkeypad

def digit_input(button_key, keys_displayed):           # function which handles unique display cases for both operands.

    global percent
    global hold_operand
    
    if percent:
        keys_displayed = ''
        values['input'] = ''
        percent = False         
        hold_operand = False
    if button_key == '.':
        if button_key in keys_displayed:
            pass
        elif keys_displayed == '':
            keys_displayed = '0.'
        else:
            keys_displayed = keys_displayed + '.'
    elif keys_displayed == '0' and button_key != '0':
        keys_displayed = button_key                                
    elif keys_displayed == '0' and button_key == '0':
        pass
    else:
        keys_displayed += button_key
    return keys_displayed

def calc(op, operand_1, operand_2):                    # function which performs the given operation (op) on two given operands.
    
    global hold_operand
    
    if op == '/':
        try:
            result = str(float(operand_1)/float(operand_2))
        except (ZeroDivisionError, ValueError):
            result = 'Error'
    elif op == 'x':
        try:
            result = str(float(operand_1)*float(operand_2))
        except ValueError:
            result = 'Error'
    elif op == '+':
        try:
            result = str(float(operand_1) + float(operand_2))
        except ValueError:
            result = 'Error'
    elif op == '-':
        try:
            result = str(float(operand_1) - float(operand_2))
        except ValueError:
            result = 'Error'
    return result

def sign_display(sign, keys_displayed):                 # function which handles the +/- sign display of any current operand.

    if sign:
        key_list = list(keys_displayed)
        del key_list[0]
        sign = False
        return ''.join(key_list)
    else:
        sign = True
        return '-' + keys_displayed

keys_entered = '0'
keys_entered_1 = ""
operator = ''
hold_operand = False
negative = False
percent = False
calculate = False

cols = [DigitalInOut(x) for x in (board.D0, board.D1, board.D5, board.D6)]        # define hardware pin mapping for MCU and passive
rows = [DigitalInOut(x) for x in (board.D9, board.D10, board.D11, board.D12)]     # keyboard key layout.
keys = ((1, 2, 3, '/'),
        (4, 5, 6, 'x'),
        (7, 8, 9, '+'),
        ('.', 0, '=', 'AC'))

keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)      # create an instance of the Adafruit Matrix_Keypad class to allow      
                                                                    # keyboard scan and key press detection.
while True:
    keys = keypad.pressed_keys
    if len(keys) > 0:
        button = str(keys[0])
        if button is 'AC':                              # clear all entries and flags if 'AC' is pressed.
            keys_entered = '0'
            keys_entered_1 = ''
            negative = False
            operator = ''
            hold_operand = False
            percent = False
        elif button in '1234567890.':
            if calculate:                               # calculate flag is set to True immediately after the = key has been
                keys_entered = ''                       # pressed, so new key_entered is began with appropriate flags reset.
                keys_entered_1 = ''
                operator = ''
                calculate = False
            if operator != '':                          # if an operator has been entered, store the 2nd operand in keys_entered_1
                hold_operand = True                     # and flag with hold_operand set to True.
                keys_entered_1 = digit_input(button, keys_entered_1)
            else:                                       # if an operator has not been entered, store digits in 1st operand.
                keys_entered = digit_input(button, keys_entered)
        elif button is '%':                             # the % key is special because operand must be divided by 100.
            percent = True                              # the percent flag is set to allow detection of new operand input if a
            if hold_operand:                            # digit is entered after the % key.
                keys_entered_1 = str(float(keys_entered_1)/100)
            else:
                keys_entered = str(float(keys_entered)/100)
        elif button in '/x-+':                          
            if hold_operand:                            # if two operands have already been entered, proceed to calculate the
                hold_operand = False                    # intermediate result when an additional operator key is entered.
                hold_operand = False                    # intermediate result when an additional operator key is entered.
                keys_entered = calc(operator, keys_entered, keys_entered_1)
            operator = button
            keys_entered_1 = ''
            calculate = False
            percent = False
        elif button is '+/-':
            if hold_operand:
                keys_entered_1 = sign_display(negative, keys_entered_1)
            else:
                keys_entered = sign_display(negative, keys_entered)
        elif button is '=':                         # perform calculation specified by the given operator on the operands and
            if keys_entered_1 != '':                # repeat calculation for each additional press of the = key.
                keys_entered = calc(operator, keys_entered, keys_entered_1)
                hold_operand = False
                calculate = True
            else:
                print(keys_entered)
       
        if hold_operand and keys_entered_1 != '':    # display 2nd operand if entry is detected.
            print(keys_entered_1)
        else:
            print(keys_entered)

        time.sleep(0.5)
