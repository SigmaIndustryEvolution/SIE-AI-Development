# %%
import numpy as np
import pandas as pd
import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from keras.callbacks import ReduceLROnPlateau, EarlyStopping
import os
import keras
from ..tools import SetClassesAndParts

# %% [markdown]
# ## Setting up parameters
#  

# %%
IMG_WIDTH = 256
IMG_HEIGHT = 256
BATCH_SIZE = 16

train_dir = r'data-train-val-test-one-folder/train'
validation_dir = r'data-train-val-test-one-folder/val'
test_dir = r'data-train-val-test-one-folder/test'

excelPathTrain = r'excel/multi-view/csv/multi-view-train.csv'
excelPathVal = r'excel/multi-view/csv/multi-view-val.csv'
excelPathTest = r'excel/multi-view/csv/multi-view-test.csv'
epochs = 5
modelSavePath = r'models/multi-view'

# %% [markdown]
# ## Setting up functions and classes

# %%
class MultiGenDF(tf.keras.utils.Sequence):

    def __init__(self, view_generators, shuffle):
        self.view_generators = view_generators
        self.shuffle = shuffle
        self.batch_size = view_generators[0].batch_size
        self.num_steps = len(view_generators[0])
        self.indices = np.arange(view_generators[0].samples)
        if self.shuffle:
            np.random.shuffle(self.indices)

    def __getitem__(self, index):
        indices = self.indices[index*self.batch_size : (index+1)*self.batch_size]
        data = []
        for gen in self.view_generators:
            minibatch = gen._get_batches_of_transformed_samples(indices)
            data.append(minibatch[0])
        labels = minibatch[1]
        return data, labels
        
    def __len__(self):
        return self.num_steps
        
    def on_epoch_end(self):
        if self.shuffle:
            np.random.shuffle(self.indices)

# %%
         
def build_datagenerator_df(df, input_size, batch_size, views, shuffle, dir, train_val = True, seed=0):
    
    if train_val:
        generator = ImageDataGenerator(width_shift_range=0.1,
                            height_shift_range=0.1,
                            zoom_range=0.2,
                            fill_mode='nearest',
                            horizontal_flip = True,
                            preprocessing_function = keras.applications.inception_v3.preprocess_input)
    
    else:
        generator = ImageDataGenerator(preprocessing_function = keras.applications.inception_v3.preprocess_input)

    view_generators = []

    for view in views:
        view_generators.append(
            generator.flow_from_dataframe(
                dataframe=df,
                directory=dir,
                x_col=view,
                y_col='class',
                target_size=input_size,
                class_mode='categorical',
                shuffle=False,
                seed = seed,
                batch_size=batch_size   
            )
        )

    return MultiGenDF(view_generators=view_generators, shuffle=shuffle)

def buildLateFusionFC(models):

    inputs = [keras.layers.Input(shape=(IMG_WIDTH,IMG_HEIGHT,3)) for i in range(len(models))]

    streams = []
    i = 0
    for model in models:
        temp = keras.Model(model.input, model.layers[-2].output)
        temp.layers[-1]._outbound_nodes = []
        temp.trainable = False
        streams.append(temp(inputs[i]))
        i += 1

    fusionFC = keras.layers.Concatenate()(streams)

    fusionFC = keras.layers.Dense(models[0].layers[-1].get_config()['units'], activation='softmax')(fusionFC)

    multi_view = keras.Model(inputs, fusionFC)

    return multi_view

# %% [markdown]
# ### Train, validation and test

# %%
classes, parts = SetClassesAndParts()

train_data_multi = pd.read_csv(excelPathTrain)
multi_gen_df_train = build_datagenerator_df(train_data_multi, (IMG_WIDTH,IMG_HEIGHT), BATCH_SIZE//3, views=parts, shuffle = True, dir=train_dir)

validation_data_multi = pd.read_csv(excelPathVal)
multi_gen_df_validation = build_datagenerator_df(validation_data_multi, (IMG_WIDTH,IMG_HEIGHT), BATCH_SIZE//3, views=parts, shuffle = True, dir=validation_dir)

test_data_multi = pd.read_csv(excelPathTest)
multi_gen_df_test = build_datagenerator_df(test_data_multi, batch_size=BATCH_SIZE, shuffle = False, input_size=(IMG_WIDTH,IMG_HEIGHT), views=parts, dir=test_dir, train_val=False)

# %% [markdown]
# ## Model creation

# %%
models = []

for part in parts: # FIX: How to choose the best model for each view, not sure yet so is using fixed number and model
    models.append(keras.models.load_model(os.path.join("models/single-view", part, f"model_{part}.h5")))
multi_view = buildLateFusionFC(models)
multi_view.summary()

# %%
# keras.utils.plot_model(multi_view, show_shapes=True)

# %%
checkpoint = tf.keras.callbacks.ModelCheckpoint(os.path.join(modelSavePath, "multi-view.h5"), 
							monitor='val_loss', verbose=1, 
							save_best_only=True, mode='min')

callbacks_list = [ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=0.00001),
                      EarlyStopping(monitor= "val_loss", patience=5),
                      checkpoint]
optimizer = Adam(learning_rate=0.001)

# %%
multi_view.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
multi_view.summary()

# %%
history = multi_view.fit(
        multi_gen_df_train,
        epochs=epochs,
        verbose = 1,
        validation_data=multi_gen_df_validation,
        callbacks = callbacks_list)

# %%
multi_view.evaluate(multi_gen_df_test)


