# Udacity Logs Analysis

A python CLI tool to list popular authors, % of error responses and top articles of the news site.


## Setup

To run this program, you will need to have python version 3 installed in your system along with postgresql database.

To install python 3, visit - [https://www.python.org/downloads/](https://www.python.org/downloads/)

To check if python is installed successfully, run the below command in your terminal:

```
python --version
```

It is possible postgressql is already installed in your operating system distribution. If thats not the case, you can download and install postgresql at [https://www.postgresql.org/download/](https://www.postgresql.org/download/)

To install this program dependencies, run:

```
pip install -r requirements.txt
```

We recommend you running this program dependencies in a virtual environment to isolate this project dependencies with the one used by other programs or your system.

## Configuration

Rename .env.example file to .env and fill in your database credentials.


### Optional
If you do not have the site's data in your local database, you can [download the example data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and load it to your local database using below commands.

```
createdb news
psql -d news -f /path/to/newsdata.sql
```

Here `createdb` creates a database with name `news`. You can name your database as you like, but make sure it to be same as the one specified in `DB_NAME` variable in .env file. 

## Usage

Run the below command in your terminal to get the desired results.

```
python analytics.py
```

To run analytics.py file directly in your linux machine, run:

```
chmod +x analytics.py

./analytics.py
```

To generate the output to a file instead of a terminal, run

```
python analytics.py > output.txt
```

Note: `In case the above setup suffues your use case, you can skip this part.`

To isolate this project enviroment with your system and also to make it portable, you can create a virtual machine with the above setup instructions.

We'd recommend vagrant as it provides the easiest and the fastest way to create and manage a virtualized environment!. Please refer [Vagrant docsumenation](https://www.vagrantup.com/docs/index.html) on how to create and manage a virtual machine.