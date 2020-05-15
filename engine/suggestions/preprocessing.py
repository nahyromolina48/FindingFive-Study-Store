import os

class CorpusCreation():
    def __init__(self):
        self.path =os.path.join(os.getenv('HOME')+'/csc480/deployment/corpus/')
        self.master = "master.txt"
        self.stoplist = {" ","--","\n","!","\"","#","$","%","&","'","(",")","*","+",",","-",".","/",":",";","<","=",">","?","@","[","\\","]","^","_","`","{","|","}","~"}
    def parse_files(self):
        #for each file grab the lemma or word, write to a central file.
        dir_files=os.listdir(self.path)
        dir_files.remove(self.master)
        with open(self.path+self.master,"w+")as par_f:
            for cur_file in dir_files:
                with open(self.path+cur_file,"r",encoding="iso-8859-1") as f:
                    print(cur_file)
                    for line in f:
                        if cur_file == "corpus.txt" or cur_file =="american-english":
                            par_f.write(line.strip())
                            par_f.write("\n")
                        else:
                            result=line.split(" ")
                            word = result[2].lower()
                            if word in self.stoplist:
                                continue
                            par_f.write(word)
                            par_f.write("\n")

    def read_corpus(self):
        corpus_path = self.path+"master.txt"
        with open(corpus_path,"r") as f:
            for line in f:
                yield line
if __name__=='__main__':
    cc=CorpusCreation()
    cc.parse_files()
