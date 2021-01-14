# LZU-AutoHealth-Submit
For the automation of LZU-Health-Submitting.
## The way of using it
### Part 1 libraries for python
You have to install some libraries listed below:
`requests` and `selenium`.
We recommend you to change the source of pip to Tsinghua instead of waiting for such a long time...
After you installed those libraries, let's go to the second part
### Part 2 Selenium and chrome for linux
Here's a guide you can use to install those:
`https://blog.csdn.net/fengltxx/article/details/79622854`
### Part 3 Setting crontab
Use ``crontab -u [your user name] -e `` to open the crontab for your user
the set `minute hour * * * [your python env(absolute path)] [the path for this script(also the absolute path)]`
After that, we can let the server sign up for us LOL!
