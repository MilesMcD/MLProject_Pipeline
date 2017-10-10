#Make can be downloaded here: https://www.gnu.org/software/make/
#http://gnuwin32.sourceforge.net/packages/coreutils.htm
#adding this to your path will give you some necessary linux commands.
IRIS_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
#this will remove any raw data csvs.

#these are not related to file structure.
.PHONY: all clean

all: data/raw/iris.csv
clean:
	rm -f data/raw/*.csv
data/raw/iris.csv:
	python data/download.py $(TEST_URL) $@
	

