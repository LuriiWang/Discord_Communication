### What, When and How do Software Practitioners Communicate in the Live Chat on Discord?

---
*Package Structure*
The artifact consists of following three parts：
- Data
  
  These datasets are used for analysis in subsequent four RQs.

  - *DataZIP*：This folder contains original data extracted by DiscordChatExporter, which is stored in zip format.
  - *DataJSON*: This folder contains utterances extracted from zip files in *DataZIP*, which are stored in json format.
  - *DataTXT*: This folder contains the utterances with timestamp, username and utterance content, which are extracted from JSON files.
  - *DataDialog*: This folder contains the diloags generated by auto disentanglement and manual disentanglement, based on txt files in *DataTXT*.
  - *DataThematic*：This folder contains the manual annotation results of dialogs for their topic and interaction pattern, based on dialogs in *DataDialog*.
  - *DataAscii*: This folder stores the results of the files which have been converted into ascii format, including texts from *DataTXT* and manually disentangled dialogs from *DataDialog/Manual*.
  - *DataRQ*: This folder stores the results of each RQ.
  
- Code

  - *Preprocess*：This folder contains snippets used to preprocess the collected data.

  - *ThematicAnalysis*：This folder contains codebooks for annotation of topic and interaction pattern (RQ2 and RQ3).
  
  - *QuantitativeAnalysis*：This folder contains snippets used to generate results for RQ1, RQ2 and RQ4.

- Figure

  This folder contains the pdfs for all figures in the paper. All these figures are generated by using Excel.

*Requirements*

- OS：
~~~
A Windows system; Python version 3.8.10; R version 4.2.2.
~~~

- Hardware：
~~~
X86/X64 CPU; 2GB Storage.
~~~

Note that a Linux system and NVIDIA GPU(s) with > 1G memory is needed if you want to run FF model for automatic disentanglement.

<!--Although it is recommended to run the artifact with NVIDIA GPUs for faster analysis, it is not a requirement. When there is no GPU available, the CPU will be responsible for running the artifact.-->


**Reproduce the results:**
1. Data Collection
<!-- requirement 
~~~
Windows
~~~-->
To collecet the data, we used Graphical User Interface (GUI) of the DiscordChatExporter, the detailed instructions of it can be found on its [guide section](https://github.com/Tyrrrz/DiscordChatExporter/blob/master/.docs/Getting-started.md#using-the-gui). You just need to select the community channel and type in time slot in need. Then you can get the target utterances in target format (we chose json here). 
We selected seven popular technical communities in the Discord platform and further chose one general channel for each community as bellow:

| Community  | Channel                                                                                     | Start Time | End Time  |
|------------|---------------------------------------------------------------------------------------------|------------|-----------|
| Docker     | - Community/Docker                                                                          | 2018/6/25  | 2022/3/30 |
| Redis      | - General Discussion/redis-general                                                          | 2020/9/1   | 2022/3/30 |
| TensorFlow | - Discussion/tf-general                                                                     | 2017/12/27 | 2022/3/30 |
| TypeScript | - General/ts-discussion                                                                     | 2018/11/3  | 2022/3/30 |
| VSCode     | - Visual Studio Code/vsc-support-2                                                          | 2018/7/21  | 2022/3/30 |
| Angular    | - Angular/Question1                                                                         | 2020/8/30  | 2022/3/30 |
| Android    | - beginner/help-old                                                                         | 2017/8/16  | 2022/3/30 |

The collected utterances are stored in *./data/DataZIP/** in zip format.

First, you need to decompress the zip files to extract the data.
How to: Run this command from the specified directory: *./Code/preprocess/.py*

2. Data Preprocessing
   - Preprocessing Utterances
 
     We proprecessing the collected utterances in following two stages:
     
     (i) filtered out the utterances that are generated by channel bots, or contain no text but only pictures. 
     (ii) removed the emojis in the utterances by using a Python library.

       How to: Run this command from the specified directory: ./Code/preprocess/ChangeStyle.py
       Output: The output is stored in *./Data/DataTXT/**
       
     <!--The datasets we preprocessed locate in ./Data. Each utterance consists of a timestamp, a username, and a textual message.-->
       
   - Dialog Disentanglement
     
     (i) Automatic disentanglement
     We run [FF model](https://jkk.name/irc-disentanglement/) for a large-scale dialog disentanglement automatically.
      + If you want to reproduce the result of automatic disentanglement, you can install [FF model](https://jkk.name/irc-disentanglement/) by following their instructions.
      <!--T+ How to: Run the following commands in order from the specified directory: 
        1. *./Code/Disentanglement/DatasetDealing.py*
        2. *./Code/Disentanglement/GetAscii.sh*
        3. *./Code/Disentanglement/GetDialogs.sh*
        4. *./Code/Disentanglement/OutputDealing.py*
        5. *./Code/Disentanglement/DialogFormat.sh*-->
   
      + Output: The dialogs generated by automatic disentanglement are stored in *./Data/DataDialog/Auto/**
      Specifically, dialogs in a file are separated by dotted lines.
      <!--The dialogs obtained from automatic disentanglement are stored under the folder "NAME" in txt files.--> 
      <!-- File : ./Code/disentanglement--> 
  
     (ii) Manual disentanglement
     Based on the number of dialogs per community estimated in (i), we curated a manual disentanglement sample dataset for thematic analysis.
     - Output：The dialogs generated by manual disentanglement are in *./Data/DataDialog/Maunal/**
     <!--the folder "NAME" in text files.-->
    
After the above steps, we obtained two datasets for subsequent analyses. 


3.Research Questions
You can generate the quantitative results in each RQs by following the instructions below：

### RQ1
   - Generate statistics for Fig.4: 
  Run script: *./Code/QuantitativeAnalysis/RQ1/Get_Longtail.py* 
  Output: the results are stored in *./Data/DataRQ/RQ1/longtail_addinfo.csv*

   - Generate statistics for Fig.5: 
  Run script: *./Code/QuantitativeAnalysis/RQ1/Get_Hourly.py* 
  Output: the results are stored in *./Data/DataRQ/RQ1/hourly.csv*

   - Generate statistics for Fig.6: 
  Run script: *./Code/QuantitativeAnalysis/RQ1/Get_Weekly.py*
  Output: the results are stored in *./Data/DataRQ/RQ1/weekly.csv*
  
   - Get the response time of dialogs in Dataset I: 
  Run script: *./Code/QuantitativeAnalysis/RQ1/Get_Speed.py*

### RQ3
- Get the similarity between questions：
  Run script: *./Code/QuantitativeAnalysis/RQ3/Get_TFIDF.py*

- Generate Fig.10:
  Run script: *./Code/QuantitativeAnalysis/RQ3/Get_VoilinPlot.py*

### RQ4
To generate TABLE VI, run the R script *./Code/QuantitativeAnalysis/RQ4/Regression.R* you can find more details in the script.
(i) You need to download R according to the [instructions](https://cran.r-project.org/mirrors.html)
(ii) Then run the commands from the specified directory to get the results of regressions:
    *setwd(".\\Discord\\Data\\DataRQ\\RQ4")*
    *source(".\\Discord\\Code\\QuantitativeAnalysis\\RQ4\\Regression.R",echo = TRUE)*
   
The paper figures are in *./Figure
