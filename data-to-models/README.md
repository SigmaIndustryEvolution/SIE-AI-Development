# Data to Model script

This script takes images ordered in classes and views and outputs models in form of CNNs. Number of models are equal to the number of views plus one multi-view model. 
Works for Windows. 

## Installation

Make sure that [python](https://www.python.org/downloads/) and [bash](https://www.lifewire.com/install-bash-on-windows-10-4101773) is installed
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all dependencies. 

## Preperation

In order for the script to create models and train, one needs to have a folder called "data" in the same folder as the script and the belonging files.
This folder should have a similar structure as this:
|- DATA 
 \n├───class-1 \n
│   ├───view-1 \n
│   │       image-1.png \n
│   │       image-2.png \n
│   │       image-3.png \n
│   │\n
│   ├───view-2 \n
│   │       image-1.png \n
│   │       image-2.png \n
│   │       image-3.png \n
│   │\n
│   └───view-3 \n
│           image-1.png \n
│           image-2.png \n
│           image-3.png \n
│\n
├───class-2 \n
│   ├───view-1 \n
│   │       image-1.png \n
│   │       image-2.png \n
│   │       image-3.png \n
│   │\n
│   ├───view-2 \n
│   │       image-1.png \n
│   │       image-2.png \n
│   │       image-3.png \n
│   │\n
│   └───view-3 \n
│           image-1.png \n
│           image-2.png \n
│           image-3.png \n
│\n
├───class-3 \n
│   ├───view-1 \n
│   │       image-1.png \n
│   │       image-2.png \n
│   │       image-3.png \n
│   │\n
│   ├───view-2 \n
│   │       image-1.png \n
│   │       image-2.png \n
│   │       image-3.png \n
│   │\n
│   └───view-3 \n
│           image-1.png \n
│           image-2.png \n
│           image-3.png \n

If one also wants to test the model on a set of images, add a folder called "test-data" using the same structure as above. 

## Usage



## Contributing

If one finds a better way to prepare images, structure excel files or to build and train models, feel free to change the code for improvements! :)
 
## License

[MIT](https://choosealicense.com/licenses/mit/)
