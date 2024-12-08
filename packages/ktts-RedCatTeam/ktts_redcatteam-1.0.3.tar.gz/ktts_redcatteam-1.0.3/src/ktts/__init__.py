from RUTTS import TTS
from ruaccent import RUAccent

accentizer=RUAccent()
accentizer.load(omograph_model_size='big_poetry', use_dictionary=True)
class KTTS:
    def load(self,tts):
        self.tts=TTS(tts,add_time_to_end=0.8)
    def say(self,text):
        text=accentizer.process_all(text)
        audio=self.tts(text,lenght_scale=0.7,play=True)

