

XGBoost4J
=========

XGBoost4J relies on underlying C++ library that must be compiled on/for the target OS.
This document section outlines:
*   Setting up maven profiles (and repo) for acquiring the correct XGBoost4J binary for your OS
*   (_Advanced_) Building XGBoost4J from source on each OS and deploying the resulting binary for others to access
    *   **NOTE:** Building XGBoost4j from source should _rarely_ be necessary unless:
        *   A binary does not already exist/work for your target OS
        *   A newer version of XGBoost is available and required
**REFS:**
*   [https://github.com/dmlc/xgboost](https://github.com/dmlc/xgboost)
*   [https://github.com/dmlc/xgboost/tree/master/jvm-packages](https://github.com/dmlc/xgboost/tree/master/jvm-packages)

Using XGBoost4J
---------------

*   Since the XGBoost dependency is platform-specific, one should leverage **Maven profiles** for selecting the correct XGBoost4j version based on the underlying OS.
    
*   XGBoost4j binaries for each of Win, *nix, Mac are available at [https://tr1.jfrog.io/tr1/libs-release-local/checkpoint-release/](https://tr1.jfrog.io/tr1/libs-release-local/checkpoint-release/)
    *   This repository can be added to your project pom in order to access them
    
    ![](http://localhost:63342/markdownPreview/386105395/cptam-common?_ijt=65mqrbimo9tv30fsdmo1dj7f93)
      ```
        <repository>
            <id>checkpoint-release-repo</id>
            <url>https://tr1.jfrog.io/tr1/libs-release-local/checkpoint-release/</url>
            <releases>
                <enabled>true</enabled>
            </releases>
        </repository>
      ```
    
    *   The following is a _profiles_ snippet from **pom.xml** that will pull in the correct XGBoost4J dependency jar based on the building OS:
        
        ![](http://localhost:63342/markdownPreview/386105395/cptam-common?_ijt=65mqrbimo9tv30fsdmo1dj7f93)
        
        ```
        ...
        <profiles>
            <profile>
                <id>build-for-windows</id>
                <activation>
                    <os>
                        <family>windows</family>
                    </os>
                </activation>
                <dependencies>
                    <dependency>
                        <groupId>ml.dmlc</groupId>
                        <artifactId>xgboost4j-win</artifactId>
                        <version>2.1.4</version>
                    </dependency>
                </dependencies>
            </profile>
            <profile>
                <id>build-for-nix</id>
                <activation>
                    <os>
                        <name>Linux</name>
                        <family>unix</family>
                    </os>
                </activation>
                <dependencies>
                    <dependency>
                        <groupId>ml.dmlc</groupId>
                        <artifactId>xgboost4j-nix</artifactId>
                        <version>2.1.4</version>
                    </dependency>
                </dependencies>
            </profile>
            <profile>
                    <id>build-for-mac</id>
                    <activation>
                        <os>
                            <family>mac</family>
                        </os>
                    </activation>
                    <dependencies>
                        <dependency>
                            <groupId>ml.dmlc</groupId>
                            <artifactId>xgboost4j-mac</artifactId>
                            <version>2.1.4</version>
                        </dependency>
                    </dependencies>
                </profile>
        </profiles>
        ...
        ```
  
      
**NOTE:** If you wish to build for a **target OS other than the build OS**, you can use the `-P` option of maven to control the profile. HOWEVER, it is preferably to use a matching build/target OS family.
For example, if building on windows to deploy to linux, the following will include the linux-friendly .so for xgboost along with the .dll.

![](http://localhost:63342/markdownPreview/386105395/cptam-common?_ijt=65mqrbimo9tv30fsdmo1dj7f93)

`mvn clean package -P build-for-nix`

Building XGBoost C library from source
--------------------------------------

*   **As noted above**, building XGBoost4j from source should _rarely_ be necessary unless:
    *   A binary does not already exist/work for your target OS
    *   A newer version of XGBoost is available and required

### Building XGBoost C library from source on Windows

The following are the build dependencies and steps for Windows (Win 7 Enterprise, sp1 x64 was used for these instructions).
**REFS:**
*   [http://xgboost.readthedocs.io/en/latest/build.html](http://xgboost.readthedocs.io/en/latest/build.html)
*   [https://xgboost.readthedocs.io/en/latest/jvm/index.html](https://xgboost.readthedocs.io/en/latest/jvm/index.html)

#### Dependencies

*   Install (if not exists) **JDK**
    *   Amazon Corretto OpenJDK 17 SDK was used for these instructions
    *   [https://docs.aws.amazon.com/corretto/latest/corretto-17-ug/downloads-list.html](https://docs.aws.amazon.com/corretto/latest/corretto-17-ug/downloads-list.html)
    *   Add (if not exists) _JAVA_HOME_ environment variable
*   Install (if not exists) **Git**
    *   Version 2.46.1.windows.1 was used for these instructions
    *   [https://github.com/git-for-windows/git/releases](https://github.com/git-for-windows/git/releases)
*   Install (if not exists) **Maven**
    *   Version 3.5.3 was used for these instructions
    *   [http://maven.apache.org/download.cgi](http://maven.apache.org/download.cgi)
*   Install (if not exists) **CMake**
    *   Version 4.0.0-rc2 was used for these instructions
    *   [https://cmake.org/download/](https://cmake.org/download/)
    *   During install, select:
        *   'Add to path...' option
*   Install (if not exists) Visual Studio **VC++ 2022**
    *   The Build Tools for Visual Studio Community 2022 installer was used for these instructions
    *   [https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022)
    *   During install (or modify), select:
        *   Under "Individual Components" tab...
        *   Check "MSVC v143 - VS 2022 x64/x86 build tools"
        *   Check Visual C++ 2022
        *   Check "Windows 11 SDK (10.0.22621.0)"

#### Retrieving and Building XGBoost

*   Pick a parent directory to download sources to. An 'xgboost' sub-dir will be created by the 'git clone' step below
    
*   Start git bash and from within your preferred directory
    *   e.g. right click in folder > Git Bash Here
        
    *   Step 1: Clone the xgboost from github
        *   Make sure to use --recursive option when cloning the xgboost repository (otherwise it will not clone some of the nested repositories and the Step 2 will fail)
        
        ![](http://localhost:63342/markdownPreview/386105395/cptam-common?_ijt=65mqrbimo9tv30fsdmo1dj7f93)
        
        `git clone --recursive https://github.com/dmlc/xgboost`
        
        *   Version release_2.1.0 was used for these instructions. You can also use the following command to directly clone a specific branch.
        
        ![](http://localhost:63342/markdownPreview/386105395/cptam-common?_ijt=65mqrbimo9tv30fsdmo1dj7f93)
        
         `git clone -b release_2.1.0 --recursive https://github.com/dmlc/xgboost`
        
    *   Step 2:  
        `cmake .. -G"Visual Studio 17 2022" -A x64 -D TCNN_CUDA_ARCHITECTURES=86 -D CMAKE_CUDA_COMPILER="C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8\bin"`
        
    *   Step 3: `cmake --build . --target xgboost --config Release`
        Assuming a successful build… xgboost.dll will be in lib
        
    *   Step 4:
        
        ![](http://localhost:63342/markdownPreview/386105395/cptam-common?_ijt=65mqrbimo9tv30fsdmo1dj7f93)
        
        `cd .. ls -ltr lib`
        
    *   Step 5: Switch to the xgboost module dir in jvm-packages dir
        
        ![](http://localhost:63342/markdownPreview/386105395/cptam-common?_ijt=65mqrbimo9tv30fsdmo1dj7f93)
        
        `cd .. cd jvm-packages/xgboost4j`
        
    *   Step 6: Edit pom.xml (for xgboost4j module)
        
            Change artifactId from 'xgboost4j' to - as applicable - one of:
            'xgboost4j-nix'
            'xgboost4j-win'
            'xgboost4j-mac'
            Remove '-SNAPSHOT' from the version, if applicable
            
        
    *   Step 7: Switch to 'jvm-packages' dir and launch maven install
        
        ![](http://localhost:63342/markdownPreview/386105395/cptam-common?_ijt=65mqrbimo9tv30fsdmo1dj7f93)
        
        `cd .. mvn install -pl xgboost4j -am`
        
        Assuming a successful install, XGBoost4J for specified OS (e.g. xgboost4j-win) is now available in your LOCAL Maven repository.
        
    *   Step 8: Assuming a successful build… **xgboost.dll** (for windows) will be in _lib_
        
        ![](http://localhost:63342/markdownPreview/386105395/cptam-common?_ijt=65mqrbimo9tv30fsdmo1dj7f93)
        
        `cd ..  -ltr lib`
        

### Building XGBoost C library from source on Ubuntu 24.04

The following are the build dependencies and steps for Ubuntu 24.04
*   The xgboost4j-nix binary built on Ubuntu 24.04 has been tested on:
    *   Ubuntu 24.04
**REFS:**
*   [http://xgboost.readthedocs.io/en/latest/build.html](http://xgboost.readthedocs.io/en/latest/build.html)
*   [https://xgboost.readthedocs.io/en/latest/jvm/index.html](https://xgboost.readthedocs.io/en/latest/jvm/index.html)

#### Dependencies

*   Install (if not exists) **JDK**
    *   Version Corretto-17.0.14.7.1 was used for these instructions
    *   Add (if not exists) _JAVA_HOME_ environment variable
    
    ![](http://localhost:63342/markdownPreview/386105395/cptam-common?_ijt=65mqrbimo9tv30fsdmo1dj7f93)

### **Step 1: Add the Corretto Repository**

1.  **Import the GPG key:**
    Open a terminal and run the following command to import the GPG key:
    
    `wget -O- https://apt.corretto.aws/corretto.key | sudo apt-key add -`
    
2.  **Add the Corretto repository:**
    Add the repository to your sources list by running:
    
    `sudo add-apt-repository 'deb https://apt.corretto.aws stable main'`
    

### **Step 2: Install Corretto 17**

1.  **Update the package index:**
    After adding the repository, update your package index:
    
    `sudo apt update`
    
2.  **Install Corretto 17:**
    Now, install Amazon Corretto 17 with the following command:
    
    `sudo apt install -y java-17-amazon-corretto-jdk`
    

### **Step 3: Verify the Installation**

You can verify that Amazon Corretto 17 has been installed correctly by checking the Java version:

`java -version`

    
*   Install (if not exists) **Git**
    *   Version 2.43.0 was used for these instructions

    
    `sudo apt update`
    `sudo apt install git`
    `git --version`
    
*   Install (if not exists) **Maven**
    *   Version 3.8.1 was used for these instructions
        
       `sudo apt update` 
       `sudo apt install maven`
        
*   Install (if not exists) **GCC-C++**
    *   Version g++ (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0 was used for these instructions
        
    `sudo apt update` 
    `sudo apt install build-essential` 
    `g++ --version` //To verify version`
        
*   Install (if not exists) **CMake**
    *   Building xgboost requires version 3.2+
    *   Version 3.28.3 was used for these instructions
    
    ![](http://localhost:63342/markdownPreview/386105395/cptam-common?_ijt=65mqrbimo9tv30fsdmo1dj7f93)
    
     `sudo apt update` 
     `sudo apt install cmake` 
     `cmake --version`  //To verify version`
    

#### Retrieving and Building XGBoost

*   Pick a parent directory to download sources to
    *   an 'xgboost' sub-dir will be created by the 'git clone' step below
*   Clone the xgboost from sourceforge
    *   Branch release_2.1.0 (branch) was used for these instructions
    
    ![](http://localhost:63342/markdownPreview/386105395/cptam-common?_ijt=65mqrbimo9tv30fsdmo1dj7f93)
    
    `git clone -b release_2.1.0 --recursive https://github.com/dmlc/xgboost`
    
*   Enter xgboost directory and run make
    
    ![](http://localhost:63342/markdownPreview/386105395/cptam-common?_ijt=65mqrbimo9tv30fsdmo1dj7f93)
    
    `cd xgboost make -j4`
    
*   Assuming a successful build… **libxgboost.so** will be in ./lib
    
    ![](http://localhost:63342/markdownPreview/386105395/cptam-common?_ijt=65mqrbimo9tv30fsdmo1dj7f93)
    
    `ls -ltr lib`
    

### Building XGBoost C library from source on Mac

[http://xgboost.readthedocs.io/en/latest/build.html#building-on-macos](http://xgboost.readthedocs.io/en/latest/build.html#building-on-macos)

### Building and Installing XGBoost4J (all platforms)

*   Switch to the xgboost module dir in jvm-packages dir
    
    ![](http://localhost:63342/markdownPreview/386105395/cptam-common?_ijt=65mqrbimo9tv30fsdmo1dj7f93)
    
     `cd jvm-packages/xgboost4j`
    
*   Edit pom.xml (for xgboost4j module)
    *   Change artifactId from 'xgboost4j' to - as applicable - one of:
        *   '**xgboost4j-nix**'
        *   '**xgboost4j-win**'
        *   '**xgboost4j-mac**'
    *   Remove '-SNAPSHOT' from the version, if applicable
*   For nix and mac you need to update the line#93 from "python" to "python3".
    
*   Switch to 'jvm-packages' dir and launch maven install
    
    ![](http://localhost:63342/markdownPreview/386105395/cptam-common?_ijt=65mqrbimo9tv30fsdmo1dj7f93)
    
     `cd .. mvn install -pl xgboost4j -am`
    
*   Assuming a successful install, XGBoost4J for specified OS (e.g. xgboost4j-win) is now available in your LOCAL Maven repository.
    

### Deploying an XGBoost4j Binary to TR Artifactory (all platforms)

*   Ensure you have credentials for tr-artifactory jfrog configured in your Maven settings.xml
    *   i.e. in ${user.home}/.m2/settings.xml
    
    ![](http://localhost:63342/markdownPreview/386105395/cptam-common?_ijt=65mqrbimo9tv30fsdmo1dj7f93)
    
    `<settings> ...    <servers>   ...      <server>        <id>checkpoint-release</id>        <username>{TR_ARTIFACTORY_USER_ID}</username>        <password>{TR_ARTIFACTORY_USER_PASS}</password>      </server>   ...   </servers> ... </settings>`
    
*   From the xgboost4j directory, upload the binary to libs-release-local with the following command
    *   Please update **OSALIAS** in the command shown to one of:
        *   win
        *   nix
        *   mac
    
    ![](http://localhost:63342/markdownPreview/386105395/cptam-common?_ijt=65mqrbimo9tv30fsdmo1dj7f93)
    
    `mvn deploy:deploy-file \ -Durl=https://tr1.jfrog.io/tr1/libs-release-local/checkpoint-release \ -DrepositoryId=checkpoint-release \ -Dfile=target/xgboost4j-OSALIAS-2.1.4.jar \ -DgroupId=ml.dmlc \ -DartifactId=xgboost4j-OSALIAS \ -Dversion=2.1.4`