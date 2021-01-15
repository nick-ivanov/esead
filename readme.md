# esead
Ethereum Social Engineering Attack Detector (ESEAD)  
Required environment: Python 3.7.4 or above  
Required packages: re, numpy, ethereum.utils    

## How to run:  
Open the terminal, then input the following command

```
python3 detector.py contract_name
```
where contract_name is the smart contract (directory+filename) which you are going to scan.  
The program will output the detection result, either "Benign" or "Suspicious" , for each type of vulnerability.  
If the result is "Suspicious", the program will output the details.



 










