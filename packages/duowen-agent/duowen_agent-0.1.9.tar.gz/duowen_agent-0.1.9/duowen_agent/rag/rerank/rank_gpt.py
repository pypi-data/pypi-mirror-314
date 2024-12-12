from typing import List

from duowen_agent.llm.chat_model import OpenAIChat
from duowen_agent.llm.tokenizer import tokenizer


class Ranker:
    """通过语言模型实现 rerank能力 不支持分值，只能排序"""

    # query: str, documents
    def __init__(self, llm: OpenAIChat, query: str, documents: List[str], rank_limit=5):
        self.llm = llm
        self.query = query
        self.rank_limit = rank_limit
        self.prompt_tokens = 1000
        self.question_tokens = tokenizer.chat_len(query)
        self.documents = documents
        self.content_tokens_limit = self.llm.token_limit - self.prompt_tokens - self.question_tokens

    def cut_passages(self):
        _content_tokens = self.content_tokens_limit
        _passages = []
        for _chunk in self.documents:
            _curr_token = tokenizer.chat_len(_chunk)
            _content_tokens = _content_tokens - _curr_token
            if _content_tokens > 0:
                _passages.append(_chunk)
            else:
                break
        self.documents = _passages

    def chk_passages_tokens_limit(self):
        if tokenizer.chat_len(''.join(self.documents)) > self.content_tokens_limit:
            return False
        else:
            return True

    def get_prefix_prompt(self, num):
        return [{'role': 'system',
                 'content': "You are RankGPT, an intelligent assistant that can rank passages based on their relevancy to the query."},
                {'role': 'user',
                 'content': f"I will provide you with {num} passages, each indicated by number identifier []. \nRank the passages based on their relevance to query: {self.query}."},
                {'role': 'assistant', 'content': 'Okay, please provide the passages.'}]

    def get_post_prompt(self, num):
        return f"Search Query: {self.query}. \nRank the {num} passages above based on their relevance to the search query. The passages should be listed in descending order using identifiers. The most relevant passages should be listed first. The output format should be [] > [], e.g., [1] > [2]. Only response the ranking results, do not say any word or explain."

    def create_permutation_instruction(self):
        if not self.chk_passages_tokens_limit():
            raise ValueError(
                f"Agent Ranker token passages overly long, model tokens limit number {self.llm.token_limit}.")
        num = len(self.documents)
        messages = self.get_prefix_prompt(num)
        rank = 0
        for hit in self.documents:
            rank += 1
            content = hit
            content = content.replace('Title: Content: ', '')
            content = content.strip()
            messages.append({'role': 'user', 'content': f"[{rank}] {content}"})
            messages.append({'role': 'assistant', 'content': f'Received passage [{rank}].'})
        messages.append({'role': 'user', 'content': self.get_post_prompt(num)})
        return messages

    def run_llm(self, messages):
        response = self.llm.chat(messages=messages, temperature=0)
        return response

    @staticmethod
    def clean_response(response: str):
        new_response = ''
        for c in response:
            if not c.isdigit():
                new_response += ' '
            else:
                new_response += c
        new_response = new_response.strip()
        return new_response

    @staticmethod
    def remove_duplicate(response):
        new_response = []
        for c in response:
            if c not in new_response:
                new_response.append(c)
        return new_response

    def receive_permutation(self, permutation):
        _passages = []
        response = self.clean_response(permutation)
        response = [int(x) - 1 for x in response.split()]
        response = self.remove_duplicate(response)
        original_rank = [tt for tt in range(len(self.documents))]
        response = [ss for ss in response if ss in original_rank]
        response = response + [tt for tt in original_rank if tt not in response]
        for x in response[:self.rank_limit]:
            _passages.append(self.documents[x])
        return _passages

    def run(self):
        if self.rank_limit < len(self.documents):
            messages = self.create_permutation_instruction()
            permutation = self.run_llm(messages)
            item = self.receive_permutation(permutation)
            return item
        else:
            return self.documents

# if __name__ == '__main__':
#     from config import DEFAULT_MODEL_CONFIG
#     from core.llm.chat_model import OpenAIChat
#
#     # logging.basicConfig(level=logging.DEBUG)
#
#     llm = OpenAIChat(**DEFAULT_MODEL_CONFIG)
#
#     rk = Ranker(llm=llm, question='How much impact do masks have on preventing the spread of the COVID-19?', passages=[
#         'Title: Universal Masking is Urgent in the COVID-19 Pandemic: SEIR and Agent Based Models, Empirical Validation, Policy Recommendations Content: We present two models for the COVID-19 pandemic predicting the impact of universal face mask wearing upon the spread of the SARS-CoV-2 virus--one employing a stochastic dynamic network based compartmental SEIR (susceptible-exposed-infectious-recovered) approach, and the other employing individual ABM (agent-based modelling) Monte Carlo simulation--indicating (1) significant impact under (near) universal masking when at least 80% of a population is wearing masks, versus minimal impact when only 50% or less of the population is wearing masks, and (2) significant impact when universal masking is adopted early, by Day 50 of a regional outbreak, versus minimal impact when universal masking is adopted late. These effects hold even at the lower filtering rates of homemade masks. To validate these theoretical models, we compare their predictions against a new empirical data set we have collected',
#         'Title: Masking the general population might attenuate COVID-19 outbreaks Content: The effect of masking the general population on a COVID-19 epidemic is estimated by computer simulation using two separate state-of-the-art web-based softwares, one of them calibrated for the SARS-CoV-2 virus. The questions addressed are these: 1. Can mask use by the general population limit the spread of SARS-CoV-2 in a country? 2. What types of masks exist, and how elaborate must a mask be to be effective against COVID-19? 3. Does the mask have to be applied early in an epidemic? 4. A brief general discussion of masks and some possible future research questions regarding masks and SARS-CoV-2. Results are as follows: (1) The results indicate that any type of mask, even simple home-made ones, may be effective. Masks use seems to have an effect in lowering new patients even the protective effect of each mask (here dubbed"one-mask protection") is',
#         'Title: To mask or not to mask: Modeling the potential for face mask use by the general public to curtail the COVID-19 pandemic Content: Face mask use by the general public for limiting the spread of the COVID-19 pandemic is controversial, though increasingly recommended, and the potential of this intervention is not well understood. We develop a compartmental model for assessing the community-wide impact of mask use by the general, asymptomatic public, a portion of which may be asymptomatically infectious. Model simulations, using data relevant to COVID-19 dynamics in the US states of New York and Washington, suggest that broad adoption of even relatively ineffective face masks may meaningfully reduce community transmission of COVID-19 and decrease peak hospitalizations and deaths. Moreover, mask use decreases the effective transmission rate in nearly linear proportion to the product of mask effectiveness (as a fraction of potentially infectious contacts blocked) and coverage rate (as'])
#
#     for i in rk.run():
#         print(i)
