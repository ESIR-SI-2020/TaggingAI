# IA-event-handler Python

This component written in Python, will retrieve an article via an URL, detect its language, process it to finally classify it according to predefined tags.

To detect the language of the article we will use the fasttext model __lid.176.ftz__ present here https://fasttext.cc/docs/en/language-identification.html.

This model comes from the following publications:

- __joulin2016bag, Bag of Tricks for Efficient Text Classification, Joulin, Armand and Grave, Edouard and Bojanowski, Piotr and Mikolov, Tomas, arXiv preprint arXiv:1607.01759, 2016__

- __joulin2016fasttext,FastText.zip: Compressing text classification models, Joulin, Armand and Grave, Edouard and Bojanowski, Piotr and Douze, Matthijs and Jegou, Herve and Mikolov, Tomas, arXiv preprint arXiv:1612.03651, 2016__
