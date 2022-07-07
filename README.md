# Structure
* *Construct HW*
    * *Build vivado schematic*
        * *Make modules*
            * **Make DPU**
            * **Setup PS**
                * **Use PS0 as USB micro B for GUI**
                * **Use PS1 as USB micro AB for debugging**
            * *Make UART modules* (***In Progress***)
                * *Use PL0~24 as RS- 422 with MAX3490ESA+* (***In Progress***)
                    * *[How to use MAX3490ESA+]()* (***In Progress***)
* *Construct Linux*
    * *Build petalinux*
        * **Contain BSP file**
        * *Make Linux drivers* (***In Progress***)
            * *For UART modules* (***In Progress***)
* *Construct SW*
    * *Build python files*
        * **Make lookup.py**
            * ~~[.csv file](./w_board/table.csv) to [.feather file](./w_board/table.feather)~~
            * **[.csv file](./w_board/table.csv)**
        * **Make [preprocess.py](./w_gui/preprocess.py)**
            * **Inputs [input file](./w_gui/input)**
        * Make [inference.py](./w_gui/inference.py)
            * **Train CNN model**
            * **Quantize CNN model**
            * **Validate CNN model**
            * **Convert into .xmodel file**
        * **Make [translate.py](./w_gui/translate.py)**
        * *Make [send.py](./w_gui/send.py)* (***In Progress***)
  

# Scenario
* Manual Mode
    * GUI#
        * Send **Mode Information, Phase Degree(Azimuth&Elevation) and Attenuator** Data with **matlab>teraterm>zmodem**
    * FPGA#
        * **Receive Data as [input file](./w_gui/input)**
        * **[preprocess.py](./w_gui/preprocess.py)**
        * **[translate.py](./w_gui/translate.py)**
        * *[send.py](./w_gui/send.py)* (***In Progress***)
    * 25'{MCUs}#
        * *Receive Control Bits in RS- 422 UART Communication with 9-pins DSUB* (***In Progress***)
* AI Mode
    * GUI#
        * Send **Mode Information, I/Q Summation** Data with **matlab>teraterm>zmodem**
    * FPGA#
        * **Receive Data as [input file](./w_gui/input)**
        * **[preprocess.py](./w_gui/preprocess.py)**
        * [inference.py](./w_gui/inference.py)
        * **[translate.py](./w_gui/translate.py)**
        * *[send.py](./w_gui/send.py)* (***In Progress***)
    * 25'{MCUs}#
        * *Receive Control Bits in RS- 422 UART Communication with 9-pins DSUB* (***In Progress***)
  

# Reference
* [How to integrate the DPU into Custom Platforms](https://docs.xilinx.com/r/en-US/ug1414-vitis-ai/Integrating-the-DPU-into-Custom-Platforms)
  

# Archieve
* How to use GPIO in commandline
   * Check amba_pl is in the list.
   >root@xilinx-zcu102-2021_2:/sys/class/gpio# ls -al  
     
   >total 0  
   >drwxr-xr-x  2 root root    0 Mar  9 13:54 .  
   >drwxr-xr-x 61 root root    0 Mar  9 13:54 ..  
   >--w-------  1 root root 4096 Mar  9 13:54 export  
   >lrwxrwxrwx  1 root root    0 Mar  9 13:54 gpiochip301 -> ../../devices/platform/axi/ff020000.i2c/i2c-0/0-0021/gpio/gpiochip301  
   >lrwxrwxrwx  1 root root    0 Mar  9 13:54 gpiochip317 -> ../../devices/platform/axi/ff020000.i2c/i2c-0/0-0020/gpio/gpiochip317  
   >lrwxrwxrwx  1 root root    0 Mar  9 13:54 gpiochip333 -> ../../devices/platform/axi/ff0a0000.gpio/gpio/gpiochip333  
   >lrwxrwxrwx  1 root root    0 Mar  9 13:54 gpiochip507 -> ../../devices/platform/amba_pl@0/a0000000.gpio/gpio/gpiochip507  
   >lrwxrwxrwx  1 root root    0 Mar  9 13:54 gpiochip508 -> ../../devices/platform/firmware:zynqmp-firmware/firmware:zynqmp-firmware:gpio/gpio/gpiochip508  
   >--w-------  1 root root 4096 Mar  9 13:54 unexport  
   * Declare to use amba_pl chip with #echo 507 > /sys/class/gpio/export#
   * Declare to use gpio as in with #echo "low" > /sys/class/gpio/gpio507/direction#
   * Declare to use gpio as out with #echo "high" > /sys/class/gpio/gpio507/direction#
   * Declare to turn on gpio with #echo 1 > /sys/class/gpio/gpio507/value#
   * Declare to stop using amba_pl chip with #echo 507 > /sys/class/gpio/unexport#
* How to use UART in commandline
   * Send file as xmodem from PC to FPGA with #sx sequence_2022_05_19_14_38_30 < /dev/ttyUSB0 > /dev/ttyUSB0#
   * Send file as xmodem from FPGA to PC with #sx sequence_2022_05_19_14_38_30 < /dev/ttyPS0 > /dev/ttyPS0#