# AliasRemover
Detecting and making report for the usage of C# aliases - such as int instead of Int32, or double instead of Double...

## Longer description

Recursively searches for all .cs files in the directory tree starting from the current directory (where the AliasRemover.py is located) and detects the use of C# aliases in them. A report is made both in console and stored in the the directory of the script. 

Location of the final report file can be altered by setting the REP_FILE value in the python script. Default is ./AliasRemoverReport.txt

## Notes

Please note that the removing (replacing) functionality is not yet present.

Run with Python3
