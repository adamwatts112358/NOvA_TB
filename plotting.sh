data_dir=/pnfs/ebd/persistent/g4bl/$1

# Copy over all data files for that run
for dir in $data_dir/*
do
	cp $dir/*.txt .
done

# Cleanup from previous runs
rm -f ./.*png
rm -rf ./combined_data

# Combine data into one txt file per detector
mkdir ./combined_data
python -W ignore plot_detectors.py

# Cleanup
rm -f ./*.txt