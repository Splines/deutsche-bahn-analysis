<p align="center">
  <img alt="Live-Poll Logo" src="https://upload.wikimedia.org/wikipedia/commons/d/d5/Deutsche_Bahn_AG-Logo.svg" width="100" />
  <h3 align="center">Deutsche Bahn<sup>*</sup> Analysis</h3>
  <p align="center">Analyzing delays of the Deutsche Bahn (DB) in the course of 2023.</p>
</p>

| :warning:   | At the moment, this repo is primarily a playground for a funny little data science project. While I usually put in an effort to write clean and well-documented code, please note that these standards will suffer in this project as this is more aimed to "get things done" instead of writing the best code. And of course, things might change very often as this is a playground.|
|---------------|:-------------------------|

<sub><sup>(*) This project is not endorsed at all by the official Deutsche Bahn.</sup></sub>


## What is this?
While most of the time, at least in my experience, DB trains arrive on schedule, there are still these one or two situations where there is a huge delay or a small, yet big enough delay, so that you miss your connection. David Kriesel has conducted an extensive study of the DB in the course of 2019 and presented his results in a very engaging way at the chaos computer club (ccc) (see [this video](https://youtube.com/watch?v=0rb9CfOvojk)).

I wanted to do an analysis of the DB on my own and especially for the region I am living in including all regional trains. First, I will collect the data from the Bahn API and just dump the xml files on the filesystem. Then, data analysis is another step where I will probably read in all xml files, organize them in a database and draw conclusions (literally "draw" some nice plots 😅).

Some questions I hope to answer:
- At which time of the day are there the fewest delays per train connection?
- Given any train connection: what is the probability that it is delayed by 1,2,...30 minutes?
- At which time of the year are there the fewest delays? -> _Histogram_
- How late are trains on average & what delay is most common? _(e.g. result could be: 1-minute delays are most common)_
- Which stations have the most delays overall ? (_of course weighted with the number of total trains passing through that station_)
- At which station do trains "collect" most delays? -> _These are the stations you have to keep your fingers crossed._


## Setup
Create a `.env` file with these entries in the root of the cloned repository. You get the credential by registering for the [**DB API Marketplace**](https://developers.deutschebahn.com/db-api-marketplace/apis/) (for free).

```
CLIENT_ID=...
CLIENT_KEY=...
```

## Run
The script is intended to be run indefinitely in the background on a server.
```
python3 ./src/main.py
```

## Usefull scripts
```
python3 ./src/util/decompress.py
python3 ./src/util/date_converter.py
```
