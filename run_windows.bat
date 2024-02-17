@echo off


echo "=========== STARTING MINIBOT CLIENT GUI ==============="
cd ./static/gui
start /b npm run webpack
echo "=========== STARTING BASESTATION ==============="
cd ../..
flask run