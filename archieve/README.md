# fpga-process    
![state_diagram](https://github.com/hun-park/fpga-process/blob/main/state_diagram.jpeg)

### working flow:    
```
    phase A) Move forward radar head -> out [6:0] control_bits
    ('en' == True)  phase B) Move backward radar head & collect data -> out [6:0] control_bits
    # when 'en' signal from laptop,
    # move backward radar head
    # & collect data from radar.
    # (5*5) inputs by 49 unit times.
        (collect data != done)  phase C) calculate hot spot -> out [6:0] control_bits
        (collect data == done)  phase B) move backward radar head & collect data -> out [6:0] control_bits
    ('en' != True) phase A) Move forward radar head -> out [6:0] control_bits
```

### pseudo code:    
```
    # open from csv
    # store informations of (theta, pi, head_position) as pandas.dataframe
    CONTROL_BITS =
    {
    '0000':6'B000000,
    '0001':6'B000001,
    '0002':6'B000002,
    '1296':6'B111111
    }
    
    INIT_STATUS = '0000'

    # phase A) Move forward radar head -> out [6:0] control_bits
    # loop
    LOOP:
        # ('en' != True)
        # phase A) Move forward radar head -> out [6:0] control_bits
        IF (EN != TRUE):
            # hash to next status
            # return control_bits
            STATUS = INIT_STATUS + 1
            RETURN CONTROL_BITS[STATUS]
        # when 'en' signal from laptop,
        # move backward radar head
        # & collect data from radar.
        # phase B) Move backward radar head & collect data -> out [6:0] control_bits
        IF (EN == TRUE):
            # (collect data != done)  phase B) move backward radar head & collect data -> out [6:0] control_bits
            IF (CLCTDT != TRUE):
                # hash to previous status
                # return control_bits
                STATUS = INIT_STATUS - 1
                COLLECTDATA(PATH)
                RETURN CONTROL_BITS[STATUS]
            # (collect data == done)  phase C) calculate hot spot -> out [6:0] control_bits
            IF (CLCTDT == TRUE):
                # caluclate hot spot
                # return control_bits
                STATUS = INFERENCE(DATA)
                RETURN CONTROL_BITS[STATUS]

    COLLECTDATA(PATH):
        OPENCSV(PATH)
        RETURN CLCTDT

    INFERENCE(DATA):
        OUT = MODEL(DATA)
        RETURN STATUS
    
    MAIN:
        GOTO LOOP
```
