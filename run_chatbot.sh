echo "============== STARTING CHATBOT QA ==================="
cd basestation/chatbot_qa_model
python server/app.py &
echo "============ START CHATBOT SENTIMENT ================="
cd ../chatbot_sentiment_model
KMP_DUPLICATE_LIB_OK=TRUE python sentiment_app.py