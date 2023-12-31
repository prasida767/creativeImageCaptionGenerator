import os
import string
import re


def pre_process(fileName, uniqueFileNumber, paramsTrainTest, purpose):
    descriptionsDictionary = create_image_captions_dict(fileName)

    clean_descriptions = cleaning_text(descriptionsDictionary)
    # Contains file with imageNames
    fileWithImageName = create_image_names_file(clean_descriptions, f"{uniqueFileNumber}_{purpose}_{paramsTrainTest}")

    # building vocabulary
    vocabulary = text_vocabulary(clean_descriptions)
    print("Length of vocabulary = ", len(vocabulary))

    # saving each description to file
    fileWithImageAndDescription = save_descriptions(clean_descriptions,
                                                    f"{uniqueFileNumber}_{purpose}_{paramsTrainTest}_descriptions")

    return descriptionsDictionary, fileWithImageName, fileWithImageAndDescription


class PreprocessDataset:

    def __init__(self, fileName, uniqueFileNumber, trainParams, purpose):
        self.fileName = fileName
        self.descriptionsDictionary, self.fileWithImageName, self.fileWithCaptionAndImageName = pre_process(
            fileName, uniqueFileNumber, trainParams, purpose)

    def __iter__(self):
        return iter([self.descriptionsDictionary, self.fileWithImageName, self.fileWithCaptionAndImageName])


# Loading a text file into memory
def create_image_captions_dict(filename):
    descriptions_dict = {}
    with open(filename, 'r') as file:
        for line in file:
            values = line.strip().split(',')
            image = values[0]
            caption = ','.join(values[1:])  # Join the remaining values as the caption

            if image in descriptions_dict:
                descriptions_dict[image].append(caption)
            else:
                descriptions_dict[image] = [caption]
    return descriptions_dict


# Data cleaning-lower casing, removing puntuations and words containing numbers
def cleaning_text(captions):
    table = str.maketrans('', '', string.punctuation)
    for img, caps in captions.items():
        for i, img_caption in enumerate(caps):
            img_caption.replace("-", " ")
            desc = img_caption.split()
            # converts to lowercase
            desc = [word.lower() for word in desc]
            # remove punctuation from each token
            desc = [word.translate(table) for word in desc]
            # remove hanging 's and a
            desc = [word for word in desc if (len(word) > 1)]
            # remove tokens with numbers in them
            desc = [word for word in desc if (word.isalpha())]
            # convert back to string
            img_caption = ' '.join(desc)
            captions[img][i] = img_caption
    return captions


def text_vocabulary(descriptions_file):
    # build vocabulary of all unique words
    vocab = set()
    for key in descriptions_file.keys():
        [vocab.update(d.split()) for d in descriptions_file[key]]
    return vocab


# All descriptions in one file
def save_descriptions(clean_descriptionsToFile, filename, output_dir="descriptionsFolder"):
    lines = list()
    for key, desc_list in clean_descriptionsToFile.items():
        for desc in desc_list:
            lines.append(key + '\t' + desc)

    data = "\n".join(lines)

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    filename = os.path.join(output_dir, f"{filename}.txt")  # Append the file_number to the filename
    with open(filename, "w") as file:
        file.write(data)

    return filename


def create_image_names_file(imageWithDescriptions, file, output_dir="imagesName"):
    image_names = list(imageWithDescriptions.keys())
    data = "\n".join(image_names)

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    filename = os.path.join(output_dir, f"{file}_image.txt")
    with open(filename, "w") as file:
        file.write(data)
    return filename

