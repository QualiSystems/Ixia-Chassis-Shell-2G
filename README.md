![](https://github.com/stsuberi/SaraTest/blob/master/cloudshell_logo.png)

# Ixia Chassis 2G Shell  

Release date: June 2018

Shell version: 2.0.4

Document version: 1.2.3

# In This Guide

* [Overview](#overview)
* [Downloading the Shell](#downloading-the-shell)
* [Importing and Configuring the Shell](#importing-and-configuring-the-shell)
* [Updating Python Dependencies for Shells](#updating-python-dependencies-for-shells)
* [References](#references)
* [Release Notes](#release-notes)

# Overview
A shell integrates a device model, application or other technology with CloudShell. A shell consists of a data model that defines how the device and its properties are modeled in CloudShell, along with automation that enables interaction with the device via CloudShell.

### Traffic Generator Shells
CloudShell's traffic generator shells enable you to conduct traffic test activities on Devices Under Test (DUT) or Systems Under Test (SUT) from a sandbox. In CloudShell, a traffic generator is typically modeled using a chassis resource, which represents the traffic generator device and ports, and a controller service that runs the chassis commands, such as Load Configuration File, Start Traffic and Get Statistics. Chassis and controllers are modeled by different shells, allowing you to accurately model your real-life architecture. For example, scenarios where the chassis and controller are located on different machines.

For additional information on traffic generator shell architecture, and setting up and using a traffic generator in CloudShell, see the [Traffic Generators Overiew](http://help.quali.com/Online%20Help/9.0/Portal/Content/CSP/LAB-MNG/Trffc-Gens.htm?Highlight=traffic%20generator%20overview) online help topic.

### Ixia Chassis 2G Shell
The Ixia Chassis 2G Shell provides you with connectivity and management capabilities such as device structure discovery and power management for the Ixia chassis. 

For more information on the Ixia Chassis, see the Ixia official product documentation.

To model an Ixia Chassis device in CloudShell, use one of the following controllers, which provide automation commands to run on the chassis, such as Load Configuration, Start Traffic/Test, Get Statistics: 

▪ <a href="https://community.quali.com/repos/1259/ixia-ixnetwork-controller-shell" target="_blank">Ixia IxNetwork Controller Shell</a>

▪ <a href="https://community.quali.com/repos/1396/ixia-ixload-controller-shell" target="_blank">Ixia IxLoad Controller Shell</a>

### Standard version
The Ixia Chassis 2G Shell 2.0.4 is based on the Traffic Shell standard *cloudshell_traffic_generator_chassis_standard_1_0_3.yaml*.

For detailed information about the shell’s structure and attributes, see the [Traffic Shell standard](https://github.com/QualiSystems/shell-traffic-standard/blob/master/spec/traffic_standard.md) in GitHub.

### Supported OS
▪ Windows

### Requirements

Release: Ixia Chassis 2G Shell 2.0.4

▪ 2G Chassis Shell: CloudShell version 8.1 and above

▪ Controller Shells: 
* Ixia IxNetwork Controller Shell - CloudShell version 8.0 and above
* Ixia IxLoad Controller Shell - CloudShell version 7.0 and above

### Data Model
#### **Ixia Chassis Families and Models**

The chassis families and models are listed in the following table:

|Family|Model|Description|
|:---|:---|:---|
|Traffic Generator Chassis|Ixia Chassis|Ixia Chassis|
|Module|Generic Traffic Generator Module|Modules located on the chassis|
|Port Group|Generic Port Group|Generic Port Group|
|Port|Generic Traffic Generator Port|Generic Traffic Generator Port|

#### **Ixia Chassis Attributes**

The attribute names and types are listed in the following table:

|Attribute|Type|Description|
|:---|:---|:---|
|Model Name|String|The catalog name of the device model. This attribute will be displayed in CloudShell instead of the CloudShell model.|
|Serial Number|Text|The serial number of the resource.|
|Server Description|String|The full description of the server. Usually includes the OS, exact firmware version, and additional characteristics of the device.|
|Vendor|String|The firmware version of the resource.|

### Automation
This section describes the automation (drivers or scripts) associated with the data model. The shell’s driver is associated with the model and provided as part of the shell package).There are two types of automation processes, Autoload and Resource. Autoload is executed when creating the resource in the Inventory dashboard, while resource commands are run in the Sandbox, providing that the resource has been discovered and is online.

For Traffic Generator Shells, commands are configured and executed from the controller service in the sandbox, with the exception of the Autoload command, which is executed when creating the resource.

|Command|Description|
|:-----|:-----|
|Autoload|Discovers the chassis, its hierarchy and attributes when creating the resource. The command can be rerun in the Inventory dashboard and not in the sandbox, as for other commands.|

### Downloading the Shell
The Ixia Chassis 2G Shell is available from the [Quali Community Integrations](https://community.quali.com/integrations) page. 

Download the files into a temporary location on your local machine. 

The shell comprises:

|File name|Description|
|:---|:---|
|Ixia.Chassis.Shell.2G.zip|Ixia Chassis Shell package|
|Ixia.Chassis.Shell.2G.offline.requirements.zip|Shell Python dependencies (for offline deployments only)|

# Importing and Configuring the Shell
This section describes how to import the Ixia Chassis 2G Shell and configure and modify the shell’s devices.

### Importing the shell into CloudShell

**To import the shell into CloudShell:**
  1. Make sure you have the shell’s zip package. If not, download the shell from the [Quali Community's Integrations](https://community.quali.com/integrations) page.
  2. In CloudShell Portal, as Global administrator, open the **Manage – Shells** page.
  3. Click **Import**.
  4. In the dialog box, navigate to the shell's zip package, select it and click **Open**.

The shell is displayed in the **Shells** page and can be used by domain administrators in all CloudShell domains to create new inventory resources, as explained in [Adding Inventory Resources](http://help.quali.com/Online%20Help/9.0/Portal/Content/CSP/INVN/Add-Rsrc-Tmplt.htm?Highlight=adding%20inventory%20resources). 

### Offline installation of a Shell

**Note:** Offline installation instructions are relevant only if CloudShell Execution Server has no access to PyPi. You can skip this section if your execution server has access to PyPi. For additional information, see the online help topic on offline dependencies.

In offline mode, import the shell into CloudShell and place any dependencies in the appropriate dependencies folder. The dependencies folder may differ, depending on the CloudShell version you are using:

* For CloudShell version 8.3 and above, see [Adding Shell and script packages to the local PyPi Server repository](#adding-shell-and-script-packages-to-the-local-pypi-server-repository).
* For CloudShell version 8.2, perform the appropriate procedure: [Adding Shell and script packages to the local PyPi Server repository](#adding-shell-and-script-packages-to-the-local-pypi-server-repository) or [Setting the python pythonOfflineRepositoryPath configuration key](#setting-the-python-pythonofflinerepositorypath-configuration-key).
* For CloudShell versions prior to 8.2, see [Setting the python pythonOfflineRepositoryPath configuration key](#setting-the-python-pythonofflinerepositorypath-configuration-key).

### Adding Shell and script packages to the local PyPi Server repository
If your Quali Server and/or execution servers work offline, you will need to copy all required Python packages, including the out-of-the-box ones, to the PyPi Server's repository on the Quali Server computer (by default *C:\Program Files (x86)\QualiSystems\CloudShell\Server\Config\Pypi Server Repository*).

For more information, see [Configuring CloudShell to Execute Python Commands in Offline Mode](http://help.quali.com/Online%20Help/9.0/Portal/Content/Admn/Cnfgr-Pyth-Env-Wrk-Offln.htm?Highlight=Configuring%20CloudShell%20to%20Execute%20Python%20Commands%20in%20Offline%20Mode).

**To add Python packages to the local PyPi Server repository:**
  1. If you haven't created and configured the local PyPi Server repository to work with the execution server, perform the steps in [Add Python packages to the local PyPi Server repository (offlinemode)](http://help.quali.com/Online%20Help/9.0/Portal/Content/Admn/Cnfgr-Pyth-Env-Wrk-Offln.htm?Highlight=offline%20dependencies#Add). 
  2. For each shell or script you add into CloudShell, do one of the following (from an online computer):
      * Connect to the Internet and download each dependency specified in the *requirements.txt* file with the following command: 
`pip download -r requirements.txt`. 
     The shell or script's requirements are downloaded as zip files.

      * In the [Quali Community's Integrations](https://community.quali.com/integrations) page, locate the Shell and click the Shell's **Download** link. In the page that is displayed, from the Downloads area, extract the dependencies package zip file.

3. Place these zip files in the local PyPi Server repository.
 
### Setting the python PythonOfflineRepositoryPath configuration key
Before PyPi Server was introduced as CloudShell’s python package management mechanism, the `PythonOfflineRepositoryPath` key was used to set the default offline package repository on the Quali Server machine, and could be used on specific Execution Eerver machines to set a different folder. 

**To set the offline python repository:**
1. Download the *Ixia.Chassis.Shell.2G.offline.requirements.zip* file, see [Downloading the Shell](#downloading-the-shell).
2. Unzip it to a local repository. Make sure the execution server has access to this folder. 
3.  On the Quali Server machine, in the *~\CloudShell\Server\customer.config* file, add the following key to specify the path to the default python package folder (for all Execution Servers):  
	`<add key="PythonOfflineRepositoryPath" value="repository 
full path"/>`
4. If you want to override the default folder for a specific Execution Server, on the Execution Server machine, in the *~TestShell\Execution Server\customer.config* file, add the following key:  
	`<add key="PythonOfflineRepositoryPath" value="repository 
full path"/>`
5. Restart the Execution Server.

### Configuring a new resource
This section explains how to create a new resource from the shell.

In CloudShell, the component that models the device is called a resource. It is based on the shell that models the device and allows the CloudShell user and API to remotely control the device from CloudShell.

You can also modify existing resources, see [Managing Resources in the Inventory](http://help.quali.com/Online%20Help/8.3/Portal/Content/CSP/INVN/Mng-Rsrc-in-Invnt.htm?Highlight=managing%20resources).

**To create a resource for the device:**
  1. In the CloudShell Portal, in the **Inventory** dashboard, click **Add New**. 
     ![](https://github.com/stsuberi/SaraTest/blob/master/create_a_resource_device.png)
  2. From the list, select the **Ixia Chassis 2G Shell**.
  3. Enter the **Name** and **IP address** of the Ixia Chassis.
  4. Click **Create**.
  5. In the **Resource** dialog box, enter the device's settings, as follows: 
      * If Ixia Chassis is Windows-based and is accessible directly to the Execution Server then there is no need for additional settings.
      * If Ixia Chassis is Linux-based, please consult with our Customer Success team.
      * If Ixia Chassis is not directly accessible to the Execution Server, there must be an IxTclServer serving as a proxy between the Execution Server and the chassis, enter the following settings:
          * **Controller Address**: address of the IxTclServer
          * **Controller TCP Port**: TCP port of IxTclServer (leave empty for default 4555 port) 
  6. Click **Continue**.

CloudShell validates the device’s settings and updates the new resource with the device’s structure (if the device has a structure).

# Updating Python Dependencies for Shells
This section explains how to update your Python dependencies folder. This is required when you upgrade a shell that uses new/updated dependencies. It applies to both online and offline dependencies.

### Updating offline Python dependencies
**To update offline Python dependencies:**
1. Download the latest Python dependencies package zip file locally.
2. Extract the zip file to the suitable offline package folder(s). 
3. Restart any execution server that has a live instance of the relevant driver or script. This requires running the Execution Server's configuration wizard, as explained in the [Configure the Execution Server](http://help.quali.com/doc/9.0/CS-Install/content/ig/configure%20cloudshell%20products/cfg-ts-exec-srver.htm?Highlight=configure%20the%20execution%20server) topic of the CloudShell Suite Installation guide. 

### Updating online Python dependencies
In online mode, the execution server automatically downloads and extracts the appropriate dependencies file to the online Python dependencies repository every time a new instance of the driver or script is created.

**To update online Python dependencies:**
* If there is a live instance of the shell's driver or script, restart the execution server, as explained above. If an instance does not exist, the execution server will download the Python dependencies the next time a command of the driver or script runs.

# References
To download and share integrations, see [Quali Community's Integrations](https://community.quali.com/integrations). 

For instructional training and documentation resources, see the [Quali University](https://www.quali.com/university/).

To suggest an idea for the product, see [Quali's Idea box](https://community.quali.com/ideabox). 

To connect with Quali users and experts from around the world, ask questions and discuss issues, see [Quali's Community forums](https://community.quali.com/forums). 

# Release Notes
### What's New

* Sets unknown port speed to zero.
* Supports new card types.
* Displays only active ports instead of all ports.

### Known Issues
* Resource groups are not modeled. Resource groups are modeled as ports with a speed that represents the total speed of the group. The index of the represented port is the index of the active port of the group.
