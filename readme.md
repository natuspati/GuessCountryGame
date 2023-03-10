# Guess Country: Daily Guessing Game

Guess a new country every day. The game shows incrementally country
capital/region/population and flag.

## Description

Game shows a user a hidden country. Country data is stored in a session.
Each guessing attempt sends HTMX request to ``` GuessCountry:check-check ```.
Upon the first loading the index page, several scenarios are possible:

* User has no country data, i.e. no session key ``` country_data ``` exists.
  * New user.
  * Initial condition for game state is set.
* User has country data, but ``` country['id'] ``` is different from today.
  * Existing user, who has not played the game today.
  * Initial condition is set.
* User has country data with same ``` country['id'] ``` and
session key ``` finished=True ```.
  * Existing user, who has completed the game today.
  * End state is shown.
  * End state reveals whole information on the hidden country.
* User has country data with same ``` country['id'] ``` and
session key ``` finished=False ```.
  * Existing user, who has not completed the game today.
  * The game from the previous attempt is restored.

Registered users' scores are stored in the database.

API is available to work with ```Country``` and ```Score``` models.
User data exposed with ```email``` attribute.
Score data is exposed with ```uuid``` field. 

> **Warning**: SQLite database does not handle ```uuid``` field.
> It yields integer overflow for CRUD operations. Use more advanced database.


## Getting Started

### Dependencies

* Tested on UNIX-like systems

### Installing

* Some TBD steps.
* Load test data from json to a database.
```shell
python manage.py loaddata db.json
```
* If session backend is database (e.g.```Dev``` settings), create cache table.
```shell
python manage.py creatcachetable
```

### Executing program

#### Dev

* TBD (how to run with dev settings)

```shell
export DJANGO_SETTINGS_MODULE=GuessCountryGame.settings.dev
python manage.py runserver 127.0.0.1:8000
```
#### Dev

* TBD (how to run with prod settings)

```
export DJANGO_SETTINGS_MODULE=GuessCountryGame.settings.prod
```

## Help

TBD

## Authors

Nurlat Bekdullayev [@natuspoati](https://twitter.com/natuspati)

## Version History

How it should look like:
* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under the
[MIT License](https://www.mit.edu/~amini/LICENSE.md).

## Acknowledgments

Inspired by 

* [Worldle](https://worldle.teuteuf.fr/)