from gailbot.transcriptionPipeline.pipeline import GBPipeline
from gailbot.sourceManager.sourceObject import SourceObject
from gailbot.profileManager.profileManager  import ProfileObject
from gailbot.engineManager.engine.engineProvider import EngineProvider
from gailbot.engineManager.engine.whisperX.whisperXProvider import WhisperXProvider
from gailbot.engineManager.engine.whisperX.whisperXSetting import WhisperXSetting


gb = GBPipeline()
source = "/Users/evacaro/Music/Music/Media.localized/Unknown Artist/Unknown Album/test.wav"
output = "/Users/evacaro/Desktop/test_out_2"
source_id = "test_analyze_name"

src_object = SourceObject(source_id= source_id, source_path= source, output= output)
setting = WhisperXSetting()
eng_prov = WhisperXProvider(name= "whisperxprov",  data= setting)
prof = ProfileObject(name= "test_eng_prov", profile_data= None, engine_provider= eng_prov, plugin_suites= None)
prof.name = "test_prof_name"
prof.profile_data = None
prof.plugin_suites = None
prof.engine_provider = eng_prov

src_object.initialize_profile(prof)
src_list = [SourceObject(source_id= source_id, source_path= source, output= output)]
print("about to convert\n")
convert_res = gb.convert(sources= src_list)
print("printing og source ids: ")
for id in convert_res.original_source_ids:
    print(id)
