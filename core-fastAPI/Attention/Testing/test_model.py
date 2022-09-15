import keras
import keras.backend as K
from keras.preprocessing.sequence import pad_sequences
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


# text = "How are you"
# translation = decode_sequence(text)
# print('-')
# print('Input sentence:', text)
# print('Predicted translation:', translation)
