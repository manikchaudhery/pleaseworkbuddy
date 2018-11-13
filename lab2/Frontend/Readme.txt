

To run:

Go to http://34.199.148.90  (functionality works without login part)

To run fully functional website locally:

1) Go to the Frontend Folder
2) Run python searchEngine.py from the terminal.

Benchmarking:

-While running ab commands we kept getting timeout erros, we tried fixing it by changing the number of threads and the processes and even extending the time limit to 9999s.

-However, we still kept running into time out errors and hence we were not able to generate the benchmarking report and derive the observations from it.



Error in submission on Saturday(As emailed to the Head TA, Richard):

Me and my partner (Zafeer, who made the first submission on Saturday) just realized we made an error in submitting the lab yesterday. We hosted our website on aws and the google login functionality of the lab does not work on the ec2 instance, but it works locally.
 
We are really sorry, we just realized that as were reading the handout submission guidelines and putting the required stuff into the folder to submit, we accidentally missed putting the tpl files which show the user history and the whole google login functionality and just submitted the searchEngine.py file. We forgot that the functionality does not work on aws and would not be available to view unless you run it on localhost.
 
We had worked really hard for this lab over the past week and we extremely sorry that this mistake happened, we uploaded all our files to github before deploying them at this link: 

https://github.com/manikchaudhery/pleaseworkbuddy/tree/master/bottle-master
 
As you can see the revision history for all the files is before the deadline. This is the same repo we have used to deploy the EC2 instance. If you clone the repo and run searchEngine.py, and all the modules are installed, the functionality will work perfectly fine on 54.87.231.248.
 
Once again, we are both extremely sorry and apologize for the error we made in this submission. We worked really hard for this lab, if you could please consider the repository it will be a huge help to us. We assure you will never repeat this mistake in the future.
 
Regards,
Manik


