from docx import *
import re  
import spacy
import spacy
from spacy.tokenizer import Tokenizer
from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER, CONCAT_QUOTES, LIST_ELLIPSES, LIST_ICONS
from spacy.util import compile_infix_regex
import datetime
import os
from django.conf import settings

def custom_tokenizer(nlp):
    infixes = (
        LIST_ELLIPSES
        + LIST_ICONS
        + [
            r"(?<=[0-9])[+\-\*^](?=[0-9-])",
            r"(?<=[{al}{q}])\.(?=[{au}{q}])".format(
                al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES
            ),
            r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
            r"(?<=[{a}0-9])[:<>=/](?=[{a}])".format(a=ALPHA),
        ]
    )

    infix_re = compile_infix_regex(infixes)

    return Tokenizer(nlp.vocab, prefix_search=nlp.tokenizer.prefix_search,
                                suffix_search=nlp.tokenizer.suffix_search,
                                infix_finditer=infix_re.finditer,
                                token_match=nlp.tokenizer.token_match,
                                rules=nlp.Defaults.tokenizer_exceptions)


nlp = spacy.load("en_core_web_trf")
nlp.tokenizer = custom_tokenizer(nlp)


class CaseApi:
  def __init__(self,doc):
    self.document = Document(doc)

  def extracting_data(self,case,style):
    

    for para in self.document.paragraphs:
      #"Title_document"
      if para.style.name==style:
        #print(style)
        title=para.text
        # self.raw(self.extracting_token_title(title))
        if case=="titlecase":
          para.text=(self.titlecase(self.extracting_token_title(title)))
          #print("New: ",para.text)          
        else:
          para.text=(self.sentence_case(self.extracting_token_title(title)))  
          #print("New: ",para.text)  
    # self.data_to_file(document)         

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
      if b != "NOUN" and b != "CCONJ" and b != "ADP" and b != "DET" and not re.search("[A-Z][a-z]?\d*|\((?:[^()]*(?:\(.*\))?[^()]*)+\)\d+",a) and a not in re.findall("[a-z]+[A-Z]+",a):
        new_token.append(a.title())
        print('title change',a.title())
      else:
        new_token.append(a)
    new_token=self.modified_token(new_token)
    return new_token

  def sentence_case(self,text):
    new_token = []
    for a, b in text:
      if b == "NOUN" or b == "CCONJ" or b == "ADP" or b=="DET" and  re.search("[A-Z][a-z]?\d*|\((?:[^()]*(?:\(.*\))?[^()]*)+\)\d+",a) and a not in re.findall("[a-z]+[A-Z]+",a):#test
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
    mod_token = mod_token.replace(" / ","/")
    mod_token = mod_token.replace(" ,", ",")
    
    return mod_token

  def data_to_file(self,dc_name):
    filename = dc_name
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
    self.document.save(filepath)
    return "media/output/"+time_stamp_for_dir+"/"+filename
    

def calling_case(doc,dct, d_name):
  cc=CaseApi(doc)
  output = None
  for i in dct.keys():
    cc.extracting_data(dct[i],i)
    output = cc.data_to_file(d_name)
  return output
    