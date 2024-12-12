# aimanual/helper.py

def helper():
    """
    import numpy as np 
    import pandas as pd

    import random

    import tensorflow as tf
    from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img

    import matplotlib.pyplot as plt

    #
    base_dir = os.path.join("/kaggle/input/rock-paper-scissors-dataset/Rock-Paper-Scissors")
    print("Base directory --> ", os.listdir(base_dir))
    # : Base directory -->  ['validation', 'test', 'train']

    # Train set
    train_dir = os.path.join("/kaggle/input/rock-paper-scissors-dataset/Rock-Paper-Scissors/train/")
    print("Train --> ", os.listdir(train_dir))

    # Test set
    test_dir = os.path.join("/kaggle/input/rock-paper-scissors-dataset/Rock-Paper-Scissors/test/")
    print("Test --> ", os.listdir(test_dir))

    # Validation set
    validation_dir = os.path.join("/kaggle/input/rock-paper-scissors-dataset/Rock-Paper-Scissors/validation/")
    print("Validation --> ", os.listdir(validation_dir)[:5])
    #: Train -->  ['paper', 'rock', 'scissors']
    #: Test -->  ['paper', 'rock', 'scissors']
    #: Validation -->  ['paper8.png', 'paper1.png', 'rock4.png', 'scissors3.png', 'rock2.png']
    
    
    # Displaying random image from the dataset

    fig, ax = plt.subplots(1, 3, figsize=(15, 10))

    sample_paper = random.choice(os.listdir(train_dir + "paper"))
    image = load_img(train_dir + "paper/" + sample_paper)
    ax[0].imshow(image)
    ax[0].set_title("Paper")
    ax[0].axis("Off")

    sample_rock = random.choice(os.listdir(train_dir + "rock"))
    image = load_img(train_dir + "rock/" + sample_rock)
    ax[1].imshow(image)
    ax[1].set_title("Rock")
    ax[1].axis("Off")

    sample_scissor = random.choice(os.listdir(train_dir + "scissors"))
    image = load_img(train_dir + "scissors/" + sample_scissor)
    ax[2].imshow(image)
    ax[2].set_title("Scissor")
    ax[2].axis("Off")

    plt.show()

    image.size

    model = tf.keras.models.Sequential([
        
        tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(300, 300, 3)),
        tf.keras.layers.MaxPooling2D(2, 2),
        
        tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2,2),
        
        tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2,2),
        
        tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2,2),
        
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(512, activation='relu'),
        
        tf.keras.layers.Dense(3, activation='softmax')
    ])


    model.compile(loss = 'categorical_crossentropy',
                  optimizer = 'adam',
                  metrics = ['accuracy'])
                  
    class myCallback(tf.keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs={}):
            if(logs.get('accuracy')>0.95):
                print("\nReached >95% accuracy so cancelling training!")
                self.model.stop_training = True
            
    callbacks = myCallback()


    train_datagen = ImageDataGenerator(
          rescale=1./255,
          rotation_range=40,
          width_shift_range=0.2, # Shifting image width by 20%
          height_shift_range=0.2,# Shifting image height by 20%
          shear_range=0.2,       # Rotation across X-axis by 20%
          zoom_range=0.2,        # Image zooming by 20%
          horizontal_flip=True,
          fill_mode='nearest')

    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size = (300, 300),
        class_mode = 'categorical',
        batch_size = 20
    )

    validation_datagen = ImageDataGenerator(rescale=1./255)

    validation_generator = validation_datagen.flow_from_directory(
        test_dir,
        target_size = (300, 300),
        class_mode = 'categorical',
        batch_size = 20
    )


    history = model.fit_generator(
          train_generator,
          steps_per_epoch = np.ceil(2520/20),  # 2520 images = batch_size * steps
          epochs = 10,
          validation_data=validation_generator,
          validation_steps = np.ceil(372/20),  # 372 images = batch_size * steps
          callbacks=[callbacks],
          verbose = 2)
          
          
    model.save('./model_2nd.h5')
    from tensorflow.keras.models import load_model

    # 모델 로드
    model = load_model('./model_2nd.h5')

    # 모델 구조 확인
    model.summary()

    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs = range(len(acc))

    plt.figure(figsize=(7,7))

    plt.plot(epochs, acc, 'r', label='Training accuracy')
    plt.plot(epochs, val_acc, 'b', label='Validation accuracy')
    plt.title('Training and validation accuracy')
    plt.legend()

    plt.figure(figsize=(7,7))

    plt.plot(epochs, loss, 'r', label='Training Loss')
    plt.plot(epochs, val_loss, 'b', label='Validation Loss')
    plt.title('Training and validation loss')
    plt.legend()

    plt.show()

    test_img = os.listdir(os.path.join(validation_dir))

    test_df = pd.DataFrame({'Image': test_img})
    test_df.head()

    test_gen = ImageDataGenerator(rescale=1./255)

    test_generator = test_gen.flow_from_dataframe(
        test_df, 
        validation_dir, 
        x_col = 'Image',
        y_col = None,
        class_mode = None,
        target_size = (300, 300),
        batch_size = 1,
        shuffle = False
    )

    # predict = model.predict_generator(test_generator, steps = int(np.ceil(33/20)))
    # predict = model.predict_generator(test_generator)#, steps = 33)
    predict = model.predict(test_generator)

    # Identifying the classes

    label_map = dict((v,k) for k,v in train_generator.class_indices.items())
    # dict k,v ==> dict v,k   idx2str label

    label_map

    # predict = model.predict_generator(test_generator, steps = int(np.ceil(33/20)))
    # predict = model.predict_generator(test_generator)#, steps = 33)
    predict = model.predict(test_generator)

    # Identifying the classes

    label_map = dict((v,k) for k,v in train_generator.class_indices.items())
    # dict k,v ==> dict v,k   idx2str label

    label_map

    test_df['Label'] = np.argmax(predict, axis = -1) # axis = -1 --> To compute the max element index within list of lists

    test_df['Label'] = test_df['Label'].replace(label_map)

    if False:
        test_df.replace({'Label':label_map}, inplace=True)
        
    lis = []
    for ind in test_df.index: 
        if(test_df['Label'][ind] in test_df['Image'][ind]):
            lis.append(1)
        else:
            lis.append(0)
            print(ind)
            
    print("Accuracy of the model on test data is {:.2f}".format((sum(lis)/len(lis))*100))
    """
    return f"Hello, {name}!"
