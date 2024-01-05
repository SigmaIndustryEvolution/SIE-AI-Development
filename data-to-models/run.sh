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
python python-scripts/3-structure-into-train-val-test/1-create-dir-with-part-class/create-empty-directories-parts-classes.py
echo -ne '(20%) ##\r'
python python-scripts/3-structure-into-train-val-test/2-create-train-val-test-one-folder/split-data-into-single-view-train-val-test-one-folder.py
echo -ne '(40%) ###\r'
python python-scripts/3-structure-into-train-val-test/3-create-train-test-one-folder/put-val-into-train.py
echo -ne '(60%) ####\r'
python python-scripts/3-structure-into-train-val-test/4-divide-train-val-test-into-parts/put-train-test-into-parts.py
echo -ne '(80%) #####\r'
python python-scripts/3-structure-into-train-val-test/4-divide-train-val-test-into-parts/put-train-val-test-into-parts.py
echo -ne '(100%) ######\r'
echo -ne '\n'

echo -e "\n\n----------------------------------------"
end=$(date +%s)
elapsed=$((end - start))
echo -e "Elapsed time: $elapsed seconds"
echo -e "----------------------------------------\n\n"

echo "Creating neccesary directories ..."
python python-scripts/4-create-csv-for-single-and-multiview/create-csv-from-directory-multi-view.py

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
python python-scripts/5-run-single-part-models/training-single-view.py

echo -e "\n\n----------------------------------------"
end=$(date +%s)
elapsed=$((end - start))
echo -e "Elapsed time: $elapsed seconds"
echo -e "----------------------------------------\n\n"


echo "Training multi-view model"
python python-scripts/6-run-multi-view/multi-view-train.py

echo -e "\n\n----------------------------------------"
end=$(date +%s)
elapsed=$((end - start))
echo -e "Elapsed time: $elapsed seconds"
echo -e "----------------------------------------\n\n"


echo "Testing models with testset"
python python-scripts/7-testing/put-images-into-parts.py
echo "Testing single view models"
python python-scripts/7-testing/testing-single-view.py
echo "Testing multi-view model"
python python-scripts/7-testing/testing-multi-view.py

echo "Removing directory"
rm -r test-data-views


end=$(date +%s)
elapsed=$((end - start))
echo "Total time: $elapsed seconds"
