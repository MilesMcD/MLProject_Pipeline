#Make can be downloaded here: https://www.gnu.org/software/make/
#http://gnuwin32.sourceforge.net/packages/coreutils.htm
#adding this to your path will give you some necessary linux commands.
IRIS_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
TaxRevByGDP_URL = "https://ourworldindata.org/taxation/"
#this will remove any raw data csvs.

#these are not related to file structure.
.PHONY: all clean test

all: data/raw/iris.csv reports/figures/exploratory.png data/processed/processed.pickle models/random_forest.model data/processed/processed.pickle data/processed/hapsui.pickle models/hapsui_kmeans.model
#Note: the '-' before rm will mean clean continues despite errors. Remove these for troubleshooting.
#WARN: CLEAN CURRENTLY DELETES MODELS. REMOVE FINALIZED MODELS BEFORE CLEANING THE PROJECT.
clean:
#	-rm -f data/raw/*.csv
	-rm -f data/processed/*.pickle
	-rm -f data/processed/*.xlsx
	-rm -f reports/figures/*.png
	-rm -f models/*.model
#test goes up a directory and calls a makefile that tests the size of the dataset.
test: all
	$(MAKE) -C .. all
#python -m pytest src
# $@ = first prerequisite
# $< = first target
#data/raw/iris.csv:
#	python data/download.py $(IRIS_URL)	$@
#reports/figures/exploratory.png: data/processed/processed.pickle
#	python visualizations/exploratory.py $< $@
#data/processed/processed.pickle: data/raw/iris.csv
#	python data/preprocess.py --cr cls $< $@ --excel data/processed/processed.xlsx
#models/random_forest.model: data/processed/processed.pickle
#	python models/train_model.py --alg rf $< $@
###SIP INFORMATION	
#For Happiness/suicide data
data/processed/hapsui.pickle: data/raw/HappinessAndGiniAndSuicides.xlsb.csv
	python data/preprocess.py --fixHeader==True $< $@ --excel data/processed/hapsui.xlsx
models/hapsui_kmeans.model:	data/processed/hapsui.pickle
	python models/train_model.py --alg km $< $@
#INCOME TAX & SOCIAL INCLUSION
data/processed/TaxRateGDP.pickle: data/raw/total-tax-revenues-gdp.csv
	python data/preprocess.py --fixheader=True $< $@ --excel data/processed/TaxRateGDP.xlsx
data/processed/noInterplSocialInclusion.pickle:	data/raw/online-data-chapter-2-whr-2017.xlsx
	python data/preprocess.py --fromexcel=0 --multi=True $< $@ --excel data/processed/noInterplSocialInclusion.xlsx
data/processed/SocialInclusion.pickle: data/raw/online-data-chapter-2-whr-2017.xlsx
	python data/preprocess.py --fromexcel=0 --multi=True --intrpl=True $< $@ --excel data/processed/SocialInclusion.xlsx
reports/figures/interpolations.png: data/processed/SocialInclusion.pickle
	python visualizations/SIP_explorations.py $< $@ --secondfile data/processed/noInterplSocialInclusion.pickle
data/processed/mergedSet.pickle: data/processed/SocialInclusion.pickle
	python data/data_joiner.py $< data/processed/TaxRateGDP.xlsx $@ --fromexcel2=0 --excel data/processed/mergedSet.xlsx

data/processed/HappSocGinTax_Interpolated.pickle: data/processed/mergedSet.pickle
	python data/preprocess.py $< $@ --intrpl=True --preprocessed=True --excel data/processed/HappSocGinTax.xlsx 

data/processed/HapSocGinTaxDiff.pickle: data/processed/HappSocGinTax_Interpolated.pickle
	python data/deltatizer.py $< $@ --excel data/processed/HSGTDiffValues.xlsx

