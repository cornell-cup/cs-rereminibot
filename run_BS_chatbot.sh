#!/bin/bash
set -e
trap "kill 0" EXIT

echo "================= MINIBOT CLIENT GUI ================="
cd static/gui
npm run webpack &
echo "============== STARTING BASESTATION =================="
cd ../..
flask run &
echo "============== STARTING CHATBOT QA ==================="
cd basestation/chatbot_qa_model
python server/app.py &
echo "============ START CHATBOT SENTIMENT ================="
cd ../chatbot_sentiment_model
KMP_DUPLICATE_LIB_OK=TRUE python sentiment_app.py