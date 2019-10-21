# IA-event-handler Python

Ce composant écrit en Python, permettra de récupérer via un URL un article, de détécter sa langue, de le traiter pour enfin le classifier selon des tags prédéfinis.

Pour détécter la langue de l'article nous utiliserons le modèle fasttext __lid.176.ftz__ présents ici https://fasttext.cc/docs/en/language-identification.html.

Ce modèle provient des publications suivantes :

- __joulin2016bag, Bag of Tricks for Efficient Text Classification, Joulin, Armand and Grave, Edouard and Bojanowski, Piotr and Mikolov, Tomas, arXiv preprint arXiv:1607.01759, 2016__

- __joulin2016fasttext,FastText.zip: Compressing text classification models, Joulin, Armand and Grave, Edouard and Bojanowski, Piotr and Douze, Matthijs and Jegou, Herve and Mikolov, Tomas, arXiv preprint arXiv:1612.03651, 2016__
