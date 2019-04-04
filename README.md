# SI 507_pjt4

## What it does

This program scrapes the US national park service webpage and collect the information about parks in a csv file.
The information includes the name, type, location, and description of each park.

## How it works

Once it scrapes data from the website, it generates a cache file and make a csv file based on the cache file until the information on the website changes.
It gets string from the website, find information from certain tags, extract texts from them and write information to each row. Also, it fills out empty space with 'NA'.

## Requirements

bs4
