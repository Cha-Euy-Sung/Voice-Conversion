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
    rate = "-3.0%"
    pitch = "low"
    speech_config = SpeechConfig(subscription="259174701e154db59bdd1e8af77a6423", region="eastus")
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    pydub.AudioSegment.converter = "./tts_storage/ffmpeg/bin/ffmpeg.exe"
    with open('./tts_storage/text/tts_script.txt', encoding='utf-8') as file_in:
        text = ""
        for line in file_in:
            text += line
        # print("## TTS script:",text)

        root = ElementTree.fromstring(
            '<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US"><voice name="ko-KR-HeamiRUS"><prosody rate="{}" pitch="{}">{}</prosody></voice></speak>'.format(
                rate, pitch, text))
        xml_script = ElementTree.ElementTree()
        ElementTree.dump(root)
        xml_script._setroot(root)
        xml_script.write('ssml.xml')

        ssml_string = open("./ssml.xml", "r", encoding='utf-8').read()
        result = synthesizer.speak_ssml_async(ssml_string).get()
        stream = AudioDataStream(result)
        stream.save_to_wav_file("./text_conversion/data/test/tts.wav")
