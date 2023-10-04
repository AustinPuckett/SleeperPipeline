

def extract_first_two_words(text):
    if text == None:
        return text
    words = text.split()
    if len(words) >= 2:
        return ' '.join(words[:2])
    else:
        return text

def get_item_from_dataframe_list_entry(list_entry, list_index=0):
    '''Default is to extract first item from list.'''
    if list_entry == None:
        return list_entry
    elif len(list_entry) == 0:
        return None

    try:
        return eval(list_entry)[list_index]
    except:
        print('Entry ', list_entry, ' could not be evaluated.')

def rank_player_on_roster(entry):
    pass
