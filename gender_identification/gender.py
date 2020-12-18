import gender_identification.test_extraction_voting as t
import pickle

def test_prediction():
    ALLOWED_EXTENSIONS = {'flac', 'wav'}  # lossless formats/extensions.
    MODELS_PATH = './gender_identification/models'
    dataPath_test = "./voice_conversion/data/test"  ##### 확인할 음원 위치 수정필요 ####
    delimeter = '/'
    path_praat = './gender_identification/myspsolution.praat'  # Path to .praat file.
    file = open(MODELS_PATH + '/latestML', 'rb')
    modelML = pickle.load(file)
    file.close()
    filename = 'voice.wav'
    return (t.model_preds_nn(modelML, dataPath_test, filename, path_praat))[0]

