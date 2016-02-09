mkdir c:\temp\rblogs

xcopy C:\n\Dropbox\csd\VCS-git\cif207 \\PMDS-DATA\p2\xampp\htdocs\python\cif207   /s/e/d/h/i/f/c/k/y 

robocopy C:\n\Dropbox\csd\VCS-git\cif207 \\PMDS-DATA\p2\xampp\htdocs\python\cif207  /l  /COPY:DT /xd  templates_c /fft /dst /xo /ndl /np /r:0 /w:9 /tee /log:"c:\temp\rblogs\cif207-%dhms%-%random%-%random%"

:robocopy C:\n\Dropbox\csd\VCS-git\cif207 \\PMDS-DATA\p2\xampp\htdocs\python\cif207   /e  /COPY:DT /xd .git templates_c testnobackup /fft /dst /xo /ndl /np /r:0 /w:9 /tee /log:"c:\temp\rblogs\cif207-%dhms%-%random%-%random%"

robocopy C:\n\Dropbox\csd\VCS-git\cif207 \\v206b2\html\python\cif207   /e  /COPY:DT /xd .git templates_c testnobackup /fft /dst /xo /ndl /np /r:0 /w:9 /tee /log:"c:\temp\rblogs\cif207-%dhms%-%random%-%random%"

pause
