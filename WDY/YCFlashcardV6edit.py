import os
import openai
import re

openai.api_key = "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"
model_id = 'gpt-3.5-turbo'

def ChatGPT_conversation(conversation):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation
    )
    # api_usage = response['usage']
    # print('Total token consumed: {0}'.format(api_usage['total_tokens']))
    # stop means complete
    # print(response['choices'][0].finish_reason)
    # print(response['choices'][0].index)
    conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    return conversation

keywordct = '10'
conversation = []
conversation.append({'role': 'system', 'content': f'You are a flashcard generator. You have two tasks, firstly you have to take in a source text and generate keywords. Only show the most important few key words, no more than {keywordct}. Keywords are usually words that the text usually proceeds to explain, and are words that would be important to a student. The second task is to generate flashcard answers based on the extracted keywords and content verbatim from the source text, ie. without using any information outside of the source text given.'})
conversation.append({"role": "user", "content": "Extract keywords from this text:\n\nCNN is a type of deep learning model for processing data that has a grid pattern, such as images, which is inspired by the organization of animal visual cortex [13, 14] and designed to automatically and adaptively learn spatial hierarchies of features, from low- to high-level patterns. CNN is a mathematical construct that is typically composed of three types of layers (or building blocks): convolution, pooling, and fully connected layers. The first two, convolution and pooling layers, perform feature extraction, whereas the third, a fully connected layer, maps the extracted features into final output, such as classification. A convolution layer plays a key role in CNN, which is composed of a stack of mathematical operations, such as convolution, a specialized type of linear operation. In digital images, pixel values are stored in a two-dimensional (2D) grid, i.e., an array of numbers (Fig. 2), and a small grid of parameters called kernel, an optimizable feature extractor, is applied at each image position, which makes CNNs highly efficient for image processing, since a feature may occur anywhere in the image. As one layer feeds its output into the next layer, extracted features can hierarchically and progressively become more complex. The process of optimizing parameters such as kernels is called training, which is performed so as to minimize the difference between outputs and ground truth labels through an optimization algorithm called backpropagation and gradient descent, among others."})
conversation = ChatGPT_conversation(conversation)
print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip()))

keyword = conversation[-1]['content'].strip()
keywords = re.findall(r'\b[A-Za-z]+\b', keyword)
keywords = re.findall(r'\d+\. ([A-Za-z ]+)', keyword)
print(keywords)
keywords_string = ', '.join(keywords)

flashcards = []

for keyword in keywords:
    prompt = f"Thank you. Now let us generate the next flashcard. Based on only the source text given, DO NOT USE OUTSIDE INFORMATION AND ONLY USE INFORMATION VERBATIM FROM THE SOURCE, generate a back side of a flashcard for {keyword}, with the corresponding front being 'What is {keyword}?'. Keep it short and simple and in point form and only text content, no need full sentences, preferably three lines at most"
    #print(prompt)
    conversation.append({'role': 'user', 'content': prompt})
    conversation = ChatGPT_conversation(conversation)
    print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip()))

    meaning = conversation[-1]['content'].strip()
    flashcard = {
        "question": f"What is {keyword}?",
        "answer": meaning
    }
    flashcards.append(flashcard)

# Print the flashcards
for flashcard in flashcards:
    print("Question:", flashcard["question"])
    print("Answer:", flashcard["answer"])
    print("---")