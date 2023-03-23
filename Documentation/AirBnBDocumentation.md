# AirBNB Clone Console - MySQL Documentation

## The docs will be based on the tasks 0 to 10

### Background Context

### Environment variables will be your best friend for this project

- `HBNB_ENV`: running environment. It can be “dev” or “test” for the moment (“production” soon!)
- `HBNB_MYSQL_USER`: the username of your MySQL
- `HBNB_MYSQL_PWD`: the password of your MySQL
- `HBNB_MYSQL_HOST`: the hostname of your MySQL
- `HBNB_MYSQL_DB`: the database name of your MySQL
- `HBNB_TYPE_STORAGE`: the type of storage used. It can be “file” (using `FileStorage`) or db (using `DBStorage`)

### Resources

- Read or watch:

- [cmd module](https://intranet.alxswe.com/rltoken/OG2OW5Pbjs-ds3ZHT0ow4g)
- packages concept page
- [unittest module](https://intranet.alxswe.com/rltoken/g0tzN6ea1hWCj5OF99HB9w)
- [args/kwargs](https://intranet.alxswe.com/rltoken/F6YRBSrkkkTTMVc66iaMgA)
- [SQLAlchemy tutorial](https://intranet.alxswe.com/rltoken/GYWCmxokUZKAr-T93iQPcQ)
- [How To Create a New User and Grant Permissions in MySQL](https://intranet.alxswe.com/rltoken/m4ogDCoKVm3Us0FybYh1tA)
- [Python3 and environment variables](https://intranet.alxswe.com/rltoken/FJCSaX1TCf0HAOzhsH_eWA)
- [SQLAlchemy](https://intranet.alxswe.com/rltoken/bWxESLJVYGNonjOYg8fOVg)
- [MySQL 8.0 SQL Statement Syntax](https://intranet.alxswe.com/rltoken/n6ePnCDwnbQMbxGgeoe1VA)
- [AirBnB clone - ORM](https://intranet.alxswe.com/rltoken/gOVFXraZLW2XXXviMLQojg)

### General

- What is Unit testing and how to implement it in a large project
- What is `*args` and how to use it
- What is `**kwargs` and how to use it
- How to handle named arguments in a function
- How to create a MySQL database
- How to create a MySQL user and grant it privileges
- What ORM means
- How to map a Python Class to a MySQL table
- How to handle 2 different storage engines with the same codebase
- How to use environment variables

Python Unit Tests

- Allowed editors: `vi`, `vim`, `emacs`
- All your files should end with a new line
- All your test files should be inside a folder `tests`
- You have to use the `unittest module`
- All your test files should be python files `(extension: .py)`
- All your test files and folders should start by `test_`
- Your file organization in the tests folder should be the same as your project: ex: for `models/base_model.py`, unit tests must be in: `tests/test_models/test_base_model.py`
- All your tests should be executed by using this command: `python3 -m unittest discover tests`
- You can also test file by file by using this command: `python3 -m unittest tests/test_models/test_base_model.py`
- All your modules should have documentation `(python3 -c 'print(__import__("my_module").__doc__)')`
- All your classes should have documentation `(python3 -c 'print(__import__("my_module").MyClass.__doc__)')`
- All your functions (inside and outside a class) should have documentation `(python3 -c 'print(__import__("my_module").my_function.__doc__)' and python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)')`
- We strongly encourage you to work together on test cases, so that you don’t miss any edge cases

### Comments for your SQL file

```
$ cat my_script.sql
-- first 3 students in the Batch ID=3
-- because Batch 3 is the best!
SELECT id, name FROM students WHERE batch_id = 3 ORDER BY created_at DESC LIMIT 3;
$
```

### Tasks

#### 0. Fork me if you can

- In the industry, you will work on an existing codebase 90% of the time. Your first thoughts upon looking at it might include:

- “Who did this code?”
- “How it works?”
- “Where are unittests?”
- “Where is this?”
- “Why did they do that like this?”
- “I don’t understand anything.”
- “… I will refactor everything…”
But the worst thing you could possibly do is to **redo everything.** Please don’t do that! **Note: the existing codebase might be perfect, or it might have errors. Don’t always trust the existing codebase!**

For this project you will fork this [codebase](https://github.com/justinmajetich/AirBnB_clone.git):

- update the repository name to `AirBnB_clone_v2`
- update the `README.md` with your information but don’t delete the initial authors

If you are the owner of this repository, please create a new repository named `AirBnB_clone_v2` with the same content of `AirBnB_clone`

**Repo:**

- GitHub repository: `AirBnB_clone_v2`

## 1. Bug free

Do you remember the `unittest` module?

This codebase contains many test cases. Some are missing, but the ones included cover the basic functionality of the program.

```
guillaume@ubuntu:~/AirBnB_v2$ python3 -m unittest discover tests 2>&1 /dev/null | tail -n 1
OK
guillaume@ubuntu:~/AirBnB_v2$
```

All your unittests `must` pass without any errors at anytime in this project, `with each storage engine!`. Same for PEP8!

```
guillaume@ubuntu:~/AirBnB_v2$ HBNB_ENV=test HBNB_MYSQL_USER=hbnb_test HBNB_MYSQL_PWD=hbnb_test_pwd HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_test_db HBNB_TYPE_STORAGE=db python3 -m unittest discover tests 2>&1 /dev/null | tail -n 1
OK
guillaume@ubuntu:~/AirBnB_v2$
```

Some tests won’t be relevant for some type of storage, please skip them by using the `skipIf` feature of [the Unittest module - 26.3.6. Skipping tests and expected failures](https://intranet.alxswe.com/rltoken/Gx_1dJOPPeAyeM6NaXDmjg). Of course, the number of tests must be higher than the current number of tests, so if you decide to skip a test, you should write a new test!

### How to test with MySQL?

First, you create a specific database for it (next tasks). After, you have to remember what the purpose of an unittest?

**“Assert a current state (objects/data/database), do an action, and validate this action changed (or not) the state of your objects/data/database”**

For example, “you want to validate that the `create State name="California"` command in the console will add a new record in your table `states` in your database”, here steps for your unittest:
