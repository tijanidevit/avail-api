### Set up, Installation & Usage.

**Make sure Docker is on and running before running this. It will build the python image on first run**

```
docker-compose up
```

### Packages consumed

##### Flask

For handling requests and responses. The framework serves as the server

##### datetime

For date time manipulation and operations e.g getting current time, holidays, getting time from another country

##### requests

Used to send api request to the calendarific api

##### pytz

Used to handle timezones with country codes e.g getting country code timezone etc

### Packages consumed

#### Calendarific api

- Used to check if a date is holiday in a country.
- It was used instead of holidays package because some holidays vary like the Islamic holidays, but calenderific is always updated

##### Flask

##### datetime

##### requests

##### pytz
