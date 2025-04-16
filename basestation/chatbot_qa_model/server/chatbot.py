import os
from transformers import pipeline, AutoTokenizer, AutoModelForQuestionAnswering
import torch
import time


model_name = "bert-large-uncased-whole-word-masking-finetuned-squad"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)

nlp = pipeline("question-answering", model=model_name)

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# default_context = "Hello, I am minibot. My creators are from Cornell but I \
# legally can't say that because they signed a waiver. Oh well, let's just say \
# I was created at Harvard. I have two wheels that are connected to motors with \
# two caster wheels. Tasks I can do are following lines and detecting objects. \
# I can be programmed to move using Blockly or Python - or both! You can share more about \
# yourself (including your search history) using the textbox in the chatbot feature. \
# Make sure to SMASH the like button and hit \
# subscribe and turn on the notification bell.  \
# See you guys in the next episode. Join my Twitch, Patreon, and Instagram."

default_context = "Ice cream(derived from earlier iced cream or cream ice) is a sweetened frozen food \
typically eaten as a snack or dessert. It may be made from dairy milk or cream and is flavoured with a sweetener, \
either sugar or an alternative, and any spice, such as cocoa or vanilla. It can also be made by whisking a flavored \
cream base and liquid nitrogen together. Colorings are usually added, in addition to stabilizers. The mixture is \
stirred to incorporate air spaces and cooled below the freezing point of water to prevent detectable ice crystals \
It becomes more malleable as its temperature increases. The sky is blue."

# default_context = "Water is an inorganic, transparent, tasteless, odorless, and nearly colorless chemical substance, which is the main constituent of Earth's hydrosphere and the fluids of all known living organisms (in which it acts as a solvent). It is vital for all known forms of life, even though it provides no calories or organic nutrients. Its chemical formula is H2O, meaning that each of its molecules contains one oxygen and two hydrogen atoms, connected by covalent bonds. Two hydrogen atoms are attached to one oxygen atom at an angle of 104.45°."

# default_context = "Ice is water frozen into a solid state.[3][4] Depending on the presence of impurities such as particles of soil or bubbles of air, it can appear transparent or a more or less opaque bluish-white color. In the Solar System, ice is abundant and occurs naturally from as close to the Sun as Mercury to as far away as the Oort cloud objects. Beyond the Solar System, it occurs as interstellar ice. It is abundant on Earth's surface – particularly in the polar regions and above the snow line[5] – and, as a common form of precipitation and deposition, plays a key role in Earth's water cycle and climate. It falls as snowflakes and hail or occurs as frost, icicles or ice spikes and aggregates from snow as glaciers and ice sheets."


class Chatbot:

    def compute_answer(self, input_question, context=default_context):

        answer_dict = nlp(question=input_question,
                          context=context)

        if answer_dict['score'] < .05:
            return "I don't have an answer to your question."

        return answer_dict['answer']

    def test(self):
        print("hello world")
