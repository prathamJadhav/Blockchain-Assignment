virtualenv env
source env/bin/activate
pip install -r requirements.txt
cd frontend/
npm install
npm run build
cd ..