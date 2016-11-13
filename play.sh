#Script file
#Python Assignment Yehonatan 

inst(){
	sudo pip install psutil;
	sudo pip install py-cpuinfo;
	
}

launch(){
	echo "Opening Server"
	gnome-terminal -e "python sysSpecs.py server"
	echo "Opening Client"
	gnome-terminal -e "python sysSpecs.py client"
}


 read -p "Do you wish to install dependencies Y/N?" yn
    case $yn in
        [Yy]* ) inst;launch;break;;
        [Nn]* ) launch;exit;;
        * ) echo "Please answer yes or no.";;
    esac
