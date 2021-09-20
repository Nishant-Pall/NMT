# NMT
NMT model made using tensorflow/keras and made use of global attention to handle long sequences

## Installation

### To install the front-end
```
git clone https://github.com/Nishant-Pall/NMT
cd client/
yarn
```
### To install the back-end
```
cd server/
pip3 install -r requirements.txt
```

## Running

To run the server
```
cd server/
uvicorn app:app --reload
```
To run the front end
```
cd client/
yarn start
```
