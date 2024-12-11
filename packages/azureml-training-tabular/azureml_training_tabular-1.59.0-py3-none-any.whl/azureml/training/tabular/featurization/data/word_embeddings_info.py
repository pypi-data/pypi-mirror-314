# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Holder for embedding information."""
from typing import Dict, Optional
from urllib.parse import urljoin

from azureml.automl.core.automl_utils import get_automl_resource_url


class EmbeddingInfo:
    """Class to hold information of embeddings."""
    BERT_BASE_CASED = "bert-base-cased"
    BERT_BASE_UNCASED = "bert-base-uncased"
    BERT_BASE_UNCASED_AUTONLP_3_1_0 = "bert-base-uncased-automlnlp-3.1.0"
    BERT_BASE_MULTLINGUAL_CASED = "bert-base-multilingual-cased"
    BERT_BASE_MULTLINGUAL_CASED_AUTONLP_3_1_0 = "bert-base-multilingual-cased-automlnlp-3.1.0"
    BERT_BASE_CHINESE = "bert-base-chinese"
    BERT_BASE_CHINESE_AUTONLP_3_1_0 = "bert-base-chinese-automlnlp-3.1.0"
    BERT_BASE_GERMAN_CASED = "bert-base-german-cased"
    BERT_BASE_GERMAN_CASED_AUTONLP_3_1_0 = "bert-base-german-cased-automlnlp-3.1.0"
    BERT_LARGE_CASED = "bert-large-cased"
    BERT_LARGE_UNCASED = "bert-large-uncased"
    DISTILBERT_BASE_CASED = "distilbert-base-cased"
    DISTILBERT_BASE_UNCASED = "distilbert-base-uncased"
    DISTILROBERTA_BASE = "distilroberta-base"
    ENGLISH_FASTTEXT_WIKI_NEWS_SUBWORDS_300 = "wiki_news_300d_1M_subword"
    GLOVE_WIKIPEDIA_GIGAWORD_6B_300 = "glove_6B_300d_word2vec"
    ROBERTA_BASE = "roberta-base"
    ROBERTA_LARGE = "roberta-large"
    XLM_ROBERTA_BASE = "xlm-roberta-base"
    XLM_ROBERTA_LARGE = "xlm-roberta-large"
    XLNET_BASE_CASED = "xlnet-base-cased"
    XLNET_LARGE_CASED = "xlnet-large-cased"

    _all_ = [
        ENGLISH_FASTTEXT_WIKI_NEWS_SUBWORDS_300,
        GLOVE_WIKIPEDIA_GIGAWORD_6B_300,
        BERT_BASE_CASED,
        BERT_BASE_UNCASED,
        BERT_BASE_UNCASED_AUTONLP_3_1_0,
        BERT_BASE_MULTLINGUAL_CASED,
        BERT_BASE_MULTLINGUAL_CASED_AUTONLP_3_1_0,
        BERT_BASE_CHINESE,
        BERT_BASE_CHINESE_AUTONLP_3_1_0,
        BERT_BASE_GERMAN_CASED,
        BERT_BASE_GERMAN_CASED_AUTONLP_3_1_0,
        BERT_LARGE_CASED,
        BERT_LARGE_UNCASED,
        DISTILBERT_BASE_CASED,
        DISTILBERT_BASE_UNCASED,
        DISTILROBERTA_BASE,
        ROBERTA_BASE,
        ROBERTA_LARGE,
        XLM_ROBERTA_BASE,
        XLM_ROBERTA_LARGE,
        XLNET_BASE_CASED,
        XLNET_LARGE_CASED
    ]

    def __init__(
        self,
        user_friendly_name: str,
        embedding_name: str,
        download_prefix: str,
        language: str,
        file_name: str,
        lower_case: bool,
        license: str,
        credits: str,
        sha256hash: str,
    ) -> None:
        """
        Create embedding info object.

        :param user_friendly_name: human-readable name
        :param embedding_name: Name of the embedding.
        :param download_prefix: Prefix of the url to download from.
        :param language: 3 letter language abbreviation
        :param file_name: Name of the file to be appended to the prefix.
        :param lower_case: True if the embeddings were generated on strings
         after lower casing.
        """
        self._user_friendly_name = user_friendly_name
        self._embedding_name = embedding_name
        self._download_prefix = download_prefix
        self._file_name = file_name
        self._lower_case = lower_case
        self._license = license
        self._credits = credits
        self._sha256hash = sha256hash
        self._language = language


# TODO Make this a full fledged class and move to config
class WordEmbeddingsInfo:
    """Word embeddings information holder."""

    BERT_EMB_CASED_INFO = EmbeddingInfo.BERT_BASE_CASED
    BERT_EMB_INFO = EmbeddingInfo.BERT_BASE_UNCASED
    BERT_EMB_AUTONLP_3_1_0 = EmbeddingInfo.BERT_BASE_UNCASED_AUTONLP_3_1_0
    BERT_MULTI_EMB_INFO = EmbeddingInfo.BERT_BASE_MULTLINGUAL_CASED
    BERT_MULTI_EMB_AUTONLP_3_1_0 = EmbeddingInfo.BERT_BASE_MULTLINGUAL_CASED_AUTONLP_3_1_0
    BERT_GERMAN_EMB_INFO = EmbeddingInfo.BERT_BASE_GERMAN_CASED
    BERT_GERMAN_EMB_AUTO_NLP_3_1_0 = EmbeddingInfo.BERT_BASE_GERMAN_CASED_AUTONLP_3_1_0
    BERT_CHINESE_EMB_INFO = EmbeddingInfo.BERT_BASE_CHINESE
    BERT_CHINESE_EMB_AUTONLP_3_1_0 = EmbeddingInfo.BERT_BASE_CHINESE_AUTONLP_3_1_0
    XLNET_EMB_INFO = EmbeddingInfo.XLNET_BASE_CASED
    WORD_VEC_LINK = urljoin(get_automl_resource_url(), "data/wordvectors/")

    # List of models under consideration for pretrained_text_dnn (main AutoML Tabular),
    # only one model per language code should be represented in this list (this is unit tested)
    pretrained_model_names_for_languages = [
        EmbeddingInfo.BERT_BASE_UNCASED,
        EmbeddingInfo.BERT_BASE_GERMAN_CASED,
        # EmbeddingInfo.BERT_BASE_CHINESE, # Disabled due to inferior ml perf compared to multilingual bert
        EmbeddingInfo.BERT_BASE_MULTLINGUAL_CASED,
    ]
    embeddings = {
        EmbeddingInfo.ENGLISH_FASTTEXT_WIKI_NEWS_SUBWORDS_300: EmbeddingInfo(
            user_friendly_name="English word embeddings trained on wikipedia and web",
            embedding_name=EmbeddingInfo.ENGLISH_FASTTEXT_WIKI_NEWS_SUBWORDS_300,
            download_prefix=WORD_VEC_LINK,
            file_name="{base}.pkl".format(base=EmbeddingInfo.ENGLISH_FASTTEXT_WIKI_NEWS_SUBWORDS_300),
            lower_case=False,
            license="Creative Commons Attribution-Share-Alike License (3.0). More information can be found at: "
            "https://creativecommons.org/licenses/by-sa/3.0/",
            credits="Advances in Pre-Training Distributed Word Representations by "
            "P. Bojanowski, E. Grave, A. Joulin, "
            "T. Mikolov, Proceedings of the International Conference on Language Resources "
            "and Evaluation (LREC 2018). More information can be found at: https://fasttext.cc and "
            "https://arxiv.org/abs/1712.09405",
            sha256hash="e3fb56356cb4de3e9808bae83610ba2d25560155646607af363977d9a97ce32c",
            language="eng",
        ),
        EmbeddingInfo.BERT_LARGE_CASED: EmbeddingInfo(
            user_friendly_name="BERT pretrained model",
            embedding_name=EmbeddingInfo.BERT_LARGE_CASED,
            download_prefix=WORD_VEC_LINK,
            file_name="{base}.zip".format(base=EmbeddingInfo.BERT_LARGE_CASED),
            lower_case=False,
            license="Apache License Version 2.0, More information can be found at: "
                    "https://www.apache.org/licenses/",
            credits="Pretrained model on English language using a masked language modeling (MLM) "
                    "objective. It was introduced in https://arxiv.org/abs/1810.04805 "
                    "and first released in https://github.com/google-research/bert",
            sha256hash="003d598ca2e8b7c03bfbb4a30581b74ba4904b2d9b99a3e061a32b6242a40aa0",
            language="eng",
        ),
        EmbeddingInfo.BERT_LARGE_UNCASED: EmbeddingInfo(
            user_friendly_name="BERT pretrained model",
            embedding_name=EmbeddingInfo.BERT_LARGE_UNCASED,
            download_prefix=WORD_VEC_LINK,
            file_name="{base}.zip".format(base=EmbeddingInfo.BERT_LARGE_UNCASED),
            lower_case=True,
            license="Apache License Version 2.0, More information can be found at: "
                    "https://www.apache.org/licenses/",
            credits="Pretrained model on English language using a masked language modeling (MLM) "
                    "objective. It was introduced in https://arxiv.org/abs/1810.04805 "
                    "and first released in https://github.com/google-research/bert",
            sha256hash="d32ea6d86ee6f327b5e72c801c90327a5daa2db2e23f5d47310d61a0cbc34ac5",
            language="eng",
        ),
        EmbeddingInfo.DISTILBERT_BASE_CASED: EmbeddingInfo(
            user_friendly_name="DistilBERT pretrained model",
            embedding_name=EmbeddingInfo.DISTILBERT_BASE_CASED,
            download_prefix=WORD_VEC_LINK,
            file_name="{base}.zip".format(base=EmbeddingInfo.DISTILBERT_BASE_CASED),
            lower_case=False,
            license="Apache License Version 2.0, More information can be found at: "
                    "https://www.apache.org/licenses/",
            credits="DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter "
                    "by Victor Sanh, Lysandre Debut, Julien Chaumond, and Thomas Wolf. "
                    "Paper available at https://arxiv.org/abs/1910.01108.",
            sha256hash="737b9bddf859831549de74ab2037800461ef50632e21fcc46ce793bcd0912c4d",
            language="eng",
        ),
        EmbeddingInfo.DISTILBERT_BASE_UNCASED: EmbeddingInfo(
            user_friendly_name="DistilBERT pretrained model",
            embedding_name=EmbeddingInfo.DISTILBERT_BASE_UNCASED,
            download_prefix=WORD_VEC_LINK,
            file_name="{base}.zip".format(base=EmbeddingInfo.DISTILBERT_BASE_UNCASED),
            lower_case=True,
            license="Apache License Version 2.0, More information can be found at: "
                    "https://www.apache.org/licenses/",
            credits="DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter "
                    "by Victor Sanh, Lysandre Debut, Julien Chaumond, and Thomas Wolf. "
                    "Paper available at https://arxiv.org/abs/1910.01108.",
            sha256hash="b66df693711b21d2f6458b9f258925c8a8fac639654e82cbafaf55186e234676",
            language="eng",
        ),
        EmbeddingInfo.DISTILROBERTA_BASE: EmbeddingInfo(
            user_friendly_name="DistilRoBERTa pretrained model",
            embedding_name=EmbeddingInfo.DISTILROBERTA_BASE,
            download_prefix=WORD_VEC_LINK,
            file_name="{base}.zip".format(base=EmbeddingInfo.DISTILROBERTA_BASE),
            lower_case=False,
            license="Apache License Version 2.0, More information can be found at: "
                    "https://www.apache.org/licenses/",
            credits="DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter "
                    "by Victor Sanh, Lysandre Debut, Julien Chaumond, and Thomas Wolf. "
                    "Paper available at https://arxiv.org/abs/1910.01108.",
            sha256hash="7a205c1d3e61a6349fdfb15c78d75a3abd722ed3a4d44f977292a85cb20cb62d",
            language="eng",
        ),
        EmbeddingInfo.ROBERTA_BASE: EmbeddingInfo(
            user_friendly_name="RoBERTa pretrained model",
            embedding_name=EmbeddingInfo.ROBERTA_BASE,
            download_prefix=WORD_VEC_LINK,
            file_name="{base}.zip".format(base=EmbeddingInfo.ROBERTA_BASE),
            lower_case=False,
            license="MIT License.",
            credits="RoBERTa: A Robustly Optimized BERT Pretraining Approach by "
                    "Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, "
                    "Omer Levy, Mike Lewis, Luke Zettlemoyer, and Veselin Stoyanov. "
                    "Paper available at https://arxiv.org/abs/1907.11692.",
            sha256hash="e82d1cca61dfe67c7b53837610ef9c74dd8e70137b5aaa0c85dc9ee572d1f637",
            language="eng",
        ),
        EmbeddingInfo.ROBERTA_LARGE: EmbeddingInfo(
            user_friendly_name="RoBERTa pretrained model",
            embedding_name=EmbeddingInfo.ROBERTA_LARGE,
            download_prefix=WORD_VEC_LINK,
            file_name="{base}.zip".format(base=EmbeddingInfo.ROBERTA_LARGE),
            lower_case=False,
            license="MIT License.",
            credits="RoBERTa: A Robustly Optimized BERT Pretraining Approach by "
                    "Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, "
                    "Omer Levy, Mike Lewis, Luke Zettlemoyer, and Veselin Stoyanov. "
                    "Paper available at https://arxiv.org/abs/1907.11692.",
            sha256hash="d3aa28b41d482890c35a98215dff257610fa2e045f44472de3e22606ea3de720",
            language="eng",
        ),
        EmbeddingInfo.XLM_ROBERTA_BASE: EmbeddingInfo(
            user_friendly_name="Multilingual RoBERTa pretrained model",
            embedding_name=EmbeddingInfo.XLM_ROBERTA_BASE,
            download_prefix=WORD_VEC_LINK,
            file_name="{base}.zip".format(base=EmbeddingInfo.XLM_ROBERTA_BASE),
            lower_case=False,
            license="MIT License.",
            credits="Unsupervised Cross-lingual Representation Learning at Scale by "
                    "Alexis Conneau, Kartikay Khandelwal, Naman Goyal, Vishrav Chaudhary, Guillaume Wenzek, "
                    "Francisco Guzmán, Edouard Grave, Myle Ott, Luke Zettlemoyer, and Veselin Stoyanov. "
                    "Paper available at http://arxiv.org/abs/1911.02116.",
            sha256hash="059fff6fb3ff9a1933cdf39156feba0b9af8bcc325fb75067d5a7bbe5feb3bdf",
            language="mul",
        ),
        EmbeddingInfo.XLM_ROBERTA_LARGE: EmbeddingInfo(
            user_friendly_name="Multilingual RoBERTa pretrained model",
            embedding_name=EmbeddingInfo.XLM_ROBERTA_LARGE,
            download_prefix=WORD_VEC_LINK,
            file_name="{base}.zip".format(base=EmbeddingInfo.XLM_ROBERTA_LARGE),
            lower_case=False,
            license="MIT License.",
            credits="Unsupervised Cross-lingual Representation Learning at Scale by "
                    "Alexis Conneau, Kartikay Khandelwal, Naman Goyal, Vishrav Chaudhary, Guillaume Wenzek, "
                    "Francisco Guzmán, Edouard Grave, Myle Ott, Luke Zettlemoyer, and Veselin Stoyanov. "
                    "Paper available at http://arxiv.org/abs/1911.02116.",
            sha256hash="a155eba41b834146a31e068d33316127c0cd8d518e2874a8af28afb521966061",
            language="mul",
        ),
        EmbeddingInfo.BERT_BASE_CASED: EmbeddingInfo(
            user_friendly_name="BERT pretrained cased model",
            embedding_name=EmbeddingInfo.BERT_BASE_CASED,
            download_prefix=WORD_VEC_LINK,
            file_name="{base}.zip".format(base=BERT_EMB_CASED_INFO),
            lower_case=False,
            license="Apache License Version 2.0, More information can\
                        be found at: https://www.apache.org/licenses/",
            credits="Pretrained model on English language using a masked language modeling (MLM) "
            "objective. It was introduced in https://arxiv.org/abs/1810.04805 "
            "and first released in https://github.com/google-research/bert",
            sha256hash="36d61b41917e649d5fdfb4ffbb7c77e7d20edce198e21538e55ea53f127f5336",
            language="eng",
        ),
        EmbeddingInfo.BERT_BASE_UNCASED: EmbeddingInfo(
            user_friendly_name="BERT pretrained model",
            embedding_name=EmbeddingInfo.BERT_BASE_UNCASED,
            download_prefix=WORD_VEC_LINK,
            file_name="{base}-nohead.zip".format(base=BERT_EMB_INFO),
            lower_case=True,
            license="Apache License Version 2.0, More information can\
                be found at: "
            "https://www.apache.org/licenses/",
            credits="BERT: Pre-training of Deep Bidirectional Transformers\
                for Language Understanding by Devlin, Jacob and Chang, "
            "Ming-Wei and Lee, Kenton and Toutanova, Kristina,\
                arXiv preprint arXiv:1810.04805",
            sha256hash="3d9b0b72bf454b5322350a8d02fefeb19f9b8cbb460be274a5f7958b2e09f025",
            language="eng",
        ),
        EmbeddingInfo.BERT_BASE_UNCASED_AUTONLP_3_1_0: EmbeddingInfo(
            user_friendly_name="BERT pretrained model",
            embedding_name=EmbeddingInfo.BERT_BASE_UNCASED_AUTONLP_3_1_0,
            download_prefix=WORD_VEC_LINK,
            file_name="{base}.zip".format(base=BERT_EMB_AUTONLP_3_1_0),
            lower_case=True,
            license="Apache License Version 2.0, More information can be found at: "
            "https://www.apache.org/licenses/",
            credits="BERT: Pre-training of Deep Bidirectional Transformers "
                    "for Language Understanding by Devlin, Jacob and Chang, "
                    "Ming-Wei and Lee, Kenton and Toutanova, Kristina, "
                    "arXiv preprint arXiv:1810.04805",
            sha256hash="7345bc86618db60016ab0412a1c1659a1e949d2608973ed3595cf8aa8b5f6b68",
            language="eng",
        ),
        EmbeddingInfo.BERT_BASE_MULTLINGUAL_CASED: EmbeddingInfo(
            user_friendly_name="BERT multilingual pretrained model",
            embedding_name=EmbeddingInfo.BERT_BASE_MULTLINGUAL_CASED,
            download_prefix=WORD_VEC_LINK,
            file_name="{base}.zip".format(base=BERT_MULTI_EMB_INFO),
            lower_case=False,
            license="Apache License Version 2.0, More information can be found at: "
            "https://www.apache.org/licenses/",
            credits="BERT: Pre-training of Deep Bidirectional Transformers "
                    "for Language Understanding by Devlin, Jacob and Chang, "
                    "Ming-Wei and Lee, Kenton and Toutanova, Kristina, "
                    "arXiv preprint arXiv:1810.04805",
            sha256hash="fc24b30e51925d7f3a8d7ddd5c5cd8ca52d769c41f2880b7c2ebcc98a270c1f9",
            language="mul",
        ),
        EmbeddingInfo.BERT_BASE_MULTLINGUAL_CASED_AUTONLP_3_1_0: EmbeddingInfo(
            user_friendly_name="BERT multilingual pretrained model",
            embedding_name=EmbeddingInfo.BERT_BASE_MULTLINGUAL_CASED_AUTONLP_3_1_0,
            download_prefix=WORD_VEC_LINK,
            file_name="{base}.zip".format(base=BERT_MULTI_EMB_AUTONLP_3_1_0),
            lower_case=False,
            license="Apache License Version 2.0, More information can be found at: "
            "https://www.apache.org/licenses/",
            credits="BERT: Pre-training of Deep Bidirectional Transformers "
                    "for Language Understanding by Devlin, Jacob and Chang, "
                    "Ming-Wei and Lee, Kenton and Toutanova, Kristina, "
                    "arXiv preprint arXiv:1810.04805",
            sha256hash="d2c235bdf57cdd30e255978dbf2f578c6dc49bb9ba846ec94d76ce78742b688c",
            language="mul",
        ),
        EmbeddingInfo.BERT_BASE_GERMAN_CASED: EmbeddingInfo(
            user_friendly_name="BERT German pretrained model",
            embedding_name=EmbeddingInfo.BERT_BASE_GERMAN_CASED,
            download_prefix=WORD_VEC_LINK,
            file_name="{base}.zip".format(base=BERT_GERMAN_EMB_INFO),
            lower_case=False,
            license="Apache License Version 2.0, More information can be found at: "
            "https://www.apache.org/licenses/",
            credits="BERT: Pre-training of Deep Bidirectional Transformers "
                    "for Language Understanding by Devlin, Jacob and Chang, "
                    "Ming-Wei and Lee, Kenton and Toutanova, Kristina, "
                    "arXiv preprint arXiv:1810.04805",
            sha256hash="d18ebfa93206af62a3dc855afff0f7503e78f913dced37e5143d90cff1e28e03",
            language="deu",
        ),
        EmbeddingInfo.BERT_BASE_GERMAN_CASED_AUTONLP_3_1_0: EmbeddingInfo(
            user_friendly_name="BERT German pretrained model",
            embedding_name=EmbeddingInfo.BERT_BASE_GERMAN_CASED_AUTONLP_3_1_0,
            download_prefix=WORD_VEC_LINK,
            file_name="{base}.zip".format(base=BERT_GERMAN_EMB_AUTO_NLP_3_1_0),
            lower_case=False,
            license="Apache License Version 2.0, More information can be found at: "
            "https://www.apache.org/licenses/",
            credits="BERT: Pre-training of Deep Bidirectional Transformers "
                    "for Language Understanding by Devlin, Jacob and Chang, "
                    "Ming-Wei and Lee, Kenton and Toutanova, Kristina, "
                    "arXiv preprint arXiv:1810.04805",
            sha256hash="4947efa756568096aea4b467340947005b9e6dca82dc65b455c429cc8e4276b7",
            language="deu",
        ),
        EmbeddingInfo.BERT_BASE_CHINESE: EmbeddingInfo(
            user_friendly_name="BERT Chinese pretrained model",
            embedding_name=EmbeddingInfo.BERT_BASE_CHINESE,
            download_prefix=WORD_VEC_LINK,
            file_name="{base}.zip".format(base=BERT_CHINESE_EMB_INFO),
            lower_case=False,
            license="Apache License Version 2.0, More information can be found at: "
            "https://www.apache.org/licenses/",
            credits="BERT: Pre-training of Deep Bidirectional Transformers "
                    "for Language Understanding by Devlin, Jacob and Chang, "
                    "Ming-Wei and Lee, Kenton and Toutanova, Kristina, "
                    "arXiv preprint arXiv:1810.04805",
            sha256hash="b654167257eeb5c66d6881709f880b911f4076d6c0d47ef5d19ec217ecc7b604",
            language="zho",
        ),
        EmbeddingInfo.BERT_BASE_CHINESE_AUTONLP_3_1_0: EmbeddingInfo(
            user_friendly_name="BERT Chinese pretrained model",
            embedding_name=EmbeddingInfo.BERT_BASE_CHINESE_AUTONLP_3_1_0,
            download_prefix=WORD_VEC_LINK,
            file_name="{base}.zip".format(base=BERT_CHINESE_EMB_AUTONLP_3_1_0),
            lower_case=False,
            license="Apache License Version 2.0, More information can be found at: "
            "https://www.apache.org/licenses/",
            credits="BERT: Pre-training of Deep Bidirectional Transformers "
                    "for Language Understanding by Devlin, Jacob and Chang, "
                    "Ming-Wei and Lee, Kenton and Toutanova, Kristina, "
                    "arXiv preprint arXiv:1810.04805",
            sha256hash="e269738101f75fc8eb97876fe61157adc624df532b1bfe3b1e6e37a9393ab8c0",
            language="zho",
        ),
        EmbeddingInfo.XLNET_BASE_CASED: EmbeddingInfo(
            user_friendly_name="XLNET pretrained model",
            embedding_name=EmbeddingInfo.XLNET_BASE_CASED,
            download_prefix=WORD_VEC_LINK,
            file_name="{base}.zip".format(base=XLNET_EMB_INFO),
            lower_case=False,
            license="MIT License.",
            credits="XLNet: Generalized Autoregressive Pretraining for "
                    "Language Understanding by Zhilin Yang*, Zihang Dai*, "
                    "Yiming Yang, Jaime Carbonell, Ruslan Salakhutdinov, and Quoc V. Le."
                    "Paper available at https://arxiv.org/abs/1906.08237.",
            sha256hash="e0193355fdf32e6cc78dd7459b6c9f13",
            language="eng",
        ),
        EmbeddingInfo.XLNET_LARGE_CASED: EmbeddingInfo(
            user_friendly_name="XLNET pretrained model",
            embedding_name=EmbeddingInfo.XLNET_LARGE_CASED,
            download_prefix=WORD_VEC_LINK,
            file_name="{base}.zip".format(base=EmbeddingInfo.XLNET_LARGE_CASED),
            lower_case=False,
            license="MIT License.",
            credits="XLNet: Generalized Autoregressive Pretraining for "
                    "Language Understanding by Zhilin Yang*, Zihang Dai*, "
                    "Yiming Yang, Jaime Carbonell, Ruslan Salakhutdinov, and Quoc V. Le."
                    "Paper available at https://arxiv.org/abs/1906.08237.",
            sha256hash="be5700beb6a455379e2ff18e41746238279149902369094f1e6e8ee305ec206f",
            language="eng",
        ),
        EmbeddingInfo.GLOVE_WIKIPEDIA_GIGAWORD_6B_300: EmbeddingInfo(
            user_friendly_name="Glove word embeddings trained on wikipedia and gigawords",
            embedding_name=EmbeddingInfo.GLOVE_WIKIPEDIA_GIGAWORD_6B_300,
            download_prefix=WORD_VEC_LINK,
            file_name="{base}.pkl".format(base=EmbeddingInfo.GLOVE_WIKIPEDIA_GIGAWORD_6B_300),
            lower_case=False,
            license="ODC Public Domain Dedication and Licence (PDDL). More information can be found at: "
            "https://www.opendatacommons.org/licenses/pddl/1.0/",
            credits="GloVe: Global Vectors for Word Representation, "
            "Empirical Methods in Natural Language Processing (EMNLP) 2014 "
            "Jeffrey Pennington and Richard Socher and Christopher D. Manning "
            "https://www.aclweb.org/anthology/D14-1162",
            sha256hash="2e0ee1cf738a34ec7fed2f24872324eddff4dce39024c815a92a39dedf7a213f",
            language="eng",
        ),
    }  # type: Dict[str, EmbeddingInfo]

    @classmethod
    def get(cls, embeddings_name: str) -> Optional[EmbeddingInfo]:
        """
        Get embedding information given the name.

        :param embeddings_name: Name of the requested embeddings.
        :return: Information on the embeddings.
        """
        return cls.embeddings[embeddings_name] if embeddings_name in cls.embeddings else None

    @classmethod
    def get_bert_model_name_based_on_language(cls, dataset_language: str = "eng") -> str:
        """
        Get embedding information given.

        :param dataset_language: Language of the input text for text classification.
        :return: Transfomer model name, e.g. bert-base-uncased, corresponding to that language
        """
        # get list of languages that bert models cover
        bert_languages = [cls.embeddings[name]._language for name in cls.pretrained_model_names_for_languages]
        if dataset_language not in bert_languages:
            # If the language is not explicitly in the map, then use multilingual bert
            dataset_language = "mul"
        model_name = next(
            name
            for name in cls.pretrained_model_names_for_languages
            if cls.embeddings[name]._language == dataset_language
        )
        return model_name
