''' 
The purpose of this simple application is to allow the user to perform the following tasks: 
1. Enter the number of people reading,
2. Enter the number of verses in the chapter being read,
3. Enter how many verses each person would like to read (or have the option to allow the app to suggest the number of verses to read based on number of people reading and number of verses in the chapter to split evenly),
4. Ability to add people's names and then display whose turn it is to read,
5. Ability to enter that one person has finished reading and then display who should read next based on the order of reading entered by the user,
6. Display which verses the next person should read.
7. Tell the user when they have finished reading.
8. Provide a simple GUI for the user to input, and view the application's output. (Using PySimpleGUI)
'''
import PySimpleGUI as sg

# Get number of people reading
num_people = int(sg.popup_get_text('Enter the number of people reading'))

# Get reader names
reader_names = []
for i in range(num_people):
    reader_names.append(sg.popup_get_text(f'Enter the name of reader number {i + 1}:'))

#Get number of verses in the chapter, and ask for number of verses for each person
#to read or offer to suggest a number
verses_count = int(sg.popup_get_text('Please enter the number of verses in the chapter:'))
num_verse_per = sg.popup_get_text("Please enter the number of verses you would like each person to read at a time (Enter the word 'Suggest' to have a number suggested): ")

#If suggest was typed, suggest a number that evenly splits verses between people reading,
#or is divisible by the verse count but will have to be read multiple times.
if num_verse_per.lower() == 'suggest':
    suggested_nums = []
    suggested_count = verses_count // num_people
    sg.popup('Suggested number of verses for each person to read:', suggested_count)
    #Displays the number of verses left over if suggested number has a remainder
    if verses_count % num_people != 0:
        extra_verses = verses_count % num_people
        if extra_verses == 1:
            sg.popup(f'With {extra_verses} extra verse for the last person to read.')
        else:
            sg.popup(f'With {extra_verses} extra verses for the last person to read or split with others.')
    #Also suggest numbers from withing range 3-8 that divide with no remainder
    for i in range(3, 9):
        if verses_count % i == 0:
           if i == suggested_count:
               pass
           else:
               suggested_nums.append(i)
    #Format the numbers from a list into a string
    if suggested_nums != []:  
        formatted_nums = ', '.join(map(str, suggested_nums[:-1]))
        if len(suggested_nums) > 1:
            formatted_nums += f", or {suggested_nums[-1]}"
        else:
            formatted_nums = str(suggested_nums[0])
        
        sg.popup(f'Or {formatted_nums} which will have no remainder verses.')
    
    #Ask now, after giving suggestions, how many verses for each person
    num_verse_per = int(sg.popup_get_text('Please enter the number of verses you would like each person to read at a time: '))

import math
current_verse = 0
temp_current_verse = 1
num_turns_to_read = math.ceil(verses_count/int(num_verse_per))

#In the range of the number of turns that are needed to read through all the verses in the
#chapter, state whose turn it is, and which verses they are to read. If verses are left over
#at the end, state how many extra verses are left.

# Loop through the number of turns required
for i in range(num_turns_to_read):

    # Calculate the next verse up to which the reader will read
    next_verse = min(current_verse + int(num_verse_per), verses_count)
    
    # Handle case when the reader is within the bounds of `reader_names`
    reader = reader_names[i % len(reader_names)]
    if i == 0:
        sg.popup(f'First person to read is {reader}, starting at verse {temp_current_verse}, until verse {next_verse}')
    # Handle extra verses at the end
    elif i + 1 == num_turns_to_read and (verses_count - current_verse) != num_verse_per:
        extra_verses = verses_count - current_verse
        sg.popup(f'There {"is" if extra_verses == 1 else "are"} {extra_verses} extra {"verse" if extra_verses == 1 else "verses"} to read.')
    # State who is next to read
    else:
        sg.popup(f'Next person to read is {reader}, starting at verse {temp_current_verse}, until verse {next_verse}')
    
    # Update `current_verse` and `temp_current_verse` for the next iteration
    current_verse = next_verse
    temp_current_verse = current_verse + 1
    
    # Force user to hit enter to see next person to read, if there are extra verses
    #don't force user to hit enter to see the extra verses.
  #  if i + 1 != num_turns_to_read:
  #      if (verses_count - next_verse) < int(num_verse_per):
  #          pass
 #       else:
 #           move_next = sg.popup("Press 'Enter' to see the next person to read: ")

sg.popup('You have finished the chapter.')
