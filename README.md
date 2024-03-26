# Slack Progress Bar Upload App
A project repo that shows an example of using the [SlackProgressBar](https://github.com/mlizzi/slack-progress-bar) 
package. 



## System Setup
The `upload_app.py` application can run on your local machine and demonstrates how a project might make use 
of the SlackProgressBar package. Other examples include tracking the progress of file downloads, ML training epochs, 
or bulk testing hardware like CPUs. 

The `flask_app.py` application runs alongside a redis instance to enable Slack API's slash commands. Endpoints 
created such as `\subscribe` and `\unsubscribe` allow the user to turn on and off update messages on Slack.


