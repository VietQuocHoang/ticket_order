# ticket_order

## Challenge
A database table/model "Ticket" has 1 million rows. The table has a "token" column that holds a random unique UUID value for each row, determined by Django/Python logic at the time of creation. Due to a data leak, the candidate should write a django management command to iterate over every Ticket record to regenerate the unique UUID value. The command should inform the user of progress as the script runs and estimates the amount of time remaining. The script should also be sensitive to the potentially limited amount of server memory and avoid loading the full dataset into memory all at once, and show an understanding of Django ORM memory usage and query execution. Finally, the script should ensure that if it is interrupted that it should save progress and restart near the point of interruption so that it does not need to process the entire table from the start.


## Solution implemented
We will use iterator() to use server-size cursor and seperate the queryset into smaller chunk (In this case: 10000 items per chunk) to process.

With Iterator:
![With Iterator](/results/with_iterator.png "With Iterator Result")


Without Iterator:
![Without Iterator](/results/without_iterator.png "Without Iterator Result")

## Possible other solution
We will use paginator to seperate the whole queryset into page, then perform update on each page.


### Overview


### Installation guide

1. Prerequisite
- Python
- PostgreSQL

2. Install the required dependency by running:

```
> pip install -r requirements.txt
```

3. Copy the content from `.env.example` to `.env` file then fill in the configuration for PostgreSQL

4. Then running the migration to generate fake data (currently 1 million record):

```
> python manage.py migrate
```

5. Run the django webapp:

```
> python manage.py runserver
```

6. To run the UUID Regenerator, please run:

```
> python manage.py regenerate_token [--iterator=1] [--bulk=0]
```

For more information on this command, please run:
```
> python manage.py regenerate_token -h
```


7. (Optional) To generate the report, please run

```
> mprof run manage.py regenerate_token [--iterator=1] [--bulk=0]
> mrpof plot <mprofile_{timestamp.dat}> (if no file name is available, will visualize the most recent execution)
```
