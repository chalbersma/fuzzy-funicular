
to-minimal:

* miniclient.sh
    * Build a small client (`miniclient.sh`) that telnets into the server regularly
    * have miniclient log requests to cloudwatch (added things to security group to allow)

* miniserver.sh
    * Add cloudwatch logging for pings recieved
    * Have it actually send pongs

* buildout.sh Improvements
    * Place Code on Provisioned Instances (likely SSH for the small stuff)
    * Initialize Code with a config file of some sort to tell it where to hit.

