import asyncio
import settings

async def timer(loop, config, gui_connection=None):
    #reading configs
    GUI = settings.read_parameter(config, ['EXECUTION', 'gui'])
    WORK_TIME = settings.read_parameter(config, ['TIME', 'work_time'], 'int')
    SHORT_BREAK_TIME = settings.read_parameter(config, ['TIME', 'short_break'], 'int')
    LONG_BREAK_TIME = settings.read_parameter(config, ['TIME', 'long_break'], 'int')
    SHORTS_BEFORE_LONG = settings.read_parameter(config, ['TIME', 'shorts_before_long'], 'int')
    default_state = settings.read_parameter(config, ['EXECUTION', 'state'])
    stop_timer = False
    
    if GUI == 'qt': # init qt gui connection
        def timeRemain():
            gui_connection.timeIs.emit(left_time)
        def closeApp():
            stop_timer = True
        gui_connection.whatTime.connect(timeRemain)
        gui_connection.closeApp.connect(closeApp)
    
    current_state = default_state
    gui_state = current_state
    count_short_breaks = 0
    is_work_time = True
    left_time = WORK_TIME
    all_time = WORK_TIME
    # start timer
    while True:
        #print(time_remain)
        left_time -= 1
        await asyncio.sleep(1)
        
        percentage = left_time/all_time * 100
        if is_work_time:
            if percentage <= 100 and percentage > 87.5:
                current_state = 'work-full'
            elif percentage <= 87.5 and percentage > 75:
                current_state = 'work-7-8'
            elif percentage <= 75 and percentage > 62.5:
                current_state = 'work-6-8'
            elif percentage <= 62.5 and percentage > 50:
                current_state = 'work-5-8'
            elif percentage <= 50 and percentage > 37.5:
                current_state = 'work-4-8'
            elif percentage <= 37.5 and percentage > 25:
                current_state = 'work-3-8'
            elif percentage <= 25 and percentage > 12.5:
                current_state = 'work-2-8'
            elif percentage <=12.5 and percentage > 0:
                current_state = 'work-1-8'
            else:
                current_state = 'work-1-8'
                is_work_time = False
                if count_short_breaks < SHORTS_BEFORE_LONG:
                    left_time = SHORT_BREAK_TIME
                    all_time = SHORT_BREAK_TIME
                    count_short_breaks += 1
                else:
                    left_time = LONG_BREAK_TIME
                    all_time = LONG_BREAK_TIME
                    count_short_breaks = 0
        else:
            if percentage <= 100 and percentage > 75:
                current_state = 'break-full'
            elif percentage <= 75 and percentage > 50:
                current_state = 'break-3-4'
            elif percentage <= 50 and percentage > 25:
                current_state = 'break-2-4'
            elif percentage <= 25 and percentage > 0:
                current_state = 'break-1-4'
            else:
                current_state = 'break-1-4'
                is_work_time = True
                left_time = WORK_TIME
                all_time = WORK_TIME
        
        if current_state != gui_state:
            gui_connection.changeState.emit(current_state)
            gui_state = current_state
        
        if stop_timer == True:
            break
