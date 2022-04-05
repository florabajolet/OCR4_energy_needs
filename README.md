# OCR4_energy_needs

*Keywords:* Regression, modèles ensemblistes, évaluation

## But du projet

Ce projet a pour but de prédire la consommation électrique et les émissions de gaz à effet de serre de bâtiments non résidentiels à partir des données de la ville de Seattle (années 2015-2016). Le modèle doit permettre de faire des prédictions à partir des donénes disponibles avant construction. Une attention particulière doit donc être portée sur le risque de fuite de données.

Un autre objectif est d'évaluer l'utilité de l'Energy Star Score dans la prédiction (un peu l'équivalent des classes énergie en France).

## Librairies et données nécessaire

Les données sont téléchargeables sur Kaggle : https://www.kaggle.com/datasets/city-of-seattle/sea-building-energy-benchmarking

Librairies utilisées :
* Python 3.8.8
* Matplotlib 3.4.2
* Pandas 1.2.4
* Nympy 1.20.1
* Seaborn 0.11.1
* Scikit-learn 1.0.2

## Fichiers
* *P4_EDA.ipynb* : Analyse exploratoire
* *P4_modeling* : Modélisation, réglage des hyperparamètres, cross-validation
* *P4_functions* : Fonctions de base pour l'exploration

## Approches
* Base line, régression linéaire (Ridge, Lasso, ElasticNet)
* Random Forest
* Gradient boosting