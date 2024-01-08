# %% [markdown]
# # Imports

# %%
import pandas as pd
from keras.preprocessing.image import ImageDataGenerator
from keras.applications import InceptionV3
from keras.optimizers import Adam
from keras.callbacks import ReduceLROnPlateau, EarlyStopping, ModelCheckpoint
from keras import regularizers
import keras
from ..tools import SetClassesAndParts

# %% [markdown]
# # Single View

# %% [markdown]
# ## Creating variables

# %%
IMG_WIDTH = 256
IMG_HEIGHT = 256
BATCH_SIZE = 16

trainData = pd.read_csv('excel/multi-view/csv/multi-view-train.csv')
trainDir = 'data-train-val-test-one-folder/train'

validationData = pd.read_csv('excel/multi-view/csv/multi-view-val.csv')
validationDir = 'data-train-val-test-one-folder/val/'

testData = pd.read_csv('excel/multi-view/csv/multi-view-test.csv')
testDir = 'data-train-val-test-one-folder/test/'

trainGenerator = ImageDataGenerator(width_shift_range=0.1,
                         height_shift_range=0.1,
                         zoom_range=0.1,
                         rotation_range=10,
                         shear_range = 0.1,
                         fill_mode='nearest',
                         horizontal_flip = True,
                         preprocessing_function = keras.applications.inception_v3.preprocess_input)

validationGenerator = ImageDataGenerator(preprocessing_function = keras.applications.inception_v3.preprocess_input)

testGenerator = ImageDataGenerator(preprocessing_function = keras.applications.inception_v3.preprocess_input)


# %% [markdown]
# ## Creating functions

# %%

def create_model(baseModel, numberOfClasses):
    
    inputs = keras.Input(shape=(IMG_HEIGHT, IMG_WIDTH, 3))
    x = baseModel(inputs, training = False)
    x = keras.layers.GlobalAveragePooling2D()(x)
    x = keras.layers.Dropout(0.3)(x)

    x = keras.layers.Flatten()(x)

    x = keras.layers.Dense(512, activation='relu', kernel_regularizer=regularizers.L1L2())(x)
    outputs = keras.layers.Dense(numberOfClasses, activation='softmax')(x)

    model = keras.Model(inputs,outputs)

    return model

# %%
root = r'data'

classes, parts = SetClassesAndParts()

# %% [markdown]
# ## Model

# %%
base_model = InceptionV3(weights = 'imagenet',
                        include_top = False,
                        input_shape = (IMG_WIDTH, IMG_HEIGHT, 3))
base_model.trainable = False

# %% [markdown]
# ### Training and evaluation

# %%
epochs = 10


for part in parts:
    
    train_data = trainData[[part, 'class']]
    validation_data = validationData[[part, 'class']]
    test_data = testData[[part, 'class']]       
    
    train_data_generator = trainGenerator.flow_from_dataframe(train_data, directory = trainDir,
						       x_col = part, y_col = "class",
						       class_mode = "categorical", 
                               shuffle = True,
                               target_size=(IMG_HEIGHT, IMG_WIDTH),
                               batch_size=BATCH_SIZE,
                               interpolation = 'lanczos')

    validation_data_generator = validationGenerator.flow_from_dataframe(validation_data, directory = validationDir,
                                x_col = part, y_col = "class",
                                class_mode = "categorical", 
                                shuffle = True,
                                target_size=(IMG_HEIGHT, IMG_WIDTH),
                                batch_size=BATCH_SIZE,
                                interpolation = 'lanczos')

    test_data_generator = testGenerator.flow_from_dataframe(test_data, directory = testDir,
                                x_col = part, y_col = "class",
                                class_mode = "categorical",
                                target_size=(IMG_HEIGHT, IMG_WIDTH),
                                interpolation = 'lanczos')

    model = create_model(base_model, len(classes))

    model.compile(Adam(0.001), 
                    loss='categorical_crossentropy', 
                    metrics=['accuracy']) 

    callbacks_list = [ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=0.00001),
                        EarlyStopping(monitor= "val_loss", patience=5),
                        ModelCheckpoint(f'models/single-view/{part}/model_{part}.h5',
                                        monitor = "val_loss",
                                        save_best_only=True, 
                                        mode='min', 
                                        verbose = 1)]

    history = model.fit(train_data_generator,
                        validation_data=validation_data_generator,
                        epochs = epochs,
                        callbacks=callbacks_list)



