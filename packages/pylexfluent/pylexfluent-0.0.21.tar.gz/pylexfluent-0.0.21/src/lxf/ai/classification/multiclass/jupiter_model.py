
import datetime
import time
from typing import List, Tuple

import logging
import lxf.ai.classification.multiclass.common as cm
from pathlib import Path
import numpy as np
import pandas as pd

############################################################
# Bug: TF Hub is not compatible with Keras 3 and TensorFlow 2.16+ #903
# https://github.com/tensorflow/hub/issues/903
# Can you try upgrading to the latest tensorflow_hub version 0.16.1 and installing tf-keras as a peer dependency?
#
#Some extra context:
#
#TensorFlow v2.16 points tf.keras to Keras 3, which unfortunately breaks a number of workflows with tensorflow_hub. We're working to make tensorflow_hub compatible with Keras 3 but in the meantime the recommendation is to use Keras 2 via tf-keras.

import os

from lxf.domain.keyswordsandphrases import KeysWordsPhrases
from lxf.domain.predictions import Prediction, Predictions
os.environ['TF_USE_LEGACY_KERAS']='1'
###########################################################
import tensorflow as tf
# Cf BUG ci-dessus 
import tensorflow_hub as hub
import pickle

##########################################################
# Pour utiliser Keras 2.x
import tf_keras as keras
#########################################################

#from  repositories.training_data_repository import TrainingDataRepository
from lxf.services.measure_time import measure_time
global embed
embed = None 
def get_embed() :
    global embed
    if embed == None :
        embedding_model= "universal-sentence-encoder-large/5"
        print(f"Chargement de l'embedding {embedding_model} ...")
        embed= hub.load(f"https://tfhub.dev/google/{embedding_model}")
        print("Chargement terminé")
    return embed

SETLEVEL = logging.ERROR
logger = logging.getLogger('MulticlassClassificationJupiterModel')
fh = logging.FileHandler('./logs/MulticlassClassificationJupiterModel.log')
fh.setLevel(SETLEVEL)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(SETLEVEL)
logger.addHandler(fh)

def get_mirrored_strategy():
    gpus = tf.config.list_logical_devices('GPU')
    if gpus:
        for gpu in gpus:
            logger.info(f"Gpu name: {gpu.name}")
        mirrored_strategy=tf.distribute.MirroredStrategy(gpus)
    else:
        logger.info("No GPU found")
        mirrored_strategy=tf.distribute.MirroredStrategy()
    return mirrored_strategy 
                

class MulticlassClassificationJupiterModel:

    def get_model_dir(self,name):
        models_dir_root = Path('models')
        if not models_dir_root.exists():
            models_dir_root.mkdir()
        model_dir = Path(f"{models_dir_root}/classification")
        if not model_dir.exists():
            model_dir.mkdir() 
        model_dir = Path(f"{model_dir}/multiclass")
        if not model_dir.exists():
            model_dir.mkdir()           
        model_dir = Path(f"{model_dir}/{name}")
        if not model_dir.exists():
            model_dir.mkdir()
        return model_dir.as_posix()

    # @measure_time
    # def train(self,td:TrainingDataRepository,ModelName:str="jupiter"):

    #     """
    #     From file name, let's extract the data and prepare the feature and label
    #     Create the model and fit it, then evaluate it
    #     return the history and the evaluation result
    #     arguments :
    #         train_id : int => unique number
    #         filename : Pathlib => fullfilename of the data
    #         name : str => name of model
    #     """
    #     mirrored_strategy = get_mirrored_strategy()
    #     # prepare datasets
    #     filter={"model": ModelName} 
    #     #data = pd.DataFrame(td.get_byfilter(filter))
    #     #temp = list(td.get_all())
    #     #logger.debug(f"All data: {temp}")
    #     data = pd.DataFrame(list(td.get_all()))
    #     logger.debug(data.head(10))
    #     samples=data.drop(columns=['_id','sid','parent_id','name','model','key_phrases','created_date'])
    #     samples = samples.sample(len(samples),random_state=cm.random_seed_base)
    #     # Thredshold computation : 80 % for training 10% for testing and 10% for validating
    #     split_threshold = round(len(samples)*.8)
    #     train_threshold = round(len(samples)*.1)
    #     valid_threshold = split_threshold+round(len(samples)*.1)

    #     #label y
    #     y=samples['famille']+'_'+samples['category']+'_'+samples['sub_category']
    #     y_labels, class_names = pd.factorize(y)
    #     logger.debug(f"Class names = {class_names}")

    #     # get y for training, testing and validating
    #     y_train,y_test, y_valid = y_labels[:split_threshold], y_labels[split_threshold:][:train_threshold],y_labels[valid_threshold:]
        
    #     # Feature x 
    #     X =[]
    #     #embed = get_embed()
    #     for row in samples['key_words']:
    #         embeddings_kw = embed([kw['word'] for kw in row])
    #         freq_kw = np.array([kw['freq'] for kw in row],dtype=np.float32 )
    #         frequencies = np.reshape(freq_kw,[freq_kw.shape[0],1])
    #         #logger.debug(embeddings_kw.shape,embeddings_kw_swapped.shape,frequencies.shape)
    #         result = frequencies*embeddings_kw
    #         #logger.debug(result.shape)
    #         lg=embeddings_kw.shape[0]
    #         paddings = tf.constant([[0, 200-lg,], [0, 0]])
    #         result_padded = tf.pad(result, paddings, "CONSTANT")
    #         #logger.debug(result_padded.shape)
    #         X.append(result_padded)
    #     X_raw=tf.convert_to_tensor(X,dtype=np.float32)
    #     x_train, x_test,x_valid = X_raw[:split_threshold], X_raw[split_threshold:][:train_threshold],X_raw[valid_threshold:]

    #     name = ModelName+"B0"
    #     with mirrored_strategy.scope(): 
    #         # Create a custom standardization function to lower.
    #         def custom_standardization(input_data):
    #             return tf.strings.lower(input_data)
    #         #define tensorboard callback
    #         tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir="logs")
    #         # Create a learning rate scheduler callback
    #         lr_scheduler = tf.keras.callbacks.LearningRateScheduler(lambda epoch: cm.lr_base * 10**(epoch/cm.epochs))
    #         #set seed 
    #         tf.random.set_seed(cm.random_seed_base)
    #         #create the model
    #         model_1=tf.keras.Sequential(name=name,layers=[
    #             tf.keras.GlobalAveragePooling1D(),
    #             tf.keras.Dense(cm.sequence_length,activation='relu'),
    #             tf.keras.Dense(len(class_names),activation='softmax')
    #         ])
    #         #compile the model 
    #         model_1.compile(loss=keras.losses.SparseCategoricalCrossentropy(),
    #                 optimizer=keras.optimizers.Adam(),
    #                 metrics=["accuracy"])
    #         # Wrap data in Dataset objects.
    #         train_data = tf.data.Dataset.from_tensor_slices((x_train, y_train))
    #         val_data = tf.data.Dataset.from_tensor_slices((x_valid, y_valid))
    #         test_data = tf.data.Dataset.from_tensor_slices((x_test,y_test))
    #         # The batch size must now be set on the Dataset objects.
    #         batch_size = 32
    #         train_data = train_data.batch(batch_size)
    #         val_data = val_data.batch(batch_size)
    #         test_data = test_data.batch(batch_size)
    #         # Disable AutoShard.
    #         options = tf.data.Options()
    #         options.experimental_distribute.auto_shard_policy = tf.data.experimental.AutoShardPolicy.OFF
    #         train_data = train_data.with_options(options)
    #         val_data = val_data.with_options(options)     
    #         test_data= test_data.with_options(options)

    #         #fit the model
    #         history_1 = model_1.fit(train_data,epochs=cm.epochs, validation_data=val_data,callbacks=[tensorboard_callback,lr_scheduler],verbose=0) 
    #         logger.debug((f"Summary:\n{model_1.summary()}"))
    #         # evaluate the model
    #         result = model_1.evaluate(test_data)
    #         logger.debug((f"Result evaluation :\n{result}"))

    #         #saving classes and model
    #         model_dir=self.get_model_dir( name=name)
    #         # Open a file and use dump()
    #         with open(f"{model_dir}/lf_categories_classnames_{name}.pkl", 'wb') as file:      
    #         # A new file will be created
    #             pickle.dump(class_names, file)    
    #         #save_options = tf.saved_model.SaveOptions(experimental_io_device='/job:localhost')    
    #         # model_1.save(f"{model_dir}/lf_categories_{name}", options=save_options)
    #         model_1.save(f"{model_dir}/lf_categories_{name}")
    #         return result
    
    async def inference(self,data:KeysWordsPhrases,model_name="jupiter")->Predictions:



        ModelName = model_name+"B0"
        model_dir = Path(self.get_model_dir(name=ModelName))
        if not model_dir.exists():
            return    
        # mirrored_strategy = get_mirrored_strategy()
        # with mirrored_strategy.scope():
        try:
            # Create a custom standardization function to lower.

            def custom_standardization(input_data):
                return tf.strings.lower(input_data)
            load_options = tf.saved_model.LoadOptions(experimental_io_device='/job:localhost')     
            #load the saved model
            model_saved_name = f"{model_dir.as_posix()}/lf_categories_{ModelName}"
            model = tf.keras.models.load_model(model_saved_name,custom_objects={"custom_standardization": custom_standardization},options=load_options)

            #logger.debug(f"Summary:\n{model.summary()}")
            # Prepare data
            X=[]            
            embed=get_embed()
            embeddings_kw = embed([row.word for row in data.keysWords])
            freq_kw = np.array([row.freq for row in data.keysWords ],dtype=np.float32 )
            frequencies = np.reshape(freq_kw,[freq_kw.shape[0],1])
            # logger.debug(embeddings_kw.shape,embeddings_kw_swapped.shape,frequencies.shape)
            result = frequencies*embeddings_kw
            # logger.debug(result.shape)
            lg=embeddings_kw.shape[0]
            paddings = tf.constant([[0, 200-lg,], [0, 0]])
            result_padded = tf.pad(result, paddings, "CONSTANT")
            #logger.debug(result_padded.shape)
            X.append(result_padded)
            X=tf.convert_to_tensor(X,dtype=np.float32)
            # Wrap data in Dataset objects.
            data = tf.data.Dataset.from_tensor_slices(X)

            # The batch size must now be set on the Dataset objects.
            batch_size = 32
            data = data.batch(batch_size)

            # Disable AutoShard.
            options = tf.data.Options()
            options.experimental_distribute.auto_shard_policy = tf.data.experimental.AutoShardPolicy.OFF
            data = data.with_options(options)

            # load the saved classes(categories)
            # Open the file in binary mode
            with open(f"{model_dir.as_posix()}/lf_categories_classnames_{ModelName}.pkl", 'rb') as file:      
                # Call load method to deserialze
                class_names = pickle.load(file)

            logger.debug(f"Class names: {class_names}")

            y_predictions=model.predict(data)

            predictions:List[Prediction]=[]
            for i,pred in enumerate(y_predictions[0]):
                accuracy = pred*100
                p:Prediction= Prediction(Name=class_names[i], Confidence=accuracy)
                predictions.append(p)
                logger.info(f"prediction = {class_names[i]} with an accuracy of {accuracy:.2f}%")

            y_pred = np.argmax(y_predictions, axis=-1)
            accuracy = y_predictions[0][y_pred[0]]*100
            logger.info(f"Best prediction  = {class_names[y_pred[0]]} with an accuracy of {accuracy:.2f} %")
            pred:Predictions = Predictions()
            pred.ModelName=ModelName
            pred.BestPrediction = class_names[y_pred[0]]
            pred.BestPredictionConfidence = accuracy
            pred.Results = predictions
            pred.PredictedAt = datetime.datetime.today().strftime("%d/%m/%Y %H:%M")                
            return pred
        except Exception as ex :
            logger.error(f"Exception pendant l'inférence : {ex}")


    async def inference_from_csv_file(self,train_id:int,filename:str,name="base"):
        """
        Make a prediction against a saved model for several data provide in filename
        Arguments :
            train_id: th id model
            filename: the csv file containing the data for predicting (Libelle ;MotsCles )
            name: name of model
        return :
            an array containing the predictions
        """
        data_filename = filename
        logger.info(f"Start Inference from {filename}")
        data = pd.read_csv(data_filename,sep=';')
        X_text = data.drop(columns=['MotsCles','Libelle'])
        # transform X_Text to numpy array and call adapt to build the vocabulary.
        if cm.concatenate_col ==False :
            X_text_array = X_text[['PhrasesCles']].to_numpy()
        else :
            X_text_array= X_text[[cm.X_col_key_phrases]].to_numpy() +' '+ X_text[[cm.X_col_key_words]].to_numpy()
            X_text_array = tf.squeeze(X_text_array)
        return  self.__inference_core__(labels=data['Libelle'],X=X_text_array,model_name=name,train_id=train_id)


    async def inference_from_string(self,train_id:int,prediction_name,X_string,name="base"):
        """
        Make a prediction against a saved model for several data provide from a X string 
        Arguments :
            train_id: the id model
            prediction_name: The name of the prediction
            X_string : the raw text for the prediction
            name: name of model
        return :
            an array containing the predictions
        """
        X_text_array=np.array([[X_string]],dtype=object)
        data_name=np.array([prediction_name],dtype=object)
        return  self.__inference_core__(labels=data_name,X=X_text_array,model_name=name,train_id=train_id)