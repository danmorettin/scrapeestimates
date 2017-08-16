
""" in case you want to run the application as a script """

from sys import argv
from scrapeestimates.application import Application

app = Application(argv)
app.run()
