#!/bin/bash
pip install -r requirements.txt

cd web_server/client
npm install
npm run build

cd ../server
npm install
npm start &

cd ../../backend_server
python service.py &

cd ../news_recommendation_service
python recommendation_service.py &
python click_log_processor.py &

echo "=================================================="
read -p "PRESS [ENTER] TO TERMINATE PROCESSES." PRESSKEY

kill $(jobs -p)
