from pydub import AudioSegment
import os
import pydub
import subprocess
import json
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from xml.etree import ElementTree


def generate_voice():
    ############# AZURE #######################
    # set volume/rate/pitch -> volume default = 50
    rate = "-12%"
    pitch = "3%"
    vol_ = 10
    # AZURE 키 필요 
    speech_config = SpeechConfig(subscription="259174701e154db59bdd1e8af77a6423", region="eastus")
    speech_config.set_speech_synthesis_output_format(SpeechSynthesisOutputFormat["Riff24Khz16BitMonoPcm"])
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    num_ = 0
    # text file
    with open('./tts_storage/text/tts_script.txt', encoding='utf-8') as file_in:
        text = ""
        for line in file_in:
            text += line
        print("## TTS script:", text)

    root = ElementTree.fromstring(
        '<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="ko-KR"><voice name="ko-KR-SunHiNeural"><prosody  volume="{}" rate="{}" pitch="{}">{}</prosody></voice></speak>'.format(
            vol_, rate, pitch, text))
    xml_script = ElementTree.ElementTree()
    ElementTree.dump(root)
    xml_script._setroot(root)
    xml_script.write('ssml.xml')

        # src = "./tts_storage/sound/tts.wav"
        # dst = "./text_conversion/data/test/tts.wav"
        # subprocess.call(['ffmpeg', '-i', 'tts.wav', '-c', 'pcm_u8', 'tts.wav'])
        #
        # sound = AudioSegment.from_wav(src)
        # sound.export(dst, format="wav", parameters=["-c:a", "pcm_u8"])
        # os.remove("./tts_storage/sound/tts.wav")
