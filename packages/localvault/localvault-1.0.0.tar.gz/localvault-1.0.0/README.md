# Crypter

```Crypter``` - A command line utility to generate random **passwords** for the given **username/key**. It generates random passwords on the fly using **encryption algorithm** and store **locally** to access them later. In today's time where privacy is the major concern, **crypter** saves you with not only storing your **passwords** locally but also being hacked at the end. It allows you to be your own master and makes sure your secrets are completely secret to you.

##### Requirements
- Python 3.6

## Installation
Since the project is in the development mode, following steps can be followed to install the crypter utility.
```
git clone https://github.com/mukultaneja/crypter.git
pip install -e .
pip install -r requirements.txt
```

## Features
```Crypter``` is in the **active development phase** currently and comes with the very basic set of commands to `add/delete/get/list` username/passwords in the system. Following the set of available commands can be used with crypter,

```
Usage: crypter [OPTIONS] COMMAND [ARGS]...

  Crypter - A command line utility to generate random passwords for the given
  username & key. It generates random passwords on the fly using pre-defined
  encryption algorithm and store locally to access them later. It saves you
  from not storing your username/passwords on the third party storage and
  being hacked at the end. It allows to be your own master where your secrets
  are completely secret to you.

Options:
  --help  Show this message and exit.

Commands:
  add     Add a new username/password tagged with the given key.
  cloud   Option to configure cloud account to backup your secrets. [ Work in Progress ]
  delete  Delete the username/password tagged with the given key if any.
  get     Fetch the username/password tagged with the given key if any.
  init    Perform the inital setup required to save your secrets.
  list    List all the stored username/passwords.
  
```

Any username/password record requires a key to be tagged with. The key can be any random string and will be used later to access the username/password record. Internally crypter manages its own database to store username/password.


## Examples
```
crypter add key
Please provide KeyName: google
Please provide userName: testUser
A new record has been added with the following details,
[
    {
        "key": "google",
        "name": "testUser",
        "password": "zZ5]O4lN=l1=mD0!"
    }
]


crypter get key
Keyname: google
Following record(s) have been found with the given key(s),
[
    {
        "key": "google",
        "name": "testUser",
        "password": "zZ5]O4lN=l1=mD0!"
    }
]

crypter list
Following are the available record(s) in the system
[
  {
    "key": "google",
    "name": "testUser",
    "password": "zZ5]O4lN=l1=mD0!"
  }
]


crypter delete key
Keyname: google
Following record(s) have been deleted with the given key(s),
[
    {
        "key": "google",
        "name": "testUser",
        "password": "zZ5]O4lN=l1=mD0!"
    }
]
```

## Contributing
Every project requires continous feature requests and active developement around of it. We welcome contributions from the community. All contributions to this repository must be signed with username/email on that page. Your signature certifies that you wrote the patch or have the right to pass it on as an open-source patch. For more detailed information, refer to [CONTRIBUTING.md]().

## License
`Crypter` utility is being released with `BSD 3-Clause License`.