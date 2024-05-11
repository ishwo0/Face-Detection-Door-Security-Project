from pathlib import Path    # IMPORTS FOR ENCODING FACES

import face_recognition     # IMPORTS FOR ENCODING FACES

import pickle               # IMPORTS FOR SAVING NAME-ENCODING DICTIONARY

import argparse             # IMPORTS FOR COMMAND-LINE ARGUMENTS

from collections import Counter     # IMPORTS FOR VOTE TRACKING

from PIL import Image, ImageDraw    # IMPORTS FOR DRAWING BOX AROUND FACE




DEFAULT_ENCODINGS_PATH = Path("output/encodings.pkl")   # CONSTANT FOR ENCODING PATH


def encode_known_faces(     # Function with for loop to go through each directory within training folder, save the label from each directory into 'name', and then uses load_image_file() from face_recognition import to load each image
    model: str = "hog", encodings_location: Path = DEFAULT_ENCODINGS_PATH   # input for function... HOG model type and location to save the encodings generated for each image
) -> None:
    
    names = []      # lists for names and encodings
    encodings = []  # ...

    for filepath in Path("training").glob("*/*"):   # for loop to go through each directory within the training folder

        name = filepath.parent.name     # save the label from each directory into 'name'
        image = face_recognition.load_image_file(filepath)  # load_image_file() from face_recognition import to load each image

        face_locations = face_recognition.face_locations(image, model=model)    # this method detects the location of faces in each image (this returns a list of four-element tuples, 
                                                                                # one tuple for each detected face. These four elements per tuple are the four coordinates of a box 
                                                                                # that could surround the detected face, aka bounding box)
                                                                                
        face_encodings = face_recognition.face_encodings(image, face_locations) # this function generates encodings for the detected faces in an image

        for encoding in face_encodings:     # add the names and their incodings into separate lists
            names.append(name)              # ...
            encodings.append(encoding)      # ...


    name_encodings = {"names": names, "encodings": encodings}       # these three lines creates a dictionary and puts the names
    with encodings_location.open(mode="wb") as f:                   # and encodings lists together and denotes which list is which
        pickle.dump(name_encodings, f)                              # then use pickle to save the encodings to disk



def _recognize_face(unknown_encoding, loaded_encodings):    # Function to identify each face in the given image
    
    boolean_matches = face_recognition.compare_faces(       # this method compares each unknown encoding in 
        loaded_encodings["encodings"], unknown_encoding     # your test image with encodings that you loaded previously
    )                                                       # will return a list of True and False values for each loaded encoding
                                                            # the indices of this list are equal to those of the loaded encodings, so the next
                                                            # thing to do is keep track of the votes for each possible match
    
    votes = Counter(    # keep track of the votes for each possible match using Counter import
        name
        for match, name in zip(boolean_matches, loaded_encodings["names"])  # track how many votes each potential match has by
        if match                                                            # counting the True values for each loaded encoding by the associated name
    )

    if votes:
        return votes.most_common(1)[0][0]       # return the name that has the most votes in its favor
    
encode_known_faces()