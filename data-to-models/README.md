# Data to Model script

This script takes images ordered in classes and views and outputs models in form of CNNs. Number of models are equal to the number of views plus one multi-view model.   
Works for Windows. 

## Installation

Make sure that [python](https://www.python.org/downloads/) and [bash](https://www.lifewire.com/install-bash-on-windows-10-4101773) is installed.  
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all dependencies. 

## Preperation

In order for the script to create models and train, one needs to have a folder called "data" in the same folder as the script and the belonging files.
This folder should have a similar structure as this:  
|- DATA  
├───class-1  
│   ├───view-1  
│   │       image-1.png  
│   │       image-2.png  
│   │       image-3.png  
│   │  
│   ├───view-2  
│   │       image-1.png  
│   │       image-2.png  
│   │       image-3.png  
│   │  
│   └───view-3  
│           image-1.png  
│           image-2.png  
│           image-3.png  
│  
├───class-2  
│   ├───view-1  
│   │       image-1.png  
│   │       image-2.png  
│   │       image-3.png  
│   │  
│   ├───view-2  
│   │       image-1.png  
│   │       image-2.png  
│   │       image-3.png  
│   │  
│   └───view-3  
│           image-1.png  
│           image-2.png  
│           image-3.png  
│  
├───class-3  
│   ├───view-1  
│   │       image-1.png  
│   │       image-2.png  
│   │       image-3.png  
│   │  
│   ├───view-2  
│   │       image-1.png  
│   │       image-2.png  
│   │       image-3.png  
│   │  
│   └───view-3  
│           image-1.png  
│           image-2.png  
│           image-3.png  

If one also wants to test the model on a set of images, add a folder called "test-data" using the same structure as above. 

## Usage



## Contributing

If one finds a better way to prepare images, structure excel files or to build and train models, feel free to change the code for improvements! :)
 
## License

[MIT](https://choosealicense.com/licenses/mit/)
