import os
os.chdir("D:\Causal_Experiment Pilot\Behavioral Data\Scripts")  # Update with your folder path
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Causal Perception Working Memory Experiment (Simplified Version)
- 3 conditions (direct, intention, indirect causation)
- 10 trials per condition (30 total)
- Randomized trial order
- Focus on effect estimation and feasibility testing
"""

from psychopy import visual, core, data, event, logging, gui
import numpy as np
import random
import os
import pandas as pd
from datetime import datetime

# ======= EXPERIMENT SETTINGS =======
EXP_NAME = 'Causal Perception Working Memory'
SCREEN_SIZE = [1024, 768]
BACKGROUND_COLOR = 'gray'
N_TRIALS_PER_CONDITION = 10  # 10 trials per condition (30 total)

# Timing parameters (in seconds)
FIXATION_DURATION = 0.5
ANIMATION_DURATION = 3.0
INTERFERENCE_DURATION = 10.0
RESPONSE_TIMEOUT = 10.0
ITI = 1.0

# ======= MATH PROBLEMS =======
MATH_PROBLEMS = [
    "What is 9 * 2?",
    "What is 7 + 5?",
    "What is 12 - 4?",
    "What is 8 / 2?",
    "What is 5 + 3?",
    "What is 6 * 3?"
]

###############################################################################
# FORCE-CHOICE QUESTIONS (unchanged)
###############################################################################
def present_force_choice_questions(win, clock):
    q1_text = visual.TextStim(
        win=win,
        text="What happened?",
        font='Arial',
        pos=(0, 0.2),
        height=0.06,
        color='white'
    )
    q1_option1 = visual.TextStim(
        win=win,
        text="1) The brown ball moved the blue ball",
        font='Arial',
        pos=(0, 0),
        height=0.05,
        color='white'
    )
    q1_option2 = visual.TextStim(
        win=win,
        text="2) The brown ball made the blue ball move",
        font='Arial',
        pos=(0, -0.1),
        height=0.05,
        color='white'
    )
    q1_text.draw()
    q1_option1.draw()
    q1_option2.draw()
    win.flip()
    q1_timer = core.Clock()
    q1_response = None
    q1_rt = None
    event.clearEvents(eventType='keyboard')
    while q1_response is None:
        keys = event.getKeys(keyList=['1', '2', 'escape'])
        if 'escape' in keys:
            win.close()
            core.quit()
        if '1' in keys or '2' in keys:
            q1_response = 1 if '1' in keys else 2
            q1_rt = q1_timer.getTime()
            break
    q2_text = visual.TextStim(
        win=win,
        text="Was it a single \"Launching event\"?",
        font='Arial',
        pos=(0, 0.2),
        height=0.06,
        color='white'
    )
    q2_option1 = visual.TextStim(
        win=win,
        text="1) Yes",
        font='Arial',
        pos=(0, 0),
        height=0.05,
        color='white'
    )
    q2_option2 = visual.TextStim(
        win=win,
        text="2) No",
        font='Arial',
        pos=(0, -0.1),
        height=0.05,
        color='white'
    )
    q2_text.draw()
    q2_option1.draw()
    q2_option2.draw()
    win.flip()
    q2_timer = core.Clock()
    q2_response = None
    q2_rt = None
    event.clearEvents(eventType='keyboard')
    while q2_response is None:
        keys = event.getKeys(keyList=['1', '2', 'escape'])
        if 'escape' in keys:
            win.close()
            core.quit()
        if '1' in keys or '2' in keys:
            q2_response = 1 if '1' in keys else 2
            q2_rt = q2_timer.getTime()
            break
    win.flip()
    core.wait(0.5)
    return {
        'ball_moved_or_made_move': q1_response,
        'ball_moved_or_made_move_rt': q1_rt,
        'launching_event': q2_response,
        'launching_event_rt': q2_rt
    }

###############################################################################
# SETUP EXPERIMENT
###############################################################################
def setup_experiment():
    exp_info = {
        'participant': '', 
        'session': '001',
        'task': ['change_detection', 'probe_recognition'],
    }
    dlg = gui.DlgFromDict(dictionary=exp_info, title=EXP_NAME)
    if not dlg.OK:
        core.quit()
    data_folder = os.path.join(os.getcwd(), 'data')
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    date_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(data_folder, f"P{exp_info['participant']}_{exp_info['task']}_{date_string}")
    win = visual.Window(
        size=SCREEN_SIZE,
        fullscr=False,
        screen=0,
        allowGUI=False,
        allowStencil=False,
        monitor='testMonitor',
        color=BACKGROUND_COLOR,
        colorSpace='rgb',
        blendMode='avg',
        useFBO=True
    )
    logging.console.setLevel(logging.WARNING)
    return win, filename, exp_info

###############################################################################
# CREATE STIMULI (with consistent border created once)
###############################################################################
def create_stimuli(win):
    fixation = visual.TextStim(
        win=win,
        name='fixation',
        text='+',
        font='Arial',
        pos=(0, 0),
        height=0.05,
        color='white'
    )
    ball_a_normal = visual.Circle(
        win=win,
        name='ball_a',
        radius=0.05,
        edges=32,
        pos=(-0.4, 0),
        fillColor='red'
    )
    ball_a_face = visual.Circle(
        win=win,
        name='ball_a_face',
        radius=0.05,
        edges=32,
        pos=(-0.4, 0),
        fillColor='red'
    )
    face_components = {
        'left_eye': visual.Circle(
            win=win,
            radius=0.01,
            edges=32,
            pos=(-0.4-0.02, 0.02),
            fillColor='black'
        ),
        'right_eye': visual.Circle(
            win=win,
            radius=0.01,
            edges=32,
            pos=(-0.4+0.02, 0.02),
            fillColor='black'
        ),
        'mouth': visual.ShapeStim(
            win=win,
            vertices=[[-0.4-0.02, -0.02], [-0.4, -0.03], [-0.4+0.02, -0.02]],
            closeShape=False,
            lineWidth=2,
            lineColor='black'
        ),
        'thought_bubble': visual.Circle(
            win=win,
            radius=0.03,
            edges=32,
            pos=(-0.3, 0.1),
            lineColor='black',
            fillColor='white',
            opacity=0.7
        )
    }
    goal_in_thought = visual.Rect(
        win=win,
        width=0.02,
        height=0.02,
        pos=(-0.3, 0.1),
        lineColor='black'
    )
    ball_b = visual.Circle(
        win=win,
        name='ball_b',
        radius=0.05,
        edges=32,
        pos=(0, 0),
        fillColor='blue'
    )
    lever = visual.Rect(
        win=win,
        name='lever',
        width=0.02,
        height=0.2,
        pos=(-0.15, 0),
        fillColor='brown'
    )
    goal = visual.Rect(
        win=win,
        name='goal',
        width=0.1,
        height=0.2,
        pos=(0.4, 0),
        lineColor='black'
    )
    background_elements = [
        visual.Rect(
            win=win,
            width=0.05,
            height=0.05,
            pos=(0.3, 0.3),
            fillColor='lightgray'
        ),
        visual.Circle(
            win=win,
            radius=0.04,
            pos=(-0.3, -0.3),
            fillColor='lightgray'
        ),
        visual.ShapeStim(
            win=win,
            vertices=[[0.2, -0.3], [0.3, -0.35], [0.25, -0.25]],
            fillColor='lightgray'
        )
    ]
    interference_numbers = visual.TextStim(
        win=win,
        name='interference_numbers',
        text="",
        font='Arial',
        pos=(0, 0),
        height=0.1,
        color='white'
    )
    n_elements = 400
    xys = []
    colors = []
    for x in range(-10, 10):
        for y in range(-10, 10):
            xys.append([x/10, y/10])
            gray_val = random.uniform(0, 1)
            colors.append([gray_val, gray_val, gray_val])
    visual_noise = visual.ElementArrayStim(
        win=win,
        name='visual_noise',
        nElements=n_elements,
        elementTex=None,
        elementMask='circle',
        xys=xys,
        sizes=0.05,
        colors=colors,
        opacities=0.5
    )
    number_recall_response = visual.TextStim(
        win=win,
        name='number_recall_response',
        text="Enter the numbers you saw:",
        font='Arial',
        pos=(0, 0.1),
        height=0.05,
        color='white'
    )
    number_recall_input = visual.TextStim(
        win=win,
        name='number_recall_input',
        text='',
        font='Arial',
        pos=(0, -0.1),
        height=0.05,
        color='white'
    )
    number_recall_submit = visual.Rect(
        win=win,
        name='number_recall_submit',
        width=0.2,
        height=0.1,
        pos=(0, -0.3),
        lineColor='white',
        fillColor='darkgray'
    )
    number_recall_submit_text = visual.TextStim(
        win=win,
        name='number_recall_submit_text',
        text="Submit",
        font='Arial',
        pos=(0, -0.3),
        height=0.05,
        color='white'
    )
    change_detection_question = visual.TextStim(
        win=win,
        name='change_detection_question',
        text="Did you notice any change in the animation?\n1 = Identical\n2 = Different",
        font='Arial',
        pos=(0, 0),
        height=0.05,
        color='white'
    )
    confidence_rating_text = visual.TextStim(
        win=win,
        name='confidence_rating_text',
        text="How confident are you in your response?\n1 = Not confident at all\n5 = Very confident",
        font='Arial',
        pos=(0, 0.3),
        height=0.05,
        color='white'
    )
    confidence_buttons = []
    confidence_labels = []
    for i in range(5):
        confidence_buttons.append(
            visual.Rect(
                win=win,
                name=f'confidence_button_{i+1}',
                width=0.1,
                height=0.1,
                pos=(-0.4 + i * 0.2, 0),
                lineColor='white',
                fillColor='darkgray'
            )
        )
        confidence_labels.append(
            visual.TextStim(
                win=win,
                name=f'confidence_label_{i+1}',
                text=str(i+1),
                font='Arial',
                pos=(-0.4 + i * 0.2, 0),
                height=0.05,
                color='white'
            )
        )
    probe_frame = visual.Rect(
        win=win,
        name='probe_frame',
        width=0.8,
        height=0.6,
        pos=(0, 0),
        lineColor='white'
    )
    probe_recognition_question = visual.TextStim(
        win=win,
        name='probe_recognition_question',
        text="Was this frame part of the animation you just saw?\n1 = Yes\n2 = No",
        font='Arial',
        pos=(0, -0.4),
        height=0.05,
        color='white'
    )
    instructions = visual.TextStim(
        win=win,
        name='instructions',
        text="",
        font='Arial',
        pos=(0, 0),
        height=0.05,
        color='white'
    )
    trial_counter = visual.TextStim(
        win=win,
        name='trial_counter',
        text="Trial 0 of 30",
        font='Arial',
        pos=(0, 0.45),
        height=0.04,
        color='white'
    )
    # Create the border once; it will be drawn on every frame in each animation.
    animation_border = visual.Rect(
        win=win,
        name='animation_border',
        width=1.0,
        height=0.6,
        pos=(0, 0),
        lineWidth=3,
        lineColor='white',
        fillColor=None,
        opacity=1.0
    )
    
    return {
        'fixation': fixation,
        'ball_a_normal': ball_a_normal,
        'ball_a_face': ball_a_face,
        'face_components': face_components,
        'ball_b': ball_b,
        'lever': lever,
        'goal': goal,
        'background_elements': background_elements,
        'goal_in_thought': goal_in_thought,
        'instructions': instructions,
        'trial_counter': trial_counter,
        'interference_numbers': interference_numbers,
        'visual_noise': visual_noise,
        'number_recall_response': number_recall_response,
        'number_recall_input': number_recall_input,
        'number_recall_submit': number_recall_submit,
        'number_recall_submit_text': number_recall_submit_text,
        'change_detection_question': change_detection_question,
        'confidence_rating_text': confidence_rating_text,
        'confidence_buttons': confidence_buttons,
        'confidence_labels': confidence_labels,
        'probe_frame': probe_frame,
        'probe_recognition_question': probe_recognition_question,
        'animation_border': animation_border
    }

###############################################################################
# CREATE TRIAL SEQUENCE (unchanged)
###############################################################################
def create_trial_sequence(task_type, n_trials_per_condition):
    conditions = [
        {'condition': 'direct', 'id': 1},
        {'condition': 'intention', 'id': 2},
        {'condition': 'indirect', 'id': 3}
    ]
    all_trials = []
    if task_type == 'change_detection':
        for condition in conditions:
            n_identical = n_trials_per_condition // 3
            n_causal_critical = n_trials_per_condition // 3
            n_causal_peripheral = n_trials_per_condition - n_identical - n_causal_critical
            for _ in range(n_identical):
                trial_info = condition.copy()
                trial_info['change_type'] = 'identical'
                trial_info['correct_response'] = 1
                all_trials.append(trial_info)
            for _ in range(n_causal_critical):
                trial_info = condition.copy()
                trial_info['change_type'] = 'causal_critical'
                trial_info['correct_response'] = 2
                all_trials.append(trial_info)
            for _ in range(n_causal_peripheral):
                trial_info = condition.copy()
                trial_info['change_type'] = 'causal_peripheral'
                trial_info['correct_response'] = 2
                all_trials.append(trial_info)
    else:
        for condition in conditions:
            n_junction_frames = n_trials_per_condition // 3
            n_non_junction_frames = n_trials_per_condition // 3
            n_novel_frames = n_trials_per_condition - n_junction_frames - n_non_junction_frames
            for _ in range(n_junction_frames):
                trial_info = condition.copy()
                trial_info['frame_type'] = 'causal_junction'
                trial_info['correct_response'] = 1
                all_trials.append(trial_info)
            for _ in range(n_non_junction_frames):
                trial_info = condition.copy()
                trial_info['frame_type'] = 'non_junction'
                trial_info['correct_response'] = 1
                all_trials.append(trial_info)
            for _ in range(n_novel_frames):
                trial_info = condition.copy()
                trial_info['frame_type'] = 'novel'
                trial_info['correct_response'] = 2
                all_trials.append(trial_info)
    random.shuffle(all_trials)
    for i, trial in enumerate(all_trials):
        trial['trial_number'] = i + 1
    if task_type == 'change_detection':
        data_types = [
            'trial_number', 'condition', 'change_type', 'correct_response', 
            'response', 'rt', 'accuracy', 
            'confidence', 'confidence_rt'
        ]
    else:
        data_types = [
            'trial_number', 'condition', 'frame_type', 'correct_response', 
            'response', 'rt', 'accuracy', 
            'confidence', 'confidence_rt'
        ]
    trials = data.TrialHandler(
        all_trials,
        nReps=1,
        method='sequential',
        dataTypes=data_types,
        name='trials'
    )
    return trials

###############################################################################
# ANIMATION FUNCTIONS (with consistent border drawn on every frame)
###############################################################################
def animate_direct_causation(win, stimuli, clock, change_type=None):
    ball_a = stimuli['ball_a_normal']
    ball_b = stimuli['ball_b']
    goal = stimuli['goal']
    background_elements = stimuli['background_elements']
    ball_a.pos = (-0.4, 0)
    ball_b.pos = (0, 0)
    if change_type == 'causal_critical':
        ball_a_endpoint = -0.1
    elif change_type == 'causal_peripheral':
        background_elements[0].fillColor = 'darkgray'
    else:
        ball_a_endpoint = 0
    # Always draw the border
    stimuli['animation_border'].draw()
    for element in background_elements:
        element.draw()
    ball_a.draw()
    ball_b.draw()
    goal.draw()
    win.flip()
    core.wait(0.5)
    animation_steps = 60
    step_time = ANIMATION_DURATION / animation_steps
    start_time = clock.getTime()
    for step in range(animation_steps // 2):
        t = step / (animation_steps // 2)
        if change_type == 'causal_critical':
            ball_a.pos = (-0.4 + 0.3 * t, 0)
        else:
            ball_a.pos = (-0.4 + 0.4 * t, 0)
        stimuli['animation_border'].draw()  # Draw border every frame
        for element in background_elements:
            element.draw()
        ball_a.draw()
        ball_b.draw()
        goal.draw()
        win.flip()
        elapsed = clock.getTime() - start_time
        target_time = step * step_time
        if elapsed < target_time:
            core.wait(target_time - elapsed)
    collision_time = clock.getTime()
    for step in range(animation_steps // 2):
        t = step / (animation_steps // 2)
        if change_type != 'causal_critical':
            ball_b.pos = (0 + 0.4 * t, 0)
        stimuli['animation_border'].draw()
        for element in background_elements:
            element.draw()
        ball_a.draw()
        ball_b.draw()
        goal.draw()
        win.flip()
        elapsed = clock.getTime() - collision_time
        target_time = step * step_time
        if elapsed < target_time:
            core.wait(target_time - elapsed)
    stimuli['animation_border'].draw()
    for element in background_elements:
        element.draw()
    ball_a.draw()
    ball_b.draw()
    goal.draw()
    win.flip()
    core.wait(0.5)
    frames = {'causal_junction': [], 'non_junction': []}
    frames['causal_junction'].append({'time': animation_steps // 2})
    frames['causal_junction'].append({'time': (animation_steps // 2) + 1})
    frames['non_junction'].append({'time': 0})
    frames['non_junction'].append({'time': animation_steps - 1})
    return frames

def animate_intention_causation(win, stimuli, clock, change_type=None):
    ball_a = stimuli['ball_a_face']
    ball_b = stimuli['ball_b']
    lever = stimuli['lever']
    goal = stimuli['goal']
    face_components = stimuli['face_components']
    thought_bubble = stimuli['face_components']['thought_bubble']
    goal_in_thought = stimuli['goal_in_thought']
    background_elements = stimuli['background_elements']
    ball_a.pos = (-0.4, 0)
    lever.pos = (-0.15, 0)
    lever.ori = 0
    ball_b.pos = (0, 0)
    face_components['left_eye'].pos = (-0.4-0.02, 0.02)
    face_components['right_eye'].pos = (-0.4+0.02, 0.02)
    face_components['mouth'].vertices = [[-0.4-0.02, -0.02], [-0.4, -0.03], [-0.4+0.02, -0.02]]
    thought_bubble.pos = (-0.3, 0.1)
    goal_in_thought.pos = (-0.3, 0.1)
    if change_type == 'causal_critical':
        show_thought_bubble = False
    elif change_type == 'causal_peripheral':
        face_components['mouth'].vertices = [[-0.4-0.02, -0.01], [-0.4, -0.01], [-0.4+0.02, -0.01]]
        show_thought_bubble = True
    else:
        show_thought_bubble = True
    # Draw border on initial state
    stimuli['animation_border'].draw()
    for element in background_elements:
        element.draw()
    ball_a.draw()
    for comp in face_components.values():
        comp.draw()
    if show_thought_bubble:
        goal_in_thought.draw()
    lever.draw()
    ball_b.draw()
    goal.draw()
    win.flip()
    core.wait(0.5)
    animation_steps = 90
    step_time = ANIMATION_DURATION / animation_steps
    start_time = clock.getTime()
    for step in range(animation_steps // 3):
        t = step / (animation_steps // 3)
        new_x = -0.4 + 0.25 * t
        ball_a.pos = (new_x, 0)
        face_components['left_eye'].pos = (new_x-0.02, 0.02)
        face_components['right_eye'].pos = (new_x+0.02, 0.02)
        face_components['mouth'].vertices = [[new_x-0.02, -0.02 if change_type != 'causal_peripheral' else -0.01],
                                             [new_x, -0.03 if change_type != 'causal_peripheral' else -0.01],
                                             [new_x+0.02, -0.02 if change_type != 'causal_peripheral' else -0.01]]
        face_components['thought_bubble'].pos = (new_x+0.1, 0.1)
        goal_in_thought.pos = (new_x+0.1, 0.1)
        stimuli['animation_border'].draw()  # draw border every frame
        for element in background_elements:
            element.draw()
        ball_a.draw()
        for comp in face_components.values():
            comp.draw()
        if show_thought_bubble:
            goal_in_thought.draw()
        lever.draw()
        ball_b.draw()
        goal.draw()
        win.flip()
        elapsed = clock.getTime() - start_time
        target_time = step * step_time
        if elapsed < target_time:
            core.wait(target_time - elapsed)
    lever_time = clock.getTime()
    for step in range(animation_steps // 3):
        t = step / (animation_steps // 3)
        lever_angle = 45 * t
        lever.ori = lever_angle
        stimuli['animation_border'].draw()
        for element in background_elements:
            element.draw()
        ball_a.draw()
        for comp in face_components.values():
            comp.draw()
        if show_thought_bubble:
            goal_in_thought.draw()
        lever.draw()
        ball_b.draw()
        goal.draw()
        win.flip()
        elapsed = clock.getTime() - lever_time
        target_time = step * step_time
        if elapsed < target_time:
            core.wait(target_time - elapsed)
    ball_b_time = clock.getTime()
    for step in range(animation_steps // 3):
        t = step / (animation_steps // 3)
        ball_b.pos = (0 + 0.4 * t, 0)
        stimuli['animation_border'].draw()
        for element in background_elements:
            element.draw()
        ball_a.draw()
        for comp in face_components.values():
            comp.draw()
        lever.draw()
        ball_b.draw()
        goal.draw()
        win.flip()
        elapsed = clock.getTime() - ball_b_time
        target_time = step * step_time
        if elapsed < target_time:
            core.wait(target_time - elapsed)
    stimuli['animation_border'].draw()
    for element in background_elements:
        element.draw()
    ball_a.draw()
    for comp in face_components.values():
        comp.draw()
    lever.draw()
    ball_b.draw()
    goal.draw()
    win.flip()
    core.wait(0.5)
    frames = {'causal_junction': [], 'non_junction': []}
    frames['causal_junction'].append({'time': animation_steps // 3})
    frames['causal_junction'].append({'time': 2 * (animation_steps // 3)})
    frames['non_junction'].append({'time': 0})
    frames['non_junction'].append({'time': animation_steps - 1})
    return frames

def animate_indirect_causation(win, stimuli, clock, change_type=None):
    ball_a = stimuli['ball_a_normal']
    ball_b = stimuli['ball_b']
    lever = stimuli['lever']
    goal = stimuli['goal']
    background_elements = stimuli['background_elements']
    ball_a.pos = (-0.4, 0)
    lever.pos = (-0.15, 0)
    lever.ori = 0
    ball_b.pos = (0, 0)
    if change_type == 'causal_critical':
        max_lever_angle = 20
    elif change_type == 'causal_peripheral':
        ball_a.fillColor = 'darkred'
        max_lever_angle = 45
    else:
        max_lever_angle = 45
    stimuli['animation_border'].draw()
    for element in background_elements:
        element.draw()
    ball_a.draw()
    lever.draw()
    ball_b.draw()
    goal.draw()
    win.flip()
    core.wait(0.5)
    animation_steps = 90
    step_time = ANIMATION_DURATION / animation_steps
    start_time = clock.getTime()
    for step in range(animation_steps // 3):
        t = step / (animation_steps // 3)
        ball_a.pos = (-0.4 + 0.25 * t, 0)
        stimuli['animation_border'].draw()
        for element in background_elements:
            element.draw()
        ball_a.draw()
        lever.draw()
        ball_b.draw()
        goal.draw()
        win.flip()
        elapsed = clock.getTime() - start_time
        target_time = step * step_time
        if elapsed < target_time:
            core.wait(target_time - elapsed)
    lever_time = clock.getTime()
    for step in range(animation_steps // 3):
        t = step / (animation_steps // 3)
        lever_angle = max_lever_angle * t
        lever.ori = lever_angle
        stimuli['animation_border'].draw()
        for element in background_elements:
            element.draw()
        ball_a.draw()
        lever.draw()
        ball_b.draw()
        goal.draw()
        win.flip()
        elapsed = clock.getTime() - lever_time
        target_time = step * step_time
        if elapsed < target_time:
            core.wait(target_time - elapsed)
    ball_b_time = clock.getTime()
    for step in range(animation_steps // 3):
        t = step / (animation_steps // 3)
        if change_type != 'causal_critical':
            ball_b.pos = (0 + 0.4 * t, 0)
        stimuli['animation_border'].draw()
        for element in background_elements:
            element.draw()
        ball_a.draw()
        lever.draw()
        ball_b.draw()
        goal.draw()
        win.flip()
        elapsed = clock.getTime() - ball_b_time
        target_time = step * step_time
        if elapsed < target_time:
            core.wait(target_time - elapsed)
    stimuli['animation_border'].draw()
    for element in background_elements:
        element.draw()
    ball_a.draw()
    lever.draw()
    ball_b.draw()
    goal.draw()
    win.flip()
    core.wait(0.5)
    frames = {'causal_junction': [], 'non_junction': []}
    frames['causal_junction'].append({'time': animation_steps // 3})
    frames['causal_junction'].append({'time': 2 * (animation_steps // 3)})
    frames['non_junction'].append({'time': 0})
    frames['non_junction'].append({'time': animation_steps - 1})
    return frames

###############################################################################
# INTERFERENCE TASK - SELF-PACED MATH & RECALL
###############################################################################
def present_interference_task(win, stimuli, clock):
    # 1) Show a random 5-digit number for 2 seconds.
    num_sequence = ''.join([str(random.randint(0, 9)) for _ in range(5)])
    stimuli['interference_numbers'].text = num_sequence
    stimuli['interference_numbers'].draw()
    win.flip()
    core.wait(2.0)
    # 2) Show visual noise for 1 second.
    stimuli['visual_noise'].draw()
    win.flip()
    core.wait(1.0)
    # 3) Present TWO math problems, self-paced.
    math_problems = random.sample(MATH_PROBLEMS, 2)
    math_answers = []
    for problem in math_problems:
        question_text = visual.TextStim(
            win=win,
            text=problem,
            font='Arial',
            pos=(0, 0.2),
            height=0.06,
            color='white'
        )
        answer_prompt = visual.TextStim(
            win=win,
            text="Type your answer, then press Enter or click Submit:",
            font='Arial',
            pos=(0, 0),
            height=0.05,
            color='white'
        )
        answer_box = visual.TextStim(
            win=win,
            text='',
            font='Arial',
            pos=(0, -0.1),
            height=0.05,
            color='white'
        )
        submit_button = stimuli['number_recall_submit']
        submit_button_text = stimuli['number_recall_submit_text']
        typed_answer = ""
        event.clearEvents()
        while True:
            question_text.draw()
            answer_prompt.draw()
            answer_box.text = typed_answer
            answer_box.draw()
            submit_button.draw()
            submit_button_text.draw()
            win.flip()
            keys = event.getKeys()
            mouse = event.Mouse()
            if 'escape' in keys:
                win.close()
                core.quit()
            for key in keys:
                if key in ['0','1','2','3','4','5','6','7','8','9']:
                    typed_answer += key
                elif key == 'backspace':
                    typed_answer = typed_answer[:-1]
                elif key == 'return':
                    math_answers.append(typed_answer)
                    typed_answer = ""
                    break
            if 'return' in keys:
                break
            if mouse.isPressedIn(submit_button):
                math_answers.append(typed_answer)
                break
    # 4) Number recall: Wait until participant types their recalled number and submits.
    stimuli['number_recall_response'].draw()
    stimuli['number_recall_input'].draw()
    stimuli['number_recall_submit'].draw()
    stimuli['number_recall_submit_text'].draw()
    win.flip()
    recall_response = ""
    event.clearEvents()
    while True:
        keys = event.getKeys()
        mouse = event.Mouse()
        if 'escape' in keys:
            win.close()
            core.quit()
        for key in keys:
            if key in ['0','1','2','3','4','5','6','7','8','9']:
                recall_response += key
            elif key == 'backspace':
                recall_response = recall_response[:-1]
            elif key == 'return':
                break
        if 'return' in keys:
            break
        if mouse.isPressedIn(stimuli['number_recall_submit']):
            break
        stimuli['number_recall_input'].text = recall_response
        stimuli['number_recall_response'].draw()
        stimuli['number_recall_input'].draw()
        stimuli['number_recall_submit'].draw()
        stimuli['number_recall_submit_text'].draw()
        win.flip()
    recall_correct = (recall_response == num_sequence)
    win.flip()
    core.wait(0.5)
    return recall_correct, num_sequence, recall_response, math_answers

###############################################################################
# TASK FUNCTIONS
###############################################################################
def run_change_detection_trial(win, stimuli, condition, clock, trial_number):
    stimuli['trial_counter'].text = f"Trial {trial_number} of 30"
    stimuli['trial_counter'].draw()
    win.flip()
    core.wait(0.5)
    stimuli['fixation'].draw()
    win.flip()
    core.wait(FIXATION_DURATION)
    change_type = condition.get('change_type', None)
    if condition['condition'] == 'direct':
        animate_direct_causation(win, stimuli, clock)
    elif condition['condition'] == 'intention':
        animate_intention_causation(win, stimuli, clock)
    else:
        animate_indirect_causation(win, stimuli, clock)
    recall_correct, num_shown, num_recalled, math_answers = present_interference_task(win, stimuli, clock)
    if condition['condition'] == 'direct':
        animate_direct_causation(win, stimuli, clock, change_type)
    elif condition['condition'] == 'intention':
        animate_intention_causation(win, stimuli, clock, change_type)
    else:
        animate_indirect_causation(win, stimuli, clock, change_type)
    stimuli['change_detection_question'].draw()
    win.flip()
    response_timer = core.Clock()
    response = None
    rt = None
    event.clearEvents(eventType='keyboard')
    while response is None:
        keys = event.getKeys(keyList=['1', '2', 'escape'])
        if 'escape' in keys:
            win.close()
            core.quit()
        if '1' in keys or '2' in keys:
            response = 1 if '1' in keys else 2
            rt = response_timer.getTime()
            break
    accuracy = 1 if response == condition['correct_response'] else 0
    stimuli['confidence_rating_text'].draw()
    for button, label in zip(stimuli['confidence_buttons'], stimuli['confidence_labels']):
        button.draw()
        label.draw()
    win.flip()
    confidence_timer = core.Clock()
    confidence = None
    confidence_rt = None
    event.clearEvents(eventType='keyboard')
    while confidence is None:
        keys = event.getKeys(keyList=['1','2','3','4','5','escape'])
        if 'escape' in keys:
            win.close()
            core.quit()
        if any(key in keys for key in ['1','2','3','4','5']):
            for i, key in enumerate(['1','2','3','4','5']):
                if key in keys:
                    confidence = i + 1
                    break
            confidence_rt = confidence_timer.getTime()
            break
        mouse = event.Mouse()
        for i, button in enumerate(stimuli['confidence_buttons']):
            if mouse.isPressedIn(button):
                confidence = i + 1
                confidence_rt = confidence_timer.getTime()
                break
        if confidence is not None:
            break
    forced_choice_results = present_force_choice_questions(win, clock)
    win.flip()
    core.wait(ITI)
    results = {
        'response': response,
        'rt': rt,
        'accuracy': accuracy,
        'confidence': confidence,
        'confidence_rt': confidence_rt,
        'recall_correct': recall_correct,
        'num_shown': num_shown,
        'num_recalled': num_recalled,
        'math_answers': math_answers
    }
    results.update(forced_choice_results)
    return results

def run_probe_recognition_trial(win, stimuli, condition, clock, trial_number):
    stimuli['trial_counter'].text = f"Trial {trial_number} of 30"
    stimuli['trial_counter'].draw()
    win.flip()
    core.wait(0.5)
    stimuli['fixation'].draw()
    win.flip()
    core.wait(FIXATION_DURATION)
    frames = None
    if condition['condition'] == 'direct':
        frames = animate_direct_causation(win, stimuli, clock)
    elif condition['condition'] == 'intention':
        frames = animate_intention_causation(win, stimuli, clock)
    else:
        frames = animate_indirect_causation(win, stimuli, clock)
    recall_correct, num_shown, num_recalled, math_answers = present_interference_task(win, stimuli, clock)
    frame_type = condition.get('frame_type', None)
    if frame_type == 'causal_junction':
        if condition['condition'] == 'direct':
            ball_a = stimuli['ball_a_normal']
            ball_b = stimuli['ball_b']
            ball_a.pos = (0, 0)
            ball_b.pos = (0.1, 0)
        elif condition['condition'] == 'intention':
            ball_a = stimuli['ball_a_face']
            lever = stimuli['lever']
            ball_a.pos = (-0.15, 0)
            lever.ori = 15
        else:
            lever = stimuli['lever']
            ball_b = stimuli['ball_b']
            lever.ori = 30
            ball_b.pos = (0.05, 0)
    elif frame_type == 'non_junction':
        if condition['condition'] == 'direct':
            ball_a = stimuli['ball_a_normal']
            ball_b = stimuli['ball_b']
            ball_a.pos = (-0.2, 0)
            ball_b.pos = (0, 0)
        elif condition['condition'] == 'intention':
            ball_a = stimuli['ball_a_face']
            ball_a.pos = (-0.4, 0)
        else:
            ball_b = stimuli['ball_b']
            ball_b.pos = (0.3, 0)
    elif frame_type == 'novel':
        if condition['condition'] == 'direct':
            ball_a = stimuli['ball_a_normal']
            ball_b = stimuli['ball_b']
            ball_a.pos = (0.2, 0.2)
            ball_b.pos = (-0.2, -0.2)
        elif condition['condition'] == 'intention':
            lever = stimuli['lever']
            lever.ori = 90
        else:
            ball_b = stimuli['ball_b']
            ball_b.pos = (0.3, 0.2)
    stimuli['probe_frame'].draw()
    for element in stimuli['background_elements']:
        element.draw()
    if condition['condition'] == 'direct':
        stimuli['ball_a_normal'].draw()
        stimuli['ball_b'].draw()
    elif condition['condition'] == 'intention':
        stimuli['ball_a_face'].draw()
        for comp in stimuli['face_components'].values():
            comp.draw()
        stimuli['lever'].draw()
        stimuli['ball_b'].draw()
    else:
        stimuli['ball_a_normal'].draw()
        stimuli['lever'].draw()
        stimuli['ball_b'].draw()
    stimuli['goal'].draw()
    stimuli['probe_recognition_question'].draw()
    win.flip()
    response_timer = core.Clock()
    response = None
    rt = None
    event.clearEvents(eventType='keyboard')
    while True:
        keys = event.getKeys(keyList=['1', '2', 'escape'])
        if 'escape' in keys:
            win.close()
            core.quit()
        if '1' in keys or '2' in keys:
            response = 1 if '1' in keys else 2
            rt = response_timer.getTime()
            break
    accuracy = 1 if response == condition['correct_response'] else 0
    stimuli['confidence_rating_text'].draw()
    for button, label in zip(stimuli['confidence_buttons'], stimuli['confidence_labels']):
        button.draw()
        label.draw()
    win.flip()
    confidence_timer = core.Clock()
    confidence = None
    confidence_rt = None
    event.clearEvents(eventType='keyboard')
    while True:
        keys = event.getKeys(keyList=['1','2','3','4','5','escape'])
        if 'escape' in keys:
            win.close()
            core.quit()
        if any(k in keys for k in ['1','2','3','4','5']):
            for i, k_ in enumerate(['1','2','3','4','5']):
                if k_ in keys:
                    confidence = i+1
                    break
            confidence_rt = confidence_timer.getTime()
            break
        mouse = event.Mouse()
        for i, button in enumerate(stimuli['confidence_buttons']):
            if mouse.isPressedIn(button):
                confidence = i + 1
                confidence_rt = confidence_timer.getTime()
                break
        if confidence is not None:
            break
    forced_choice_results = present_force_choice_questions(win, clock)
    win.flip()
    core.wait(ITI)
    results = {
        'response': response,
        'rt': rt,
        'accuracy': accuracy,
        'confidence': confidence,
        'confidence_rt': confidence_rt,
        'recall_correct': recall_correct,
        'num_shown': num_shown,
        'num_recalled': num_recalled,
        'math_answers': math_answers
    }
    results.update(forced_choice_results)
    return results

###############################################################################
# MAIN EXPERIMENT
###############################################################################
def run_experiment():
    win, filename, exp_info = setup_experiment()
    stimuli = create_stimuli(win)
    if exp_info['task'] == 'change_detection':
        instructions_text = (
            "In this experiment, you will see animations of balls moving.\n\n"
            "You will see each animation twice, with a brief task in between.\n\n"
            "Your job is to determine if the second animation is IDENTICAL to or DIFFERENT from the first.\n\n"
            "After each response, you'll rate your confidence from 1-5.\n\n"
            "There will be 30 trials total.\n\n"
            "Press spacebar to start."
        )
    else:
        instructions_text = (
            "In this experiment, you will see animations of balls moving.\n\n"
            "After each animation and a brief task, you will see a still frame.\n\n"
            "Your job is to determine if the frame was part of the animation you just saw.\n\n"
            "After each response, you'll rate your confidence from 1-5.\n\n"
            "There will be 30 trials total.\n\n"
            "Press spacebar to start."
        )
    stimuli['instructions'].text = instructions_text
    trials = create_trial_sequence(exp_info['task'], N_TRIALS_PER_CONDITION)
    exp_clock = core.Clock()
    stimuli['instructions'].draw()
    win.flip()
    event.clearEvents(eventType='keyboard')
    while True:
        if 'space' in event.getKeys(keyList=['space', 'escape']):
            break
        elif 'escape' in event.getKeys():
            win.close()
            core.quit()
    for trial in trials:
        trial_number = trial['trial_number']
        condition = trial
        if exp_info['task'] == 'change_detection':
            results = run_change_detection_trial(win, stimuli, condition, exp_clock, trial_number)
        else:
            results = run_probe_recognition_trial(win, stimuli, condition, exp_clock, trial_number)
        for key, value in results.items():
            trials.addData(key, value)
        try:
            trials.saveAsExcel(filename + '.xlsx', sheetName='data', dataOut=['all_raw'])
            print(f"Successfully saved data after trial {trial_number}")
        except Exception as e:
            print(f"Warning: Could not save data on trial {trial_number}. Error: {str(e)}")
            try:
                thisExp = data.ExperimentHandler(name=EXP_NAME, extraInfo=exp_info, dataFileName=filename)
                thisExp.addData('trial_number', trial_number)
                thisExp.addData('condition', condition['condition'])
                for k, v in results.items():
                    thisExp.addData(k, v)
                thisExp.nextEntry()
                thisExp.saveAsWideText(filename + '_backup.csv')
                print(f"Saved current trial data to backup file")
            except Exception as e2:
                print(f"Warning: Backup save also failed. Error: {str(e2)}")
        if trial_number % 10 == 0 and trial_number < 30:
            break_text = f"You've completed {trial_number} of 30 trials.\nTake a short break if needed.\n\nPress spacebar when ready to continue."
            break_stim = visual.TextStim(win, text=break_text, height=0.05, pos=(0,0), color='white')
            break_stim.draw()
            win.flip()
            event.clearEvents()
            while True:
                if 'space' in event.getKeys(keyList=['space', 'escape']):
                    break
                elif 'escape' in event.getKeys():
                    win.close()
                    core.quit()
    try:
        try:
            import openpyxl
            data_df = pd.read_excel(filename + '.xlsx')
            print("Successfully read data from Excel file for summary statistics")
        except Exception as e:
            print(f"Could not read Excel data file. Error: {str(e)}")
            data_df = pd.DataFrame({
                'condition': [t['condition'] for t in trials.trialList],
                'accuracy': [t.get('accuracy', None) for t in trials.data],
                'rt': [t.get('rt', None) for t in trials.data]
            })
            print("Created summary data from memory instead")
        with open(filename + '_summary.txt', 'w') as f:
            f.write(f"Experiment: {exp_info['task']}\n")
            f.write(f"Participant: {exp_info['participant']}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"Completed trials: {trial_number} of 30\n\n")
            try:
                acc_values = [v for v in data_df.get('accuracy', []) if pd.notnull(v)]
                mean_accuracy = sum(acc_values)/len(acc_values) if acc_values else "N/A"
                f.write(f"Overall accuracy: {mean_accuracy}\n")
                conditions = data_df.get('condition', [])
                f.write("\nTrials by condition:\n")
                for cnd in ['direct', 'intention', 'indirect']:
                    count = sum(1 for c in conditions if c == cnd)
                    f.write(f"{cnd}: {count} trials\n")
            except Exception as e_stats:
                f.write(f"Could not calculate detailed statistics. Error: {str(e_stats)}\n")
                f.write("Please check the Excel data file directly for complete results.\n")
    except Exception as main_e:
        print(f"Note: Could not create summary statistics. Error: {str(main_e)}")
        print("Data file was still saved as Excel.")
    stimuli['instructions'].text = "Thank you for participating.\nAll data has been saved.\nPress any key to exit."
    stimuli['instructions'].draw()
    win.flip()
    event.waitKeys()
    win.close()

if __name__ == '__main__':
    run_experiment()
