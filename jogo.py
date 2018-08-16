from random import shuffle, choice
from os import listdir

def positive_msg():
    positivemsgs = ['Try again', 'You can do it', 'Don\'t give up']
    return choice(positivemsgs)

def word_sort(words):
    return choice(words)

def word_shuffle(word):
    shuffledword = list(word)
    shuffle(shuffledword)
    return ''.join(shuffledword)

def themeChoice():
    themes, words = [], []
    print('Select the theme:\n', end='\n')
    for y,x in enumerate(listdir('wordthemes/')):
        themes.append(x)
        print('{} - {}'.format(y + 1, '{}'.format(x).split('.')[0]))
    theme = int(input('\nYour choice:\n'))-1
    if theme in [x for x in range(len(themes))]:
        arc = open("wordthemes/{}".format(themes[theme]), "r")
    else:
        print('\nInvalid choice\n')
        return themeChoice()
    for x in arc:
        if x != '\n':
            words.append(x.replace('\n',''))
    arc.close()
    return words

def difficult():
    lvls = ['easy', 'normal', 'hard', 'godlike']
    difficults = [10, 5, 3, 1]
    print('\nSelect the difficult:\n', end='\n')
    for y,x in enumerate(lvls):
        print('{} - {}'.format(y+1,x.upper()))
    numDiff = int(input('\nYour choice:\n'))-1
    if numDiff in [0,1,2,3]:
        return difficults[numDiff]
    else:
        return difficult()

words = themeChoice()
word = word_sort(words)
shuffledword = word_shuffle(word)
numsOfTry = difficult()
trys = 1

print('\nThe shuffled word is: \'{}\'.'.format(shuffledword))

while trys <= numsOfTry:
    tryAgainOverAndOverAgain = input('\nTry to figure out the sorted word. Attempt {}/{}:\n'.format(trys, numsOfTry))
    if tryAgainOverAndOverAgain == word:
        print('\n\n\n\n{0} CONGRATULATIONS {0}\n\n{1}You\'re right!\n'.format('='*20,' '*22))
        break
    elif trys == numsOfTry:
        print('\n\n\n\n{0} WE ARE SORRY {0}\n\n{1}You missed all the attempts. :('.format('-'*21,' '*13))
    else:
        print('\n{}'.format(positive_msg()))
        trys += 1
print('The word actually was \'{}\' and the shuffle was \'{}\''.format(word,shuffledword))