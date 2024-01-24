# Let's find some athletes out

Simple scraper for retriving data from [www.strava.com](https://www.strava.com/).

## Purpose

This repository can be used as an API for other apps to help data integration.

## Configuration - SetUp

You might need at first some environment variables or a *.env* file at root. (There is a *template* sample also)

- STRAVA_USER
- STRAVA_PSW  (**It might be in base64 :D**)


⚠️ As you will be using an account, you might be using it carefully. This scraper is using sessions to avoid logging multiple times, although each request should be used wisely.