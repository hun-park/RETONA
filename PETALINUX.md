- Make sure .xsa include bitstream.  

- Open petalinux
>source_petalinux   

- Create petalinux project
>petalinux-create -t project -s xilinx-zcu102-trd.bsp   

- Change directory into project
>cd xilinx-zcu102-trd   

- Make sure *(Yocto Settings) → Enable Buildtools Extended*
>petalinux-config --get-hw-description=../xsas/plus_uart.xsa  

- Make sure *CONFIG_GPIO_SYSFS=y*
- Make sure *CONFIG_SYSFS=y*
- Make sure *CONFIG_GPIO_XILINX=y*
>petalinux-config -c kernel 

- Make sure *petalinux-group → opencv, opencv-dev*
>petalinux-config -c rootfs 

- Build the petalinux project. 
>petalinux-build    

- Change directory into **images/linux**
>cd images/linux    

- Package **boot loader, zynqmp_fsbl.elf, u-boot.elf, pmufw.elf and system.bit** files.
>petalinux-package --boot --fsbl zynqmp_fsbl.elf --u-boot u-boot.elf --pmufw pmufw.elf --fpga system.bit    

- Package into *.gzip*.
>petalinux-package --wic --wic-extra-args "-c gzip"

- Bake SD card
>/tools/BalenaEtcher