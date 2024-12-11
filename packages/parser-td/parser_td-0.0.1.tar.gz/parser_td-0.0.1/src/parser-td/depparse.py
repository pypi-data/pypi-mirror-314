import stanza
from stanza.resources.common import download_models


stanza.download('th')

download_list = [('depparse', 'best_transformer_parser')]
resources = {
    'th': {
        'depparse': {
            'best_transformer_parser': {
                'url': "https://huggingface.co/nlp-chula/Thai-dependency-parser/resolve/main/th_best_transformer_parser_checkpoint.pt",
                'md5': None
            }
        }
    }
}

download_models(
    download_list=download_list,
    lang='th',
    resources = resources,
    model_dir='/root/stanza_resources',
    model_url="https://huggingface.co/nlp-chula/Thai-dependency-parser/resolve/main/th_best_transformer_parser_checkpoint.pt"
)


import logging
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
logging.getLogger("stanza").setLevel(logging.ERROR)
logging.getLogger("stanza.models").setLevel(logging.ERROR)
logging.getLogger("stanza.models.pos").setLevel(logging.ERROR)

from stanza.pipeline.processor import ProcessorVariant, register_processor_variant
from stanza.models.common.doc import Document
from stanza.models.common import doc
from stanza.pipeline.core import Pipeline
from stanza.pipeline._constants import *
from stanza.pipeline.pos_processor import POSProcessor
from stanza.pipeline.lemma_processor import LemmaProcessor
from stanza.models.pos.data import Dataset


@register_processor_variant('pos', 'non')
class PythaiPOStag(ProcessorVariant):
    def __init__(self, config):
        pass
    def process(self, text):
        return text

@register_processor_variant('lemma', 'non')
class PythaiPOStag(ProcessorVariant):
    def __init__(self, config):
        pass
    def process(self, text):
        return text
    
def pos_process(self, document):
    maximum_tokens = self.config.get('batch_maximum_tokens', 5000)
    args = {'shorthand': 'default', 'word_cutoff':1, 'bert_model': None, 'sample_train': 1.0, 'pretrain': False, 'augment_nonpunct':0.0}
    dataset = Dataset(document, args, False)
    batch = iter(dataset.to_length_limited_loader(batch_size=5000, maximum_tokens=maximum_tokens))
    for _, b in enumerate(batch):
        pred_num = b.text
        pred_num = len(pred_num[0])

    dataset.doc.set([doc.UPOS, doc.XPOS, doc.FEATS], [['.', '.', '_']] * pred_num)
    return dataset.doc

def lemma_process(self, document):
    maximum_tokens = self.config.get('batch_maximum_tokens', 5000)
    args = {'shorthand': 'default', 'word_cutoff':1, 'bert_model': None, 'sample_train': 1.0, 'pretrain': False, 'augment_nonpunct':0.0}
    dataset = Dataset(document, args, False)
    batch = iter(dataset.to_length_limited_loader(batch_size=5000, maximum_tokens=maximum_tokens))
    for _, b in enumerate(batch):
        pred_num = b.text
        pred_num = len(pred_num[0]) # can change to text

    dataset.doc.set([doc.UPOS, doc.XPOS, doc.LEMMA], [['.', '.', '.']] * pred_num)
    return dataset.doc

def load_model():
    POSProcessor.process = pos_process
    LemmaProcessor.process = lemma_process
    nlp = stanza.Pipeline(
    lang='th',
    processors='tokenize,pos,lemma,depparse',
    depparse_model_path= "/root/stanza_resources/th/depparse/best_transformer_parser.pt",
    depparse_pretrain_path= "/root/stanza_resources/th/pretrain/fasttext157.pt",
    depparse_forward_charlm_path="/root/stanza_resources/th/forward_charlm/oscar.pt",
    depparse_backward_charlm_path="/root/stanza_resources/th/backward_charlm/oscar.pt",
    use_gpu=False,
    pos_with_non=True,
    lemma_with_non=True)
    return nlp

def depparse(text, depparse_model):
    token = depparse_model(text.replace(' ', ''))
    return token