HiBench-ML: Automated deployment of Intel HiBench Machine Learning benchmarks
```````````````````````````````````````````````````````````````````````````````

- The project is tested in **bdossp_sp16** virtualenv from **hw3** using Chameleon cloud infrastructure. All default values are set to match with Chameleon deployment.

- Before deployment ou need to configure the envirnoment by loading openstack module::

	$ module load openstack

- Load the script which provides access to a cloud infrastructure::

	$ source /path/to/cloud/access/configuration

Instructions  
-------------------------------------------------------------------------------

- First clone the repo at *https://github.iu.edu/alivara/HiBench-ML*::

	$ git clone --recursive git@github.iu.edu:alivara/hibench-ml.git HiBench-ML

- Change directory to *HiBench-ML*::

	$ cd HiBench-ML

- Specify **remote_user** variable in *ansible.cfg*  and *plays/vars.yml* files. If you are using chameleon it should be **cc**.::

	$ vi bds/ansible.cfg
	$ vi ansible.cfg
 	$ vi plays/vars.yml

-  Apply the following changes to the *bds/.cluster.py*::

	$ vi bds/.cluster.py
	Change 'create_floating_ip': False to  'create_floating_ip': True
	Make sure to set 'image' within 'openstack' dictionary. If you are using chameleon it should be 'image': 'CC-Ubuntu14.04'
	Change 'flavor': 'm1.small' to 'flavor': 'm1.large' within 'openstack' dictionary
	
- Determine benchmark dataset scale varibel **scale**. You may choose one of these three values: **tiny**, **small**, **large**, **huge**, **gigantic**, and **bigdata**. Default is **tiny**::

	$ vi plays/vars.yml

- Add  the follwoing lines to hadoop configuration roles::


	$ vi bds/base/02-hadoop.yml

	under 'mapred_site' role add these lines:
		mapreduce.map.memory.mb: 4096
		mapreduce.reduce.memory.mb: 8192
		mapreduce.map.java.opts: "-Xmx2040m"
		mapreduce.reduce.java.opts: "-Xmx4096m"


	under 'yarn_site' role add these lines:
		yarn.scheduler.maximum-allocation-mb: 9216

- Change the **spark_version: 1.6.0**  **spark_version: 1.3.1** in Spark installation role::

	$ vi bds/addons/spark.yml

- Run the following command to create three VMs::

	$ cd bds && vcl boot -p openstack -P $USER- && cd ..

- Make sure that all VMs are reachble using the following command::

	$ ansible all -m ping
	
- Install required packages, Hadoop, and Spark::

	$ cd bds && ansible-playbook play-hadoop.yml addons/spark.yml  && cd ..

- Install HiBench, configure, run benchmarks, and plot results::

        $ ansible-playbook hibench.yml

- The results will be placed in the following path in the frontendnode::

	/home/{{ remote_user }}/HiBench/report/


- You can use the following command to copy to get the plot (if you remote_user is set to cc)::

	$ scp cc@<frontendnode address>:/home/cc/HiBench/report/durtation.png .
	$ scp cc@<frontendnode address>:/home/cc/HiBench/report/throughput_per_node.png .
	$ scp cc@<frontendnode address>:/home/cc/HiBench/report/throughput_total.png .

- Plots from sample benchmark executioon can be found at the following path in the repo::

	examples/plots/ 


