**To run:**
- Run 
  - python awsEC2.py on your shell
- The shell will print 
  - "Paste this in your browser: IP_ADDRESS"
- Copy this IP and save it in a notepad. Will need this later
- Run and fill in the PUBLIC-IP-ADDRESS with the IP from the previous step
  - scp -i KEY.pem sshSetup.sh ubuntu@PUBLIC-IP-ADDRESS:~
- Run and fill in the PUBLIC-IP-ADDRESS with the IP from the previous step
  - ssh -i KEY.pem ubuntu@PUBLIC-IP-ADDRESS
- Run
  - sh sshSetup.h
- Paste IP address on the browser.
  
