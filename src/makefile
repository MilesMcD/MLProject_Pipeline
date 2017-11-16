#Make can be downloaded here: https://www.gnu.org/software/make/
#http://gnuwin32.sourceforge.net/packages/coreutils.htm
#adding this to your path will give you some necessary linux commands.
IRIS_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
TaxRevByGDP_URL = "https://ourworldindata.org/taxation/"
HappinessDataOverTime_URL = "https://ourworldindata.org/happiness-and-life-satisfaction/"


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
#INCOME TAX, GINI INDEX, & SOCIAL INCLUSION
#Process Data
data/processed/TaxRateGDP.pickle: data/raw/total-tax-revenues-gdp.csv
	python data/preprocess.py --fixheader=True $< $@ --excel data/processed/TaxRateGDP.xlsx
data/processed/noInterplSocialInclusion.pickle:	data/raw/online-data-chapter-2-whr-2017.xlsx
	python data/preprocess.py --fromexcel=0 --multi=1,2 $< $@ --excel data/processed/noInterplSocialInclusion.xlsx
	
#Interpolate
data/processed/SocialInclusion.pickle: data/raw/online-data-chapter-2-whr-2017.xlsx
	python data/preprocess.py --fromexcel=0 --multi=1,2 --intrpl=True $< $@ --excel data/processed/SocialInclusion.xlsx
reports/figures/interpolations.png: data/processed/SocialInclusion.pickle
	python visualizations/SIP_explorations.py $< $@ --secondfile data/processed/noInterplSocialInclusion.pickle
	
#Merge Sets
data/processed/mergedSet.pickle: data/processed/SocialInclusion.pickle
	python data/data_joiner.py $< data/processed/TaxRateGDP.xlsx $@ --fromexcel2=0 --excel data/processed/mergedSet.xlsx

#Complete interpolation
data/processed/HappSocGinTax_Interpolated.pickle: data/processed/mergedSet.pickle
	python data/preprocess.py $< $@ --intrpl=True --preprocessed=True --excel data/processed/HappSocGinTax_interpolated.xlsx 

#Find change/year
data/processed/HapSocGinTaxDiff.pickle:	data/processed/HappSocGinTax_Interpolated.pickle
	python data/deltatizer.py $< $@ --excel data/processed/HSGTDiffValues.xlsx

#Drop incomplete rows.
data/processed/HappSocGinTax_Interpolated_NoNA.pickle: data/processed/mergedSet.pickle
	python data/preprocess.py $< $@ --dropna=True --preprocessed=True --excel data/processed/HappSocGinTax_interpolated_NoNA.xlsx 
data/processed/HSGT_Averages.pickle: data/processed/HappSocGinTax_Interpolated_NoNA.pickle
	python data/preprocess.py $< $@ --preprocessed=True --getaverages=0 --excel data/processed/HSGT_Averages.xlsx
models/HSGT_kmeans.model: data/processed/HSGT_Averages.pickle
	python models/train_model.py --alg km $< $@

	#LETS ADD HAPPINESS INFORMATION
data/interim/happinessladder.pickle: data/raw/happiness-cantril-ladder.csv
	python data/preprocess.py --csvheader=0  --multi="0,2" $< $@ --excel data/interim/happinessladder.xlsx
data/interim/HapReportHappy.pickle: data/processed/mergedSet.pickle
	python data/data_joiner.py $< data/interim/happinessladder.pickle $@ --excel data/interim/HapReportHappy.xlsx	
data/interim/HapReportHappy_Interp.pickle: data/interim/HapReportHappy.pickle
	python data/preprocess.py $< $@ --intrpl=True --preprocessed=True --excel data/processed/HapReportHappy_Interp.xlsx 
data/interim/SatSocGinTax_Trimmed.pickle: data/interim/HapReportHappy_Interp.pickle
	python data/data_selector.py $< $@ 2 3 4 6 --trimcat=True --trimna=True --excel data/interim/SatSocGinTax_Trimmed.xlsx
data/processed/SatSocGinTaxNorm_Final.pickle: data/interim/SatSocGinTax_Trimmed.pickle
	python data/preprocess.py $< $@ --preprocessed=True --normalize=True  --excel data/processed/SatSocGinTaxNorm_Final.xlsx
models/SatSocGinTaxSVR.model: data/processed/SatSocGinTaxNorm_Final.pickle
	python models/train_model.py --alg svr $< $@
