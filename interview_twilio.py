#!/usr/bin/python
bracket_list = ['{some text}', # balance 
                '{{some text}', # not balanced
                '{{some text}}', # balanced
                '{{ another string }}}'] # not balanced

for string in bracket_list: # loop through the elements
    open_brackets = 0
    close_brackets = 0
    for char in string: # loop through the characters
        if char == '{':
            open_brackets += 1
        if char == '}':
	    close_brackets += 1
    if open_brackets == close_brackets:
        print 'The string "%s" is balanced' % string
    else:
        print 'The string "%s" is unbalanced' % string
   
