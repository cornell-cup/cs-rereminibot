# run this script in the parent directory of cs-rereminibot
# if there is no permission to execute this script:
# chmod +x cs-rereminibot/installation.sh
# to run this script:
# ./cs-rereminibot/installation.sh
conda env create --name cup --file=cs-rereminibot/environment.yml
conda activate cup
cd cs-rereminibot/static/gui
npm install
cd ../..
chmod +x ./run_BS.sh
./run_BS.sh