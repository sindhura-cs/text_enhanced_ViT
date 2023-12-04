# import torch.nn as nn
# from transformers.models.bert.modeling_bert import BertConfig, BertEmbeddings

# '''text-level module'''


# class TextLevelModule(nn.Module):
#     def __init__(self, config):
#         super(TextLevelModule, self).__init__()
#         self.bert_config = BertConfig(
#            vocab_size=config["vocab_size"],
#            hidden_size=config["hidden_size"],
#            num_hidden_layers=config["num_layers"],
#            num_attention_heads=config["num_heads"],
#            intermediate_size=config["hidden_size"]*config["mlp_ration"],
#             max_position_embeddings=config["max_text_len"],
#             hidden_dropout_prob=config["drop_rate"],
#             attention_probs_dropout_prob=config["drop_rate"],
#         )
#         self.text_embeddings = BertEmbeddings(self.bert_config)
#         self.token_type_embeddings = nn.Embedding(2, config["hidden_size"])

#     def forward(self, x):
#         x = self.text_embeddings(x)
#         return x

import torch.nn as nn
from transformers import BertConfig, BertModel, AutoTokenizer

'''text-level module'''

class TextLevelModule(nn.Module):
    def __init__(self, config):
        super(TextLevelModule, self).__init__()
        self.config = config
        
        if config["text_emb"] == "bert-base-uncased":
            self.bert_model = BertModel.from_pretrained(config["model_name"])
        elif config["text_emb"] == "biobert":
            self.bert_model = BertModel.from_pretrained("dmis-lab/biobert-v1.1")
        elif config["text_emb"] == "clinicalbert":
            self.bert_model = BertModel.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")

        self.tokenizer = AutoTokenizer.from_pretrained(config["model_name"])

    def forward(self, input_text):
        inputs = self.tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)
        outputs = self.bert_model(**inputs)
        return outputs.last_hidden_state
