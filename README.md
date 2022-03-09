# GVE_DevNet_Meraki_Sensor_Trigger_For_Snapshots
This tool provides a simple page to (1) configure a Meraki sensor to trigger a Meraki camera snapshot, which is sent to the user over Webex, and (2) manually trigger the same process (snapshot + Webex notification) without a sensor trigger. To allow for public reachability of the tool by the Meraki ecosystem, the tool is designed to be deployed on [Heroku](https://dashboard.heroku.com/).

## Contacts
* Stien Vanderhallen

## High-level Overview

![](/INTERNALDOCS/overview.png)

## Solution Components
* Meraki Camera
* Meraki Sensor
* Webex
* Heroku

## Installation/Configuration

0. Open a new terminal, and clone this repository

```
$ git clone https://wwwin-github.cisco.com/gve/GVE_DevNet_Meraki_Sensor_Trigger_For_Snapshots
$ cd GVE_DevNet_Meraki_Sensor_Trigger_For_Snapshots
```

1. Create your own fork of this repository

- In a browser, navigate to [GitHub](www.github.com) and log into your account (or make a new one)
- Create a new repository named `GVE_DevNet_Meraki_Sensor_Trigger_For_Snapshots` using the top-right `New Repository` button (other options can be left to their default values).
- In a terminal, set this new repository as the new remote:
```
$ git remote rename origin old
$ git remote add origin https://wwwin-github.cisco.com/<YOUR-GITHUB-USERNAME>/GVE_DevNet_Meraki_Sensor_Trigger_For_Snapshots
```
- In a terminal, push all code to your new repository:
```
$ git branch -M master
$ git push -u origin master
```

2. Deploy your fork to Heroku

- In a browser, navigate to [Heroku](https://dashboard.heroku.com/) and log into your account (or make a new one)
- Create a new app using the `New` button on the top right of the Heroku dashboard.
- In the `Deploy` tab of your new app, select `GitHub` as the `Deployment method`.
- Log into GitHub, and select your forked repository
- Select the `master` branch of your repository, and click `Deploy Branch` to deploy your version of this tool to Heroku.

3. Find your webhook URL

- In a browser, navigate to [Heroku](https://dashboard.heroku.com/) and log into your account (or make a new one)
- Select the app you created in step 2. 
- On the top right, click `Open app`
- In a new tab, your app will be opened.
- Copy the URL of the page hosting your app (Generally, this URL is `https://<YOUR-APP-NAME.herokuapp.com>`), and refer to this URL further in this guide as `WEBHOOK_URL`. 

4. Create a Webex bot

- In a browser, navigate to [Webex](https://developer.webex.com/) and log into your account (or make a new one)
- Click `Start Building Apps`, then `Create a New App`
- Select `Bot`
- Give your bot a suitable name, username, icon and description.
- Copy the API token displaying after creating your bot, and refer to this URL firther in this guide as `WEBEX_BOT_API_KEY`.

5. Configure your tool

- Navigate to your `WEBHOOK_URL` (see also step 3).
- On the landing page, select `Settings`
- Fill out the following settings, according to the page:
  - `Meraki API key`: Your Meraki API key
  - `Webex bot API key`: Your Webex bot API key (see also step 4 - `WEBEX_BOT_API_KEY`)
  - `Webex account e-mail`: The e-mail you use for your Webex account
  - `Webhook URL`: Your webhook URL (see also step 3 - `WEBHOOK_URL`)
  - In the other fields, you can customise the tool to work for a specific sensor/camera pair. You select the organization and network in which both reside, and their serial numbers. 
- Click `Submit`


## Usage

1. In a browser, navigate to your `WEBHOOK_URL` (see step 3 in the above installation guide)

2. To set off the snapshot trigger:
- EITHER trigger the attached sensor
- OR click the `Snapshot` button on the tool

3. Monitor your Webex App for receiving the snapshot

4. Optional: Recofigure your app by clicking `Settings`

# Screenshots

- **Landing page:** Either set of the snapshot process manually, or configure its settings.

![](/IMAGES/landing.png)

- **Settings page:** Configure the sensor, camera and Webex bot used foor the snapshot process

![](/IMAGES/settings.png)

- **Webex notification:** An example of the Webex notifications generated after the snapshot process is triggered.

![](/IMAGES/webex.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
