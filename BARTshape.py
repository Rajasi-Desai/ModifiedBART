#Modified version of BART
#Developer: Rajasi Desai
#Based on version developed by Hannah Sophie Heinrichs
#https://github.com/hsx1/bart_task

# A simple version of the Balloon Analog Risk Task (BART) written with PsychoPy.
# This experiment is a computerized, laboratory-based measure that involves actual
# risky behavior for which, similar to real-world situations, riskiness is rewarded
# up until a point at which further riskiness results in poorer outcomes.
# Participants complete 90 trials where they pump a balloon and obtain money.
# With every pump a balloon wil explode with increasing probability (Lejuez et al. 2002).
# Subject and data will be seperately stored in txt files and can be matched by subject id.

# It is entirely based on:
# Lejuez, C. W., Read, J. P., Kahler, C. W., Richards, J. B., Ramsey, S. E., Stuart, G. L., ... & Brown, R. A. (2002).
# Evaluation of a behavioral measure of risk taking: the Balloon Analogue Risk Task (BART).
# Journal of Experimental Psychology: Applied, 8(2), 75-84. http://dx.doi.org/10.1037/1076-898X.8.2.75
# source: http://www.impulsivity.org/measurement/BART


import random
from psychopy import core, data, event, gui, visual
import datetime


# window and stimulus sizes
WIN_WIDTH = 1280
WIN_HEIGHT = 720
BALL_TEXTURE_SIZE = (596, 720)
CARD_COUNTER = 0

# task configuration
#SHAPE_LIST = ["square", "triangle", "circle"]
SHAPE_IMAGE_LIST = []
for i in range(13):
    letter = chr(i+97)
    SHAPE_IMAGE_LIST.append("images/point_" + letter + ".png")
BAD_CARD_IMAGE = "images/lose_all.png"
MAX_PUMPS = [8, 32, 128]  # three risk types
REPETITIONS = 30  # repetitions of risk
REWARD = 1

# keys
KEY_PUMP = 'space'
KEY_NEXT = 'return'
KEY_QUIT = 'escape'

# messages
ABSENT_MESSAGE = 'You\'ve waited to long! Your temporary earnings are lost.'
FINAL_MESSAGE = 'Well done! You banked a total of {:d}. Thank you for your participation.'


# global objects

# create window
win = visual.Window(
    size=(WIN_WIDTH, WIN_HEIGHT),
    units='pixels',
    #color='Black',
    fullscr=False
)

card_base = visual.Rect(
    win=win, name='polygon',
    width=(0.4, 0.5)[0], height=(0.4, 0.5)[1],
    ori=0.0, pos=(0, 0),
    lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
    opacity=None, depth=0.0, interpolate=True
)

shape_image = visual.ImageStim(
    win=win,
    name='image', 
    mask=None,
    ori=0.0, pos=(0, 0), size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-1.0
)

# stimulus
stim = visual.ImageStim(
    win,
    pos=(0, 0),
    units='pix',
    interpolate=True
)
# text
text = visual.TextStim(
    win,
    color='White',
    height=0.08,
    pos=(0.4, -0.9),
    alignText='right',
    units='norm',
    anchorHoriz='center',
    anchorVert='bottom'
)
remind_return = visual.TextStim(
    win,
    color='White',
    height=0.08,
    pos=(-0.2, -0.9),
    alignText='right',
    units='norm',
    anchorHoriz='right',
    anchorVert='bottom'
)
remind_enter = visual.TextStim(
    win,
    color='White',
    height=0.08,
    pos=(0.2, -0.9),
    alignText='left',
    units='norm',
    anchorHoriz='left',
    anchorVert='bottom'
)

def createTrialHandler(shapeList, maxPumps, REPETITIONS, REWARD):
    """Creates a TrialHandler based on colors of balloon and pop stimuli, repetitions of trials and reward value for
    each successful pump. CAVE: color_list and maxPumps must be lists of equal length."""
    # to import balloon and pop images of different colors
    # create trial list of dictionaries
    trialList = []
    for index in range(len(shapeList)):
        trialDef = {
            'shapeCard': shapeList[index],
            'maxPumps': maxPumps[index%3],
            'reward': REWARD
        }
        trialList.append(trialDef)
    # same order for all subjects
    random.seed(52472)
    trials = data.TrialHandler(
        trialList,
        nReps=REPETITIONS,
        method='fullRandom'
    )
    return trials

#change it either to direct text or tell Ramiro to make an image applicable to this experiment
def showInstruction(img, wait=30):
    """Show an instruction and wait for a response"""
    instruction = visual.ImageStim(
        win,
        image=img,
        pos=(0, 0),
        size=(2, 2),
        units='norm'
    )
    instruction.draw()
    win.flip()
    respond = event.waitKeys(
        keyList=[KEY_PUMP, KEY_QUIT],
        maxWait=wait
    )
    key = KEY_QUIT if not respond else respond[0]
    return key


def drawText(TextStim, pos, txt, alignment='right'):
    """Takes a PsychoPy TextStim and updates position and text before drawing the stimulus."""
    TextStim.pos = (pos)
    TextStim.setText(txt)
    TextStim.alignText = alignment
    TextStim.draw()


def showCard(img, wait=1):
    stim.setImage(img)
    card_base.setAutoDraw(True)
    stim.draw()
    win.flip()
    core.wait(wait)



#CHANGE TO CSV
def saveData(dataList):
    """"Saves all relevant data in txt file."""
    #changes to experiment handler
    #NOT IMPLEMENTED YET


def drawTrial(image, lastMoney, totalMoney):
    """Shows trial setup, i.e. reminders, stimulus, and account balance."""
    #stim.size = ballSize
    stim.setImage(image)
    card_base.setAutoDraw(True)
    stim.draw()
    #showCard(image)
    drawText(remind_return, (-0.23, -0.9),
             'Press ENTER\nto collect points', 'right')
    drawText(remind_enter, (0.23, -0.9),
             'Press SPACE\nto get a new card', 'left')
    drawText(text, (0.4, -0.6),
             'Last card deck: \n{:d}'.format(lastMoney))
    drawText(text, (0.4, -0.9),
             'Total Earned: \n{:d}'.format(round(totalMoney, 2)))
    win.flip()
    card_base.setAutoDraw(False)


def bart():
    """Execute experiment"""
    trials = createTrialHandler(SHAPE_IMAGE_LIST, MAX_PUMPS, REPETITIONS, REWARD)

    #if showInstruction('instructions.png') == KEY_QUIT:
     #   return

    permBank = 0
    lastTempBank = 0
    # iterate thorugh balloons
    for trialNumber, trial in enumerate(trials):

        # trial default settings
        tempBank = 0  # temporary bank
        pop = False
        nPumps = 0
        continuePumping = True
        increase = 0

        # pump balloon
        while continuePumping and not pop:

            counter = random.randint(0,2) 

            drawTrial(SHAPE_IMAGE_LIST[counter], lastTempBank, permBank)

            # process response
            respond = event.waitKeys(
                keyList=[KEY_PUMP, KEY_NEXT, KEY_QUIT],
                maxWait=15
            )

            # no response - continue to next balloon
            if not respond:
                drawText(
                    text, (0, 0), ABSENT_MESSAGE, 'center')
                win.flip()
                core.wait(5)
                continuePumping = False

            # escape key pressed
            elif respond[0] == KEY_QUIT:
                return

            # cash out key pressed
            elif respond[0] == KEY_NEXT:
                lastTempBank = tempBank

                # aninmation: count up to new balance
                #newBalance = permBank + tempBank
                #while round(permBank, 2) < round(newBalance, 2):
                 #   permBank += 0.01
                    #drawText(text, (0.4, -0.9),
                  #           'Total Earned:\n{:.2f}'.format(permBank))
                   # win.flip()
                permBank += tempBank
                drawText(text, (0.4, -0.9),
                             'Total Earned:\n{:d}'.format(permBank))
                continuePumping = False

            # pump key pressed
            elif respond[0] == KEY_PUMP:
                nPumps += 1

                # determine whether balloon pops or not
                if random.random() < 1.0 / (trial['maxPumps'] - nPumps):
                    #showImg(trial['pop_img'], POP_TEXTURE_SIZE)

                    #SHOW THE "BAD" CARD
                    #showImg(BAD_CARD)
                    showCard(BAD_CARD_IMAGE)
                    lastTempBank = 0
                    pop = True
                else:
                    tempBank += REWARD
                    # increase balloon size to fill up other 80%
                    increase += 0.8 / max(MAX_PUMPS)

    # final information about reward
    drawText(text, (0, 0),
             FINAL_MESSAGE.format(permBank), 'center')
    win.flip()
    core.wait(5)
    return


def main():
    # dialog for subject information
    #infoDlg = showInfoBox()
    #info = infoDlg.dictionary
    #if infoDlg.OK:
        # start experiment
     #   bart(info)

    bart()
    # quit experiment
    win.close()
    core.quit()


if __name__ == "__main__":
    main()
