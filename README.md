# Distributed Computing Project with Ray Library using Rapid API 
This project aims to implement a web scraping script in Python using RapidAPI to gather information on real estate listings in a local area. This data is then gathered for further analysis. In the context of computer networks, this project uses multiple technologies such as web scraping and distributed computing (using Ray) to automate collecting data. 
Automating the data collection process saves time and effort compared to if it was done manually. Analyzing this data proves to be beneficial for analyzing pricing insights and marketing trends. This data is useful for real estate developers and investors who need this data to make business decisions. This project can be further improved by leveraging cloud storage to store larger amounts of data without limitations. 


## Configuration:

To be able to distribute tasks amongst virtual machines and be able to execute our Python script, a head node is needed. This virtual machine was created on Azure. Then, because this is a simple task, I only decided to use one worker node virtual machine. If this was a bigger project, then I would have created more worker nodes. On Azure, the two VMs were configured under the same resource group, subnet, and operating system (Ubuntu).
![azure set up](https://github.com/guegracie/web-scraping-project/assets/95649024/418c34fe-ab3e-48e8-911d-e2c2688feaec)

**Ray Cluster**

We configured our Ray cluster by first establishing a connection to our VMs via SSH using the path to the corresponding private keys.
<img width="649" alt="img2" src="https://github.com/guegracie/web-scraping-project/assets/95649024/fee8417e-77ce-4c73-836e-319d5d0cb7cb">

Before setting up our Ray cluster, we ensured the VMs were able to communicate with one another using: **telnet 4.234.169.27 22 (telnet <ip addr><port #>)**.

Once in our terminals, we ran the following commands to establish a ray session and ray head node.

![ray head](https://github.com/guegracie/web-scraping-project/assets/95649024/11ae73ef-6a5a-4747-a22f-7781dc360d8e)


Note the command used to do this: **ray start --head --port=6379 --dashboard-host 0.0.0.0**
 
After the head node was configured, we ran the following command to connect our worker node to our head node. 

![connect ray node to head node](https://github.com/guegracie/web-scraping-project/assets/95649024/b6a15259-c850-4d04-9077-4afb9fd4bd6a)

Note the command used to do this: **ray start --address=’10.0.0.4:6379' --dashboard-host 0.0.0.0**

Note: **using ray status also allowed us to verify the nodes in our cluster:**
![ray status](https://github.com/guegracie/web-scraping-project/assets/95649024/918e0cc7-f44b-496b-b2ce-d620a3e12e23)

Before compressing our script’s file and extracting it, we also installed the necessary dependencies.

sudo apt update
sudo apt install python3
pip install ray
pip install requests
pip install azure-storage-blob
pip install beautifulsoup4
pip install pandas

For organizational purposes, we made a directory in the head cluster where we would unzip our files and execute our scripts using the mkdir command: **mkdir /my_proj**

Using scp command: **scp -i /Users/gracieguevara/Downloads/NetworksVM_key.pem -r /Users/gracieguevara/Desktop/web\ scraping\ project.zip azureuser@4.234.169.250:web-scraping-project.zip**, from the local machine we ran this command to transfer our zip file into our VM

![transfer zip file](https://github.com/guegracie/web-scraping-project/assets/95649024/bc51049c-5bdc-4f9d-9e24-cbf0d5665763)

Note: This is how many times I extracted the whole folder multiple times before realizing transferring my single file with my script was easier!
 
Once back into the head VM, we used the **unzip web-scraping-project.zip -d ~/my_proj/** command to extract our files. 

![run script](https://github.com/guegracie/web-scraping-project/assets/95649024/e37c9da4-557d-445e-abd8-8351cb23e694)

Once the files were in our head VM, we navigated to the directory with our Python files and executed our script. As you can see our VM connects to the existing Ray cluster and distributes the work with our other VM. Our data is then saved to the web scraping directory. We’ve successfully distributed the task using a Ray cluster!


