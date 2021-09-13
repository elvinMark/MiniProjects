# Y.A.R.V.I.S
**Y**et **A**nother **R**eliable **V**irtual **I**ntelligent **S**ystem

## About 
This is my I-lost-track-of-the-number attempt to make an AI Virtual
Assistant. Hopefully, this time I will get it done. 

## Requirements

- PyAudio (to get audio input from the mic)
- SpeechRecognition (using some api to do some speech recognition)
- gtts (using google api to convert text to speech)
- mpg123 (play mp3 audios)

## Progress Log

### listener
- Got constant input from the mic using PyAudio and store the obtained waveform
  data in a buffer.
- Data from the buffer is also converted to text using SpeechRecognition.

### speaker
- Converts any text to speech and save it into an mp3 file using gtts.
- Play the mp3 file with mpg123. (I know, I know, it is not efficient and
  honestly not aesthetically good either but I will find a better way later -maybe-)
