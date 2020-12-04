import boto3
from pydub import AudioSegment
import os
import pydub
import subprocess
import json


def generate_voice():
    polly_client = boto3.Session(
        aws_access_key_id='AKIAJSNUEM4XXIJU4WSQ',
        aws_secret_access_key='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',
        region_name='ap-northeast-2').client('polly')
    # 경로수정 필요
    pydub.AudioSegment.converter = "./tts_storage/ffmpeg/bin/ffmpeg.exe"
    with open("./tts_storage/text/tts_script.txt", encoding='utf-8') as file_in:
        data = []
        text_ = ''
        for line in file_in:

            text_ += line
            print("## TTS script:",line)
        data.append(text_)
    for i in range(0, len(data)):
        response = polly_client.synthesize_speech(VoiceId='Seoyeon',
                                                  OutputFormat='mp3',
                                                  Text=data[i] + ' .')

        file = open('./tts_storage/sound/seoyeon_{}.mp3'.format(i), 'wb')
        file.write(response['AudioStream'].read())
        file.close()

        src = "./tts_storage/sound/seoyeon_{}.mp3".format(i)
        dst = "./text_conversion/data/test/tts.wav".format(i)
        subprocess.call(['ffmpeg', '-i', 'seoyeon_{}.mp3'.format(i), '-c', 'pcm_u8', 'tts.wav'.format(i)])

        sound = AudioSegment.from_mp3(src)
        sound.export(dst, format="wav", parameters=["-c:a", "pcm_u8"])
        os.remove("./tts_storage/sound/seoyeon_{}.mp3".format(i))
