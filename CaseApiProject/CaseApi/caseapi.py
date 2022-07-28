from docx import *
import re
import spacy
from django.conf import settings
import datetime
import os
nlp=spacy.load('en_core_web_trf')
class CaseApi:
  def _init_(self):
    pass
  def extracting_data(self,doc,case, doc_name):
    document = Document(doc)

    for para in document.paragraphs:
      if para.style.name=="Title_document":
        title=para.text
        self.raw(self.extracting_token_title(title))
        if case=="titlecase":
          para.text=(self.titlecase(self.extracting_token_title(title)))
        else:
          para.text=(self.sentence_case(self.extracting_token_title(title)))                

      elif para.style.name=="Head1":
        title=para.text
        self.raw(self.extracting_token_title(title))
        if case=="titlecase":
          para.text=(self.titlecase(self.extracting_token_title(title)))
        else:
          para.text=(self.sentence_case(self.extracting_token_title(title)))
      
      elif para.style.name=="Head2":
        title=para.text
        self.raw(self.extracting_token_title(title))
        if case=="titlecase":
          para.text=(self.titlecase(self.extracting_token_title(title)))
        else:
          para.text=(self.sentence_case(self.extracting_token_title(title)))

      elif para.style.name=="Head3":
        title=para.text
        self.raw(self.extracting_token_title(title))
        if case=="titlecase":
          para.text=(self.titlecase(self.extracting_token_title(title)))
        else:
          para.text=(self.sentence_case(self.extracting_token_title(title)))
    
    return self.data_to_file(document, doc_name)

  def extracting_token_title(self,title):
    tokens = []
    token_pos = []
    txt = nlp(title)
    for token in txt:
      tokens.append(token.text)
      token_pos.append(token.pos_)
      text = zip(tokens, token_pos)
    return text

  def raw(self,text):
    new_token = []
    for a, b in text:
      new_token.append(a)
    new_token=self.modified_token(new_token)
    print("RAW: ",new_token)

  def titlecase(self,text):
    new_token = []
    for a, b in text:
      if b != "NOUN" and b != "CCONJ" and b != "ADP" and b != "DET" and a.isalnum()==False:
        new_token.append(a.title())
      else:
        new_token.append(a)
    new_token=self.modified_token(new_token)
    return new_token

  def sentence_case(self,text):
    new_token = []
    for a, b in text:
      if b == "NOUN" or b == "CCONJ" or b == "ADP" or b=="DET" or a.isalnum()==True:
        new_token.append(a)
      else:
        new_token.append(a.lower())
    new_token=self.modified_token(new_token)
    new_token=new_token[0].capitalize()+new_token[1:]
    return new_token

  def modified_token(self,new_token):
    mod_token = " ".join(new_token)
    mod_token = mod_token.replace('( ', '(')
    mod_token = mod_token.replace(" )", ")")
    mod_token = mod_token.replace("[ ", "[")
    mod_token = mod_token.replace(" ]", "]")
    mod_token = mod_token.replace("{ ", "{")
    mod_token = mod_token.replace(" }", "}")
    mod_token = mod_token.replace(" :", ":")
    return mod_token

  def data_to_file(self,document, d_name):
    filename = d_name
    time_stamp_for_dir = str(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M"))
    # Parent Directory path
    try:
        if not os.path.exists(r""+settings.MEDIA_ROOT+"output"):
            root_dir_path = os.path.join(r""+settings.MEDIA_ROOT, "output") 
            os.mkdir(root_dir_path)
    except Exception as err_root_dir_path:
        print("Error while trying to create root directory-->", err_root_dir_path)

    parent_dir = r""+settings.MEDIA_ROOT+"output/"
  
    # Path
    try:
        path = os.path.join(parent_dir, time_stamp_for_dir)
        os.mkdir(path)
    except Exception as dir_err:
        print("Error while trying to make directory-->", dir_err)
    filepath = r""+settings.MEDIA_ROOT+"output/"+time_stamp_for_dir+"/"+filename
    document.save(filepath)
    return "media/output/"+time_stamp_for_dir+"/"+filename


