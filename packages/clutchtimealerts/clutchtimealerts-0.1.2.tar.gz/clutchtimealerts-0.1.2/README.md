# ClutchTimeAlerts - NBA Clutch Time Alert Service

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A service that tracks ongoing NBA games and sends alerts when games enter "clutch time"—the last five minutes of the fourth quarter or overtime when the point difference is five points or fewer. The serivce monitors live game data and sends notifications via configured messaging platforms (such as GroupMe, Slack, etc.) to keep you informed of the most intense moments.

# Features
- **Real-Time Clutch Detection**: Monitors live NBA game data and detects when games enter clutch time.
- **Customizable Alerts**: Configure the service to send alerts on various platforms (GroupMe, Slack, etc.).
- **Multiple Game Support**: Tracks multiple NBA games simultaneously to ensure you don't miss any clutch moments.

# Supported Notification Types

We currently support the following notification types out of the box:

- **GroupMe** 
- **Slack**
- **Twilio** (SMS)

On our road map we want to expand the supported notification types. If there's a type you want to see supported add an issue or submit a PR for review.

# Installation 

There are two different supported installation types: Python and Docker.

**Python**

To install the python package, first clone the repository then use pip to install it.
 
```sh
git clone git@github.com:bwalheim1205/clutchtimealerts.git
cd clutchtimealerts
pip install clutchtimealerts
```

To install via docker, first clone the repository then build using the Dockerfile.

**Docker**

```sh
git clone git@github.com:bwalheim1205/clutchtimealerts.git
docker build clutchtimealerts/ -t clutchtimealerts
```

# Usage

## Configuration File

The alert system utilizes a yaml configuration file. YAML contains configuration 
options for SQLite database and alert method configurations. Here is an example
of a configuration file

**Example Configuration**

```yaml
db_file_path: clutchtime.db
db_table_name: clutchgames
notifications:
  - type: GroupMe
    config:
      bot_id: "<group-bot-id>"
  - type: Slack
    config:
      channel: "#general"
      token: "<slack-api-token>"
- type: Twilio
    config:
      account_sid: "<twilio-accout-sid>"
      auth_token: "<twilio-auth-token>"
      from: "+14155551212"
      to: 
        - "+14155551212"
        - "+14155551212"
```

### YAML Fields

**db_file_path** (__Optional__): Path to sqllite database to store game data. Defaults to clutchtime.db

**db_table_name** (__Optional__):  SQLite table name to store data in. Default to clutchgames

**notifications**: List of notification configs
-  **type**: class name or common name of the alert type
-  **config**: kwargs** for the alert classes


## Running Alert Service

Once you've generated a configuration file you can run alert service
using one of the following commands

**Python**

```sh
python3 -m clutchtimealerts -f <path-to-config>
```

**Docker**
```sh
docker run -v <path-to-config>:/app/config.yml clutchtimealerts
```