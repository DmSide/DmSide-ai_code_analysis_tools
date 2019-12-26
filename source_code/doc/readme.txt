To start server you need to:
clone project from git
install all requirements (sudo pip install -r requirements)
run manage.py runserver to start server and manage.py process_tasks to start background tasks

************************************************************************************************

            API

        test_exception_work
        Description: testwork
        Input:
        Output:
        {
            "status": true,
            "response": {},
            "error": {}
        }

        prepare_db
        Description: preparing db
        Fields:
        name: str, name of db
        Input:
        {
            "name": "test"
        }
        Output:
        {
            "status": true,
            "response": {},
            "error": {}
        }


        get_accounts_list
        Description: get list of all github accounts in git_ifo.git_account collection
        Fields:
        Input:
        Output:
        {
            "status": true,
            "response": {
                "accounts list":
                [
                    {
                        "_id": "5d1dc750e9da6076a10a28c6",
                        "account_id": "id",
                        "account_type": "gitlab",
                        "base_url_http": "https://",
                        "baser_url_ssh": "ssh:",
                        "username": "",
                        "password": "",
                        "ssh_key": "path/to/ssh_key_file",
                        "api_key": "API_KEY"
                    }
                ]
        },
            "error": {}
        }

        get_account
        Description: get account from git_ifo.git_account collection by id
        Fields: account_id
        Input:
        {
            "account_id": "5d1dc750e9da6076a10a28c6"
        }
        Output:
        {
            "status": true,
            "response": {
                "account": {
                    "_id": "5d1dc750e9da6076a10a28c6",
                    "account_id": "id",
                    "account_type": "gitlab",
                    "base_url_http": "https://",
                    "baser_url_ssh": "ssh:",
                    "username": "",
                    "password": "",
                    "ssh_key": "path/to/ssh_key_file",
                    "api_key": "API_KEY"
                }
            },
            "error": {}
        }

        delete_account
        Description: delete account from git_ifo.git_account collection by id
        Fields: account_id
        Input:
        {
            "account_id": "5d1dc750e9da6076a10a28c6"
        }
        Output:
        {
            "status": true,
            "response": {},
            "error": {}
        }

        check_path
