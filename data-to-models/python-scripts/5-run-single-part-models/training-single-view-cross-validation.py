# %% [markdown]
# # Classification of doors

# %% [markdown]
# ## Adding libraries

# %%
import numpy as np
import pandas as pd
import os
from sklearn.model_selection import StratifiedKFold
import tensorflow as tf
import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.applications import InceptionV3
from keras.optimizers import Adam
from keras.callbacks import ReduceLROnPlateau, EarlyStopping
from keras import regularizers

# %% [markdown]
# ## Setting up parameters

# %% [markdown]
# ### Height, Width, Batch Size & Number of Splits

# %%
IMG_WIDTH = 256 # input width on the images
IMG_HEIGHT = 256 # input height on the images
BATCH_SIZE = 16 
numberOfSplits = 1 # Will generate the same number of models from each split
root = r'data'
epochs = 20
excelPath = r'excel\single-view\train-test'
trainImagesPath = r'data-train-test\train'
testImagesPath = r'data-train-test\test'

modelSavePath = r'models\single-view'


# %% [markdown]
# ### Generators
# 

# %%
train_val_generator = ImageDataGenerator(width_shift_range=0.1,
                         height_shift_range=0.1,
                         zoom_range=10,
                         shear_range = 0.1,
                         fill_mode='nearest',
                         horizontal_flip = True,
                         rescale=1./255)

test_generator = ImageDataGenerator(rescale=1./255)

# %% [markdown]
# ### Base Model

# %%
base_model = InceptionV3(weights = 'imagenet',
                        include_top = False,
                        input_shape = (IMG_WIDTH, IMG_HEIGHT, 3))

# %% [markdown]
# ## Setting up functions

# %% [markdown]
# ### Get Parts And Classes

# %%
def SetClassesAndParts(root):
    classes = os.listdir(root) # gets a list of all classes from data
    pathToParts = os.path.join(root, classes[0])
    parts = os.listdir(pathToParts) # gets a list of all parts from data
    return classes, parts

# %% [markdown]
# ### Naming Models

# %%
def get_model_name(part_name, k):
    return part_name + "_" + "model_" + str(k) + '.h5'

# %% [markdown]
# ### Creating Model

# %%
def create_functional_model(base_model, numberOfClasses):
    
    inputs = keras.Input(shape=(IMG_HEIGHT,IMG_WIDTH,3))
    x = base_model(inputs, training = False)
    x = keras.layers.GlobalAveragePooling2D()(x)
    x = keras.layers.Dropout(0.3)(x)
    
    x = keras.layers.Flatten()(x)
    
    x = keras.layers.Dense(512, activation = 'relu', kernel_regularizer=regularizers.L1L2())(x)
    outputs = keras.layers.Dense(numberOfClasses, activation = 'softmax')(x)

    model = keras.Model(inputs, outputs)
    model.layers[0].trainable = False

    return model

classes, parts = SetClassesAndParts(root)

model = create_functional_model(base_model, len(classes))

model.compile(Adam(0.0001), # OG: Adam(0.001)
            loss='categorical_crossentropy', 
            metrics=['accuracy']) 

# %% [markdown]
# ## K-Fold
# 

# %%
skf = StratifiedKFold(n_splits = numberOfSplits, random_state = 7, shuffle = True)

# %% [markdown]
# # Training models
# 

# %%

for part in parts:
    trainDataCsv = pd.read_csv(os.path.join(excelPath, part, "csv", f"single-view-{part}-train.csv"))
    testDataCsv = pd.read_csv(os.path.join(excelPath, part, "csv", f"single-view-{part}-test.csv")) 
    
    trainImagesPartPath = os.path.join(trainImagesPath, part)
    testImagesPartPath = os.path.join(testImagesPath, part)
    
    modelPartSavePath = os.path.join(modelSavePath, part)
    
    X = trainDataCsv[["filename"]] 
    Y = trainDataCsv[["class"]]

    labels = pd.unique(Y["class"]) 
    nr_classes = len(labels)   
    
    fold_var = 1
    
    validation_accuracy = []
    test_accuracy = []
    
    for train_index, val_index in skf.split(X, Y):

        trainDataAtIndex = trainDataCsv.iloc[train_index]

        validatingDataAtIndex = trainDataCsv.iloc[val_index]
        
        trainDataGenerator = train_val_generator.flow_from_dataframe(trainDataAtIndex, directory = trainImagesPartPath,
                                x_col = "filename", y_col = "class",
                                class_mode = "categorical", 
                                shuffle = True,
                                target_size=(IMG_HEIGHT, IMG_WIDTH),
                                batch_size=BATCH_SIZE)
        

        validationDataGenerator  = test_generator.flow_from_dataframe(validatingDataAtIndex, directory = trainImagesPartPath,
                                x_col = "filename", y_col = "class",
                                class_mode = "categorical", 
                                shuffle = True,
                                target_size=(IMG_HEIGHT, IMG_WIDTH),
                                batch_size=BATCH_SIZE)
        
        
        testDataGenerator  = test_generator.flow_from_dataframe(testDataCsv, directory = testImagesPartPath,
                                x_col = "filename", y_col = "class",
                                class_mode = "categorical", 
                                shuffle = True,
                                target_size=(IMG_HEIGHT, IMG_WIDTH),
                                batch_size=BATCH_SIZE)
        
        nb_train_samples = trainDataGenerator.samples
        nb_validation_samples = validationDataGenerator.samples
        nb_test_samples = testDataGenerator.samples

        
        
        checkpoint = tf.keras.callbacks.ModelCheckpoint(os.path.join(modelPartSavePath, get_model_name(part, fold_var)),
                                monitor='val_loss', verbose=1, 
                                save_best_only=True, mode='min')
        
        
        callbacks_list = [ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=0.00001),
                        EarlyStopping(patience=5), checkpoint]
        
        history = model.fit(trainDataGenerator,
                            steps_per_epoch = nb_train_samples // BATCH_SIZE, 
                            validation_data = validationDataGenerator,
                            validation_steps = nb_validation_samples // BATCH_SIZE, 
                            epochs = epochs,
                            callbacks = callbacks_list)
        
        # LOAD BEST MODEL to evaluate the performance of the model
        model.load_weights(os.path.join(modelPartSavePath, get_model_name(part, fold_var)))

        valid_res = model.evaluate(validationDataGenerator)
        validation_accuracy.append(valid_res[1])

        test_res = model.evaluate(testDataGenerator)
        test_accuracy.append(test_res[1])

        tf.keras.backend.clear_session()

        fold_var += 1
       
    print(validation_accuracy)
    print(np.average(validation_accuracy))
    print(np.std(validation_accuracy))
    
    print(test_accuracy)
    print(np.average(test_accuracy))
    print(np.std(test_accuracy))
    

# %%
validation_accuracy

# %%
np.average(validation_accuracy)

# %%
np.std(validation_accuracy)

# %%
test_accuracy

# %%
np.average(test_accuracy)

# %%
np.std(test_accuracy)


