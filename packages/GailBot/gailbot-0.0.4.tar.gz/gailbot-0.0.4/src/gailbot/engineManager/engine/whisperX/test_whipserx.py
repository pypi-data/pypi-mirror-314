import gailbot
from gailbot.engineManager.engine.whisperX.whisperX import WhisperX
from gailbot.engineManager.engine.whisperX.whisperXSetting import WhisperXSetting

setting = WhisperXSetting()
# setting.engine = "whisperX"
# setting.output_format = "all"
# setting.language = "en"
# setting.interpolate_method = "nearest"
# setting.min_speakers = 1
# setting.max_speakers = 2
# setting.temperature = 1
# setting.condition_on_previous_text = False
# setting.initial_prompt = None
# setting.vad_onset = 0.5
# setting.vad_offset = 0.363
# setting.chunk_size =  30
# setting.no_speech_threshold = 0.6
print("created")

whisp = WhisperX(setting)

audio = "/Users/evacaro/Desktop/test.wav"
payload = "/Users/evacaro/GailBot/gailbot_workspace/temporary/test_0618_11_14_09_068129/transcribe_ws"

transcription = whisp.transcribe(audio_path= audio, payload_workspace= payload)

print("done ", transcription)