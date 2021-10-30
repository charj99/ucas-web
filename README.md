# ucas-web
ucas web homework: password analysis
* environment
  - python 3.9.0
  - other requirements are in **requirements.txt**
    ```shell
    pip install -r requirements.txt # install packages for python
* input
  - **Pure data**, manually deleted other messages
* run anlysis
  ```shell
  python mainAnalyze.py -y # for YaHoo dataset
  # or
  python mainAnalyze.py -c # for CSDN dataset
  ```

  there are three types of analysis:
  - analyzeComponent, gernerate following files:
    * calculate different passwords,   and save to "YaHoo/CSDN-passwords.txt"
    * calculate password patterns,     and save to "YaHoo/CSDN-patterns.txt"
    * calculate digital sequences,     and save to "YaHoo/CSDN-digits.txt"
    * calculate character sequences,   and save to "YaHoo/CSDN-characters.txt"
    * calculate other sequences,       and save to "YaHoo/CSDD-specials.txt"
    * caluclate diffent email types,   and save to "YaHoo/CSDN-emails.txt"
  - analyzePinyin, generate following files:
    * calculate different pinyins,     and save to "YaHoo/CSDN-pinyins.txt"
    * calculate different words,       and save to "YaHoo/CSDN-words.txt"
  - analyzeRelation, generate following files:
    * calculate how many password are the same as id or email, and save to "YaHoo/relations.txt"
  
  **notice:**
    1. **You should set analyzer in mainAnalyze.py manually.** Run one analyzer each time to save time.
    2. **analyzeComponent** is enough for PCFG
    3. **analyzePinyin** is not accurate enough, see "results/YaHoo-pinyins" and "results/CSDN-pinyins"
    
* build dictionary
  ```shell
  python mainDictionary.py -y # for YaHoo dataset
  # or
  python mainDictionary.py -c # for CSDN dataset
  ```
  Result will be saved in "YaHoo/CSDN-dictionary.txt"  
* results
  Results of each analyzer for both dataset are saved in directory ./results
---
## TODO
* Visualize the data!
* Maybe add multi-processing for anaylyzePinyin, which is too slow
