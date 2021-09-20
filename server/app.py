# Importing Necessary modules
import keras
import keras.backend as K
from keras.preprocessing.sequence import pad_sequences
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import numpy as np
import pickle
LATENT_DIM_DECODER = 128


def softmax_over_time(x):
    assert(K.ndim(x) > 2)
    e = K.exp(x - K.max(x, axis=1, keepdims=True))
    s = K.sum(e, axis=1, keepdims=True)
    return e / s


word2idx_inputs = pickle.load(
    open('Attention/Dumps/word2idx_inputs.pkl', 'rb'))
word2idx_outputs = pickle.load(
    open('Attention/Dumps/word2idx_outputs.pkl', 'rb'))

idx2word_eng = {v: k for k, v in word2idx_inputs.items()}
idx2word_trans = {v: k for k, v in word2idx_outputs.items()}

decoder_model = keras.models.load_model(
    'Attention/Models/decoder_model.h5', custom_objects={"softmax_over_time": softmax_over_time})
encoder_model = keras.models.load_model(
    'Attention/Models/encoder_model.h5', custom_objects={"softmax_over_time": softmax_over_time})

tokenizer_inputs = pickle.load(
    open("Attention/Dumps/tokenizer_inputs.pkl", "rb"))
tokenier_outputs = pickle.load(
    open("Attention/Dumps/tokenizer_outputs.pkl", "rb"))


def decode_sequence(input_text):
    text = []
    text.append(input_text)
    input_seq = tokenizer_inputs.texts_to_sequences(text)
    input_seq = pad_sequences(input_seq, maxlen=6)
    # Encode the input as state vectors.
    enc_out = encoder_model.predict(input_seq)

    # Generate empty target sequence of length 1.
    target_seq = np.zeros((1, 1))

    # Populate the first character of target sequence with the start character.
    # NOTE: tokenizer lower-cases all words
    target_seq[0, 0] = word2idx_outputs['<sos>']

    # if we get this we break
    eos = word2idx_outputs['<eos>']

    # [s, c] will be updated in each loop iteration
    s = np.zeros((1, LATENT_DIM_DECODER))
    c = np.zeros((1, LATENT_DIM_DECODER))

    # Create the translation
    output_sentence = []
    for _ in range(16):
        o, s, c = decoder_model.predict([target_seq, enc_out, s, c])

        # Get next word
        idx = np.argmax(o.flatten())

        # End sentence of EOS
        if eos == idx:
            break

        word = ''
        if idx > 0:
            word = idx2word_trans[idx]
            output_sentence.append(word)

        # Update the decoder input
        # which is just the word just generated
        target_seq[0, 0] = idx

    return ' '.join(output_sentence)


class Item(BaseModel):
    input_text: str


# Declaring our FastAPI instance
app = FastAPI(
    title='NMT Model API using Attention',
    description='NMT Model made using Global Attention Mechanism and Teacher forcing',
    version='0.1'
)

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def main():
    return {'HELLO'}


@app.get('/{name}')
def hello_name(name: str):
    return {'message': f'Welcome!, {name}'}


@app.post('/predict')
def predict(input_text: Item):
    translation = decode_sequence(input_text.input_text)
    return {'predicted_translation': translation}
