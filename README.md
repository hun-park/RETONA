# Structure
* *Construct HW*
    * *Build vivado schematic*
        * *Make modules*
            * **Make DPU**
            * *Setup PS*
                * *Use PS0 as USB micro B for GUI*
                * *Use PS1 as USB micro AB for debugging*
            * *Make UART modules*
                * *Use PL0~24 as RS- 422 with MAX3490ESA+*
                    * *[How to use MAX3490ESA+]()*
* *Construct Linux*
    * *Build petalinux*
        * **Contain BSP file**
        * *Make Linux drivers*
            * *For UART modules*
* *Construct SW*
    * *Build python files*
        * **Make 0_lookup.py**
            * **[.csv file](./w_board/table.csv) to [.feather file](./w_board/table.feather)**
        * *Make [1_preprocess.py](./w_gui/1_preprocess.py)* (***In Progress***)
            * Inputs [input file](./w_gui/input)
        * *Make [2_inference.py](./w_gui/2_inference.py)*
            * **Train CNN model**
            * **Quantize CNN model**
            * **Validate CNN model**
            * **Convert into .xmodel file**
        * *Make [3_translate.py](./w_gui/3_translate.py)
        * *Make [4_send.py](./w_gui/4_send.py)
<br></br>
# Scenario
* Manual Mode
    * GUI#
        * Send **Mode Information, Phase Degree(Azimuth&Elevation) and Attenuator** Data with **matlab>teraterm>zmodem**
    * FPGA#
        * Receive Data as [input file](./w_gui/input)
        * [1_preprocess.py](./w_gui/1_preprocess.py)
        * [3_translate.py](./w_gui/3_translate.py)
        * [4_send.py](./w_gui/4_send.py)
    * 25'{MCUs}#
        * Receive Control Bits in RS- 422 UART Communication with 9-pins DSUB
* AI Mode
    * GUI#
        * Send **Mode Information, I/Q Summation** Data with **matlab>teraterm>zmodem**
    * FPGA#
        * Receive Data as [input file](./w_gui/input)
        * [1_preprocess.py](./w_gui/1_preprocess.py)
        * [2_inference.py](./w_gui/2_inference.py)
        * [3_translate.py](./w_gui/3_translate.py)
        * [4_send.py](./w_gui/4_send.py)
    * 25'{MCUs}#
        * Receive Control Bits in RS- 422 UART Communication with 9-pins DSUB
<br></br>
# Reference
* [How to integrate the DPU into Custom Platforms](https://docs.xilinx.com/r/en-US/ug1414-vitis-ai/Integrating-the-DPU-into-Custom-Platforms)
<br></br>
# Archieve
* How to use GPIO in commandline
    ># root@xilinx-zcu102-2021_2:/sys/class/gpio# ls -al
    ># total 0
    ># drwxr-xr-x  2 root root    0 Mar  9 13:54 .
    ># drwxr-xr-x 61 root root    0 Mar  9 13:54 ..
    ># --w-------  1 root root 4096 Mar  9 13:54 export
    ># lrwxrwxrwx  1 root root    0 Mar  9 13:54 gpiochip301 -> ../../devices/platform/axi/ff020000.i2c/i2c-0/0-0021/gpio/gpiochip301
    ># lrwxrwxrwx  1 root root    0 Mar  9 13:54 gpiochip317 -> ../../devices/platform/axi/ff020000.i2c/i2c-0/0-0020/gpio/gpiochip317
    ># lrwxrwxrwx  1 root root    0 Mar  9 13:54 gpiochip333 -> ../../devices/platform/axi/ff0a0000.gpio/gpio/gpiochip333
    ># lrwxrwxrwx  1 root root    0 Mar  9 13:54 gpiochip507 -> ../../devices/platform/amba_pl@0/a0000000.gpio/gpio/gpiochip507
    ># lrwxrwxrwx  1 root root    0 Mar  9 13:54 gpiochip508 -> ../../devices/platform/firmware:zynqmp-firmware/firmware:zynqmp-firmware:gpio/gpio/gpiochip508
    ># --w-------  1 root root 4096 Mar  9 13:54 unexport
* How to use UART in commandline