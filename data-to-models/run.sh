#!/bin/bash

start=$(date +%s)
pip install -r requirements.txt
echo "Renaming images ..."
python python-scripts/1-rename-images/rename-files.py

echo "Rotating images ..."
python python-scripts/2-rotate-images/rotate_images_to_portrait.py

echo -e "\n\n----------------------------------------"
end=$(date +%s)
elapsed=$((end - start))
echo -e "Elapsed time: $elapsed seconds"
echo -e "----------------------------------------\n\n"

echo "Creating neccesary directories ..."
echo -ne '(0%) #\r'
python -m python-scripts.3-structure-into-train-val-test.1-create-dir-with-part-class.create-empty-directories-parts-classes
echo -ne '(20%) ##\r'
python -m python-scripts.3-structure-into-train-val-test.2-create-train-val-test-one-folder.split-data-into-single-view-train-val-test-one-folder
echo -ne '(40%) ###\r'
python python-scripts/3-structure-into-train-val-test/3-create-train-test-one-folder/put-val-into-train.py
echo -ne '(60%) ####\r'
python -m python-scripts.3-structure-into-train-val-test.4-divide-train-val-test-into-parts.put-train-test-into-parts
echo -ne '(80%) #####\r'
python- -m python-scripts.3-structure-into-train-val-test.4-divide-train-val-test-into-parts.put-train-val-test-into-parts
echo -ne '(100%) ######\r'
echo -ne '\n'

echo -e "\n\n----------------------------------------"
end=$(date +%s)
elapsed=$((end - start))
echo -e "Elapsed time: $elapsed seconds"
echo -e "----------------------------------------\n\n"

echo "Creating neccesary directories ..."
python -m python-scripts.4-create-csv-for-single-and-multiview.create-csv-from-directory-multi-view

echo -e "\n\n----------------------------------------"
end=$(date +%s)
elapsed=$((end - start))
echo -e "Elapsed time: $elapsed seconds"
echo -e "----------------------------------------\n\n"


echo "Removing directories"
rm -r data-parts-classes
rm -r data-train-test-one-folder
rm -r data-train-test
rm -r data-train-val-test

echo "Training single models"
python -m python-scripts.5-run-single-part-models.training-single-view

echo -e "\n\n----------------------------------------"
end=$(date +%s)
elapsed=$((end - start))
echo -e "Elapsed time: $elapsed seconds"
echo -e "----------------------------------------\n\n"


echo "Training multi-view model"
python -m python-scripts.6-run-multi-view.training-multi-view

echo -e "\n\n----------------------------------------"
end=$(date +%s)
elapsed=$((end - start))
echo -e "Elapsed time: $elapsed seconds"
echo -e "----------------------------------------\n\n"


echo "Testing models with testset"
python -m python-scripts.7-testing.put-images-into-parts
echo "Testing single view models"
python -m python-scripts.7-testing.testing-single-view
echo "Testing multi-view model"
python -m python-scripts.7-testing.testing-multi-view

echo "Removing directory"
rm -r test-data-views


end=$(date +%s)
elapsed=$((end - start))
echo "Total time: $elapsed seconds"
