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
        * **[inference.py](./w_gui/inference.py)**
        * **[translate.py](./w_gui/translate.py)**
        * *[send.py](./w_gui/send.py)* (***In Progress***)
    * 25'{MCUs}#
        * *Receive Control Bits in RS- 422 UART Communication with 9-pins DSUB* (***In Progress***)
  

# Reference
* [How to integrate the DPU into Custom Platforms](https://docs.xilinx.com/r/en-US/ug1414-vitis-ai/Integrating-the-DPU-into-Custom-Platforms)

# Steps
* vivado
* petalinux ***cd ~/projects/retona/standalone/***
   * source_petalinux
   * petalinux-create -t project -s ../bsp/xilinx-zcu102-trd.bsp && cd xilinx-zcu102-trd
   * petalinux-config --get-hw-description=../../xsas/uartlite_w_interrupt.xsa
      * (Yocto Settings) → Enable Buildtools Extended
   * petalinux-config -c kernel
      * CONFIG_GPIO_SYSFS=y
      * CONFIG_SYSFS=y
      * CONFIG_GPIO_XILINX=y
      * CONFIG_SERIAL_UARTLITE=y | CONFIG_SERIAL_UARTLITE=m
      * CONFIG_SERIAL_UARTLITE_NR_UARTS=<total number of UARTs in the system>
   * petalinux-config -c rootfs
      * petalinux-group → opencv, opencv-dev
   * petalinux-build
   * cd images/linux && petalinux-package --boot --fsbl zynqmp_fsbl.elf --u-boot u-boot.elf --pmufw pmufw.elf --fpga system.bit
   * petalinux-package --wic --wic-extra-args "-c gzip"
* FPGA
   * to check device-tree, dtc -I fs /sys/firmware/devicetree/base
   * to check interrupts, cat /proc/interrupts

# Archieve
* How to connect UARTLITE with vivado and petalinux
   * vivado@host -> Connect UARTLITE IP with PS
   * vivado@host -> Connect UARTLITE IP's Interrupt with PS IRQ_F2P
   * petalinux@host -> kernel config to ***Device drivers - Characters devices - Serial Drivers - Xilinx uartlite...***
   * device probing
      * petalinux@host
      > dtc -O dts -I dtb -o images/linux/system.dts images/linux/system.dtb
      
      > system.dts: Warning (unit_address_vs_reg): /amba_pl@0: node has a unit name, but no reg property  
      > system.dts: Warning (unit_address_vs_reg): /memory: node has a reg or ranges property, but no unit name  
      > system.dts: Warning (pci_device_reg): /axi/pcie@fd0e0000/legacy-interrupt-controller: missing PCI reg property  
      > system.dts: Warning (simple_bus_reg): /amba_pl@0/misc_clk_0: missing or empty reg/ranges property  
      > system.dts: Warning (simple_bus_reg): /amba_pl@0/misc_clk_1: missing or empty reg/ranges property  
      > system.dts: Warning (avoid_unnecessary_addr_size): /gpio-keys: unnecessary #address-cells/#size-cells without "ranges" or child "reg" property  
      > system.dts: Warning (gpios_property): /__symbols__:gpio: property size (19) is invalid, expected multiple of 4  

      * cmd@host
         * this issue is relevant with [./build/tmp/work-shared/zynqmp-generic/kernel-source/drivers/tty/serial/uartlite.c](https://elixir.bootlin.com/linux/latest/source/drivers/tty/serial/uartlite.c)
      > dmesg | grep serial
      
      > [    3.947328] ff000000.serial: ttyPS0 at MMIO 0xff000000 (irq = 50, base_baud = 6249375) is a xuartps  
      > [    3.969882] xuartps ff010000.serial: there is not valid maps for state default  
      > [    3.981473] ff010000.serial: ttyPS1 at MMIO 0xff010000 (irq = 51, base_baud = 6249375) is a xuartps  
      > [    4.120876] [uartlite a0000000.serial: ttyUL1 too large](https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=wmk2&logNo=220198111054)*  
      > [    4.126020] uartlite: probe of a0000000.serial failed with error -22  
   
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
   * Declare to use amba_pl chip with
   > echo 507 > /sys/class/gpio/export
   * Declare to use gpio as in with 
   > echo "low" > /sys/class/gpio/gpio507/direction
   * Declare to use gpio as out with
   > echo "high" > /sys/class/gpio/gpio507/direction
   * Declare to turn on gpio with
   > echo 1 > /sys/class/gpio/gpio507/value
   * Declare to stop using amba_pl chip with
   > echo 507 > /sys/class/gpio/unexport
   
* How to use UART in commandline
   * Send file as xmodem from PC to FPGA with 
   > sx sequence_2022_05_19_14_38_30 < /dev/ttyUSB0 > /dev/ttyUSB0#
   * Send file as xmodem from FPGA to PC with
   > sx sequence_2022_05_19_14_38_30 < /dev/ttyPS0 > /dev/ttyPS0#
