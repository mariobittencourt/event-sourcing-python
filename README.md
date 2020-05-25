# Event Sourcing 

This contains a sample implementation to illustrate keys aspects of implementing an application that uses Event Sourcing.

## Requirements

You have to have Python 3.7+ installed on your local system nad docker + docker-compose.

## Setup

1. Clone this repository

2. Install the Python dependencies

In a command line - or via your IDE of choice - run

`pip3 install -r requirements.txt`

If you are using a virtual environment (venv) replace the pip3 with simply pip.

3. Enable docker container

`docker-compose up -d`

It will download and run the event store (eventstore.org). Try to access it via localhost:2113

```
username: admin
password: changeit
```

4. Initialize the database that will contain the projections

`python3 setup.py`

You should see an output like the one below
```
Ledger persistence available
Payment projection available
Decline code projection available
```

If you ever need to reset the projections call the same script with a `-r` option after setup.py.

## Using

The system consists of 2 projections that should be run from command line to create projections (read models) of the system
for two different purposes.

- ./src/ui/console/manage_customer_payment_projection.py

It will create a projection stored in the SQLite table payment_view. It contains only the latest status of the payment.

- ./src/ui/console/manage_decline_code_projection.py

It will create a projection stored in the SQLite table decline_view. It contains a list of all declined payments organized
by the decline code, bank and date.

It also contains a helper script `api.py` that simulates the actions of API calls that would manipulate payments:
- create
- authorize
- settle
- refund
- decline
- find

For the full list of options you should run `python3 api.py -h`:
```
Usage: api.py [options]

Options:
  -h, --help            show this help message and exit
  -a ACTION, --action=ACTION
                        Which action to execute create, authorize, settle,
                        decline, refund or find
  -i ID, --id=ID        The payment ID to authorize, settle, decline, refund
                        or find
  -v VALUE, --value=VALUE
                        The amount to create, settle or refund
  -b BANK_NAME, --bank-name=BANK_NAME
                        The bank name
  -c DECLINE_CODE, --decline-code=DECLINE_CODE
                        The code for decline

```
With the exception of the `find` option, all the other commands, if successfully executed, will generate events that can
be seen by accessing: http://localhost:2113/web/index.html#/streams/$ce-payments
