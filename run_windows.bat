@echo off


echo "=========== STARTING MINIBOT CLIENT GUI ==============="
cd ./static/gui
start npm run webpack
echo "=========== STARTING BASESTATION ==============="
cd ../..
flask run