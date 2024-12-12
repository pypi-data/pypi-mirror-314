# Libraire python Lexfluent RevolutionAI
*Auteur Jacques MASSA*
*Créé le 2 décembre 2024*

---

## Présentation
Cette librairie permet:
- la classification de documents selon le modèle jupiterB0 
- l'extraction de données contenu dans des documents de classes connues(Offre de prêts, IBAN, CNI, etc ...).


## Installations Prérequises 

``` 

    pip install setuptools wheel 
    pip install pdfplumber 
    pip install spacy[cuda12x]
    pip install tqdm 
    pip install opencv-python
    pip install pytesseract
    pip install pdf2image
    pip install pillow==10.0.1
    pip install pandas
    pip install scikit-learn
    pip install matplotlib
    pip install tensorflow==2.17.0
    pip install tf-keras==2.17.0
    pip install tensorflow_hub
    pip install tensorrt
    pip install langchain-community
    pip install ocrmypdf

```
 
## Téléchargement modèles 
### SPACY 

``` python -m spacy download fr_core_news_lg ```

## Update et installations requises
``` 
    apt-get update 
    apt-get upgrade
    apt install software-properties-common -y
    apt-get install poppler-utils -y
    add-apt-repository ppa:alex-p/tesseract-ocr5
    apt-get install libc6 -y
    apt-get install poppler-utils -y
    apt-get install tesseract-ocr -y
    apt-get install tesseract-ocr-fra -y
    apt-get install tesseract-ocr-eng -y
    apt-get install tesseract-ocr-ita -y
    apt-get install tesseract-ocr-spa -y
    apt-get install tesseract-ocr-deu -y
    apt-get install tesseract-ocr-cos -y
    apt-get install tesseract-ocr-lat -y
    apt-get install automake libtool -y
    apt-get install libleptonica-dev -y
    apt-get install ffmpeg libsm6 libxext6  -y
    apt-get install ocrmypdf -y    

``` 

## GPU issue 
Si problème : Successful NUMA node read from SysFS had negative value (-1) 

```
for a in /sys/bus/pci/devices/*; do echo 0 |  tee -a $a/numa_node; done

```