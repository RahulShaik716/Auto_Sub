import datetime 
import whisper 
import os
import sys
model = whisper.load_model('base.en')
option = whisper.DecodingOptions(language='en',fp16 = False)
path = sys.argv[1]
dir_list = os.listdir(path)
for file1 in dir_list:
    filename = os.path.join(path,file1)
    result = model.transcribe(filename)
    save_target = filename.replace('.ts','.srt')
    print(save_target)
    with open(save_target,'w') as file: 
        for indx,segment in enumerate(result['segments']):
            file.write(str(indx+1)+'\n')
            file.write(str(datetime.timedelta(seconds=segment['start']))+'--->'+str(datetime.timedelta(seconds=segment['end']))+'\n')
            file.write(segment['text'].strip()+'\n')
            file.write('\n')