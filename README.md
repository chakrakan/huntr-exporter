# Huntr-Exporter

🚀 A job board exporter tool for the Huntr Chrome extension.

## The Problem

**First of all, let me preface everything by stating that [Huntr](http://huntr.co/) has been very helpful to quickly get up and running with tracking of all my job applications in 
one central location and I strongly urge that you pay it forward to the developers if/when you manage to land a job (I plan on doing so).**

Prior to stumbling upon Huntr, I wanted to simply track everything in a spreadsheet. However, the thought of not having the workflow automated in some shape/form put me off that, plus, I wanted the flexibility to look back at job postings again in case it expires/is removed. 
On top of that, I also wanted to create visualizations of the data that I gather such as creating [Sankey diagrams](https://en.wikipedia.org/wiki/Sankey_diagram) and much more. 

I wanted to build a tool very similar to Huntr, but since it already existed, it made no sense to try and re-invent the wheel especially when the primary purpose of all this was to apply to jobs and track them, and not spend precious time doing what others have already done.
. 

Now that I am using the app, however, there are a few things
that I wanted within which are not available to me (makes sense as a design decision from their perspective):

- Ability to track more than 40 jobs (after all, finding the right one is a numbers game)
- Ability to export a job board to a parsable format such as CSV, JSON, or to a Excel spreadsheet
- Ability to create different types of diagrams from the data itself rather than the ones provided in their paid offering of a simple curve diagram of application trends over time.

Now due to the paid model that Huntr has, exporting data is something that is unlikely for them to offer because it enables any user 
to continuously add and remove jobs as required, and simply use their service as a html tag selector to get relevant job details off a posting.

This tool will allow you to do exactly that - grab the data, and make sense out of it in whichever way you'd like.

## Usage

1. Before you do anything, make sure you setup a virtual env and install all dependencies from the requirements file for your [respective working environment](https://docs.python.org/3/tutorial/venv.html)
2. Create a .env file at the base of the project with the necessary variables as defined in .env.sample
3. Run the script using `python main.py`

## Note

You can also un-archive your past boards temporarily and get info from those by populating 
the `ARCHIVED_BOARD_NAME` environment variable in your env and setting the title accordingly.

Then re-archive old boards to continue adding to the main board in use.




