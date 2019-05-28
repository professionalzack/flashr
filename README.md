# flashr

To use at home: fork this repo, clone it to your computer, then, in the command line, run:

```zsh
virtualenv .env -p python3
source .env/bin/activate
pip3 install -r requirements.txt
createdb flashr
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py loaddata db.json
python3 manage.py runserver
```

## Motto

```python
from project3.team import Friends
```

- **'before you catch errors, remember to catch each other'**

- **'git is your friend.'**

## Seeding Instructions

In the flashr repo is a file called db.json. This is the seed file.
The way it works is using something called Django Fixtures. More info:

- <https://docs.djangoproject.com/en/2.2/ref/django-admin/#what-s-a-fixture>
- <https://docs.djangoproject.com/en/2.2/howto/initial-data/>

To add the seed data, run:

```zsh
python3 manage.py loaddata db.json
```

## Technologies Used

1. Python

2. Django

3. SQL // POSTGRES // DBGLASS

4. Javascript

5. JQuery // AJAX

6. HTML // CSS

7. Heroku for Django

8. Trello (<https://trello.com/b/vrz8MIi1/flashr>)

9. Github (<https://github.com/professionalzack/flashr>)

## Process // Approach

- **XXTREME PAIR PROGRAMMING**
  
- Major Trello-ing

- Team Decisions

- Never forgetting **MVP** (scaling down)

As a team, we all spent the first day whiteboarding our ERD, tables, and wireframes. Once that was concluded, we went to Trello to plan our sprints.

When one of us were stuck, we approached the problem as team. Having one driver who will code and three passengers.

## Unsolved Problems

## Wins // Challenges

### Wins

- Finding an alternative way to seed the database through fixtures and DBGlass.

- Understanding tags and python cannot be written within.

- Scaling down our project to MVP.

### Challenges

- Creating the deck routes, view, and logic
  
  - Make a deck model that will give a user a personalized deck based on their pain level. 

- The community aspect.

## Future/Wish List

 - Comments on Answers
  
 - 'Hints' functionality
 
 - User submitted questions
  
 - Expand responsiveness and accessibility
 
 - Guest Mode
 
 - Expand Contributing Guidelines and Code of Conduct
 
 
 ## Contributing !
 
 **Fl\*shr** depends on community in order to work at all, so simply using it and saving public answers is contributing! While you are doing so, if you happen to encounter any bugs, errors, or simply have a cool idea you'd like to see in Fl\*shr, just [open an issue](https://github.com/professionalzack/flashr/issues).
 
 If you'd like to get *really* involved, fork the repo, make the changes of your dreams, and either make a pull request, or change the name and try and sell to some chump. Or, go through any [issues](https://github.com/professionalzack/flashr/issues)
 you see and try and correct them. Thanks!
