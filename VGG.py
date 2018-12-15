{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "VGG.ipynb",
      "version": "0.3.2",
      "provenance": [],
      "collapsed_sections": [],
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/dipanjan1311/COMP551/blob/master/VGG.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "metadata": {
        "id": "u2OM48ORyouj",
        "colab_type": "code",
        "outputId": "1afc674c-367a-4868-b2df-e753cafe6d72",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 34
        }
      },
      "cell_type": "code",
      "source": [
        "import numpy   as np  \n",
        "import cv2\n",
        "from scipy import ndimage\n",
        "import scipy.misc # to visualize only\n",
        "from scipy.misc import imresize\n",
        "from skimage.restoration import denoise_bilateral\n",
        "from sklearn.svm import SVC\n",
        "from sklearn.linear_model import LogisticRegression\n",
        "from matplotlib import pyplot as plt\n",
        "!pip install -q keras\n",
        "from __future__ import print_function\n",
        "import keras\n",
        "from keras.models import Sequential\n",
        "from keras.layers import Dense, Dropout, Flatten\n",
        "from keras.layers import Conv2D, MaxPooling2D\n",
        "from keras import backend as K\n",
        "from keras.utils.np_utils import to_categorical\n",
        "from google.colab import files"
      ],
      "execution_count": 1,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "Using TensorFlow backend.\n"
          ],
          "name": "stderr"
        }
      ]
    },
    {
      "metadata": {
        "id": "8ZXUfHrryr-Z",
        "colab_type": "code",
        "outputId": "c4655b59-8ac2-4169-8394-7f82f34d8b46",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 582
        }
      },
      "cell_type": "code",
      "source": [
        "URL_ENDPOINT = \"http://cs.mcgill.ca/~ksinha4/datasets/kaggle/\"\n",
        "\n",
        "X_train = np.loadtxt(URL_ENDPOINT+\"train_x.csv\", delimiter=\",\")\n",
        "print(\"Training Set Loaded\")\n",
        "Y_train = np.loadtxt(URL_ENDPOINT+\"train_y.csv\", delimiter=\",\")\n",
        "X_test = np.loadtxt(URL_ENDPOINT+\"test_x.csv\", delimiter=\",\")\n",
        "print(\"Test Set Loaded\")\n",
        "\n",
        "X_train = X_train.reshape(-1, 64, 64) # reshape \n",
        "Y_train = Y_train.reshape(-1, 1) \n",
        "X_test = X_test.reshape(-1, 64, 64) # reshape"
      ],
      "execution_count": 2,
      "outputs": [
        {
          "output_type": "error",
          "ename": "OSError",
          "evalue": "ignored",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mOSError\u001b[0m                                   Traceback (most recent call last)",
            "\u001b[0;32m<ipython-input-2-7c936821ca5a>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m()\u001b[0m\n\u001b[1;32m      1\u001b[0m \u001b[0mURL_ENDPOINT\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0;34m\"http://cs.mcgill.ca/~ksinha4/datasets/kaggle/\"\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      2\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 3\u001b[0;31m \u001b[0mX_train\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mnp\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mloadtxt\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mURL_ENDPOINT\u001b[0m\u001b[0;34m+\u001b[0m\u001b[0;34m\"train_x.csv\"\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mdelimiter\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0;34m\",\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      4\u001b[0m \u001b[0mprint\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m\"Training Set Loaded\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      5\u001b[0m \u001b[0mY_train\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mnp\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mloadtxt\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mURL_ENDPOINT\u001b[0m\u001b[0;34m+\u001b[0m\u001b[0;34m\"train_y.csv\"\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mdelimiter\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0;34m\",\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.6/dist-packages/numpy/lib/npyio.py\u001b[0m in \u001b[0;36mloadtxt\u001b[0;34m(fname, dtype, comments, delimiter, converters, skiprows, usecols, unpack, ndmin, encoding)\u001b[0m\n\u001b[1;32m    915\u001b[0m             \u001b[0mfname\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mstr\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mfname\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    916\u001b[0m         \u001b[0;32mif\u001b[0m \u001b[0m_is_string_like\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mfname\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 917\u001b[0;31m             \u001b[0mfh\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mnp\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mlib\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m_datasource\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mopen\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mfname\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m'rt'\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mencoding\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mencoding\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    918\u001b[0m             \u001b[0mfencoding\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mgetattr\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mfh\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m'encoding'\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m'latin1'\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    919\u001b[0m             \u001b[0mfh\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0miter\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mfh\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.6/dist-packages/numpy/lib/_datasource.py\u001b[0m in \u001b[0;36mopen\u001b[0;34m(path, mode, destpath, encoding, newline)\u001b[0m\n\u001b[1;32m    258\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    259\u001b[0m     \u001b[0mds\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mDataSource\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mdestpath\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 260\u001b[0;31m     \u001b[0;32mreturn\u001b[0m \u001b[0mds\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mopen\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mpath\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mmode\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mencoding\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mencoding\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mnewline\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mnewline\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    261\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    262\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.6/dist-packages/numpy/lib/_datasource.py\u001b[0m in \u001b[0;36mopen\u001b[0;34m(self, path, mode, encoding, newline)\u001b[0m\n\u001b[1;32m    614\u001b[0m                                       encoding=encoding, newline=newline)\n\u001b[1;32m    615\u001b[0m         \u001b[0;32melse\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 616\u001b[0;31m             \u001b[0;32mraise\u001b[0m \u001b[0mIOError\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m\"%s not found.\"\u001b[0m \u001b[0;34m%\u001b[0m \u001b[0mpath\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    617\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    618\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mOSError\u001b[0m: http://cs.mcgill.ca/~ksinha4/datasets/kaggle/train_x.csv not found."
          ]
        }
      ]
    },
    {
      "metadata": {
        "id": "VWJnKC-N1fmU",
        "colab_type": "code",
        "colab": {}
      },
      "cell_type": "code",
      "source": [
        "####################### PREPROCESSING IMAGE ARRAYS #####################################\n",
        "X_train_processed = np.where(X_train>250, 1, 0)\n",
        "X_test_processed = np.where(X_test>250, 1, 0)"
      ],
      "execution_count": 0,
      "outputs": []
    },
    {
      "metadata": {
        "id": "S3DfBA_D1oJU",
        "colab_type": "code",
        "colab": {}
      },
      "cell_type": "code",
      "source": [
        "################################### GET A LIST OF BOUNDING BOX AROUND EACH DIGIT #########################################\n",
        "def get_bounding_boxes(x):\n",
        "    BB = []\n",
        "    for i in range(x.shape[0]):\n",
        "        img = x[i].copy()\n",
        "\n",
        "        # Threshold, find contours (connected parts of image with the same value)\n",
        "        ret_t, thresh = cv2.threshold(img,254,255,0)\n",
        "        im2, contours, hierarchy = cv2.findContours(np.uint8(thresh), 0, 2)\n",
        "\n",
        "        # Find min area rectangle that will encompass the contour\n",
        "        L = []\n",
        "        for c in contours:\n",
        "            rect = cv2.minAreaRect(c)\n",
        "            pos, size, orient = rect\n",
        "            area = max(size[0],size[1])**2\n",
        "            # Discard bounding boxes that cannot possibly be a digit..\n",
        "            if area > 49:\n",
        "                L.append((area,[pos[0],pos[1],size[0],size[1],orient]))\n",
        "        \n",
        "        # Sort by area, from largest to smallest\n",
        "        L.sort(key=lambda x: x[0], reverse=True)\n",
        "        L = list(list(zip(*L))[1])\n",
        "        BB.append(L)\n",
        "    \n",
        "    return BB"
      ],
      "execution_count": 0,
      "outputs": []
    },
    {
      "metadata": {
        "id": "MpEysPk83RQS",
        "colab_type": "code",
        "colab": {}
      },
      "cell_type": "code",
      "source": [
        "########################################## Return coordinates of a tight, non-oriented box around each digit ############################################\n",
        "def get_coord(img, bounding_box, offset=0):\n",
        "    _, img_t = cv2.threshold(img,254,255,0)\n",
        "    x_pos, y_pos, width, height, orient = bounding_box\n",
        "    box = cv2.boxPoints(((x_pos, y_pos),(width, height),orient))\n",
        "    box = np.int0(box)\n",
        "\n",
        "    x_min = max(min(box[:,0]),0)\n",
        "    x_max = min(max(box[:,0]),img_t.shape[0])\n",
        "    y_min = max(min(box[:,1]),0)\n",
        "    y_max = min(max(box[:,1]),img_t.shape[0])\n",
        "    \n",
        "    # Original bounding box found (discarding orientation...)\n",
        "    digit = img_t[y_min:y_max,x_min:x_max].copy()\n",
        "    \n",
        "    # Since we've discarded orientation info, we should tighten up the bounding box to compensate\n",
        "    s_x = np.sum(digit,axis=0)\n",
        "    x_nz = np.nonzero(s_x)\n",
        "    x_min += np.amin(x_nz)\n",
        "    x_max -= (digit.shape[1] - np.amax(x_nz))\n",
        "\n",
        "    s_y = np.sum(digit,axis=1)\n",
        "    y_nz = np.nonzero(s_y)\n",
        "    y_min += np.amin(y_nz)\n",
        "    y_max -= (digit.shape[0] - np.amax(y_nz))\n",
        "    \n",
        "    x_min = max(x_min-offset,0)\n",
        "    x_max = min(x_max+offset,img_t.shape[0])\n",
        "    y_min = max(y_min-offset,0)\n",
        "    y_max = min(y_max+offset,img_t.shape[0])\n",
        "    \n",
        "    width = x_max-x_min\n",
        "    height = y_max-y_min\n",
        "    \n",
        "    return x_min, y_min, width, height"
      ],
      "execution_count": 0,
      "outputs": []
    },
    {
      "metadata": {
        "id": "0RsbCB4W3Vtl",
        "colab_type": "code",
        "colab": {}
      },
      "cell_type": "code",
      "source": [
        "############################### GET THE DIGIT FROM BOUNDING BOX #########################################\n",
        "def get_digit(img, bounding_box, offset=0):\n",
        "    x, y, w, h = get_coord(img, bounding_box)\n",
        "    digit = digit[y:y+h,x:x+w].copy()\n",
        "    return digit"
      ],
      "execution_count": 0,
      "outputs": []
    },
    {
      "metadata": {
        "id": "E7mIFZHF3aS0",
        "colab_type": "code",
        "colab": {}
      },
      "cell_type": "code",
      "source": [
        "################################################ GET ORIENTED BOUNDED BOX FOR ALL ENTRIES ###################################\n",
        "# Oriented bounding boxes for all digits\n",
        "\n",
        "def get_processed_dataset(dataset):\n",
        "  TRAIN_BB = get_bounding_boxes(dataset)\n",
        "\n",
        "  DISCARD_THRESH = 64\n",
        "  TRAIN_X_ORIG = []\n",
        "  TRAIN_X_PROC = []\n",
        "  TRAIN_Y_PROC = []\n",
        "  TRAIN_BB_PROC = []\n",
        "  \n",
        "  for i in range(dataset.shape[0]):\n",
        "\n",
        "      # Cannot possibly be a single digit... Discard...\n",
        "      x_orig, y_orig, w_orig, h_orig, _ = TRAIN_BB[i][0]\n",
        "      if w_orig >= DISCARD_THRESH or h_orig >= DISCARD_THRESH:\n",
        "        print(i)\n",
        "        continue\n",
        "\n",
        "      # Get un-rotated digit and threshold...\n",
        "      x,y,w,h = get_coord(dataset[i], TRAIN_BB[i][0])\n",
        "      x,y,w,h = int(x),int(y),int(w),int(h)\n",
        "      _, img_t = cv2.threshold(dataset[i,y:y+h,x:x+w],254,255,0)  \n",
        "\n",
        "      # Pad such that we have a square...\n",
        "      max_wh = max(w,h)\n",
        "      if max_wh > w:\n",
        "        pad_amt = int((max_wh-w)/2)\n",
        "        img_t = np.pad(img_t, ((0,0),(pad_amt,pad_amt)), 'constant', constant_values=0)\n",
        "      elif max_wh > h:\n",
        "        pad_amt = int((max_wh-h)/2)\n",
        "        img_t = np.pad(img_t, ((pad_amt,pad_amt),(0,0)), 'constant', constant_values=0)\n",
        "\n",
        "      # Pad such that we have a border of 2 pixels...\n",
        "      img_t = np.pad(img_t, 2, 'constant', constant_values=0)\n",
        "      img_t = cv2.resize(img_t, (28,28))\n",
        "\n",
        "      TRAIN_X_ORIG.append(dataset[i])\n",
        "      TRAIN_X_PROC.append(img_t)\n",
        "      TRAIN_Y_PROC.append(Y_train[i])\n",
        "      TRAIN_BB_PROC.append(TRAIN_BB[i])\n",
        "\n",
        "  TRAIN_X_ORIG = np.array(TRAIN_X_ORIG)\n",
        "  TRAIN_X_PROC = np.expand_dims(np.array(TRAIN_X_PROC),axis=1)\n",
        "  TRAIN_Y_PROC = np.array(TRAIN_Y_PROC)\n",
        "  TRAIN_BB_PROC = np.array(TRAIN_BB_PROC)\n",
        "\n",
        "  # Normalize to be in range [-1,1]\n",
        "  TRAIN_X_PROC = (TRAIN_X_PROC/255)*2-1\n",
        "  \n",
        "  return TRAIN_X_PROC, TRAIN_Y_PROC"
      ],
      "execution_count": 0,
      "outputs": []
    },
    {
      "metadata": {
        "id": "-Monk2Vn1v5f",
        "colab_type": "code",
        "colab": {}
      },
      "cell_type": "code",
      "source": [
        "########################### RETRIVE PROCESSED DATASET FROM ABOVE METHODS ##############################\n",
        "\n",
        "X_train_processed, Y_train_processed = get_processed_dataset(X_train) \n",
        "X_test_processed, temp = get_processed_dataset(X_test)\n",
        "del(temp)"
      ],
      "execution_count": 0,
      "outputs": []
    },
    {
      "metadata": {
        "id": "e6R5OCCZ2UlA",
        "colab_type": "code",
        "colab": {}
      },
      "cell_type": "code",
      "source": [
        "############################## FLATENNING THE TRAINING AND TEST SET ####################################################\n",
        "X_train_ready, X_test_ready = [],[]\n",
        "\n",
        "\n",
        "#Training set\n",
        "for image in X_train_processed:\n",
        "    flat_img = image.reshape((784))\n",
        "    X_train_ready.append(flat_img)\n",
        "    \n",
        "#Test set\n",
        "for image in X_test_processed:\n",
        "    flat_img = image.reshape((784))\n",
        "    X_test_ready.append(flat_img)\n",
        "\n",
        "\n",
        "X_train_ready = np.array(X_train_ready)\n",
        "X_test_ready = np.array(X_test_ready)"
      ],
      "execution_count": 0,
      "outputs": []
    },
    {
      "metadata": {
        "id": "rfxdXjVS2Yho",
        "colab_type": "code",
        "colab": {}
      },
      "cell_type": "code",
      "source": [
        "x_train = X_train_ready\n",
        "y_train = Y_train\n",
        "x_valid = X_train_ready[37500:]\n",
        "y_valid = Y_train[37500:]\n",
        "\n",
        "x_test = X_test_ready\n",
        "x_train = x_train.reshape(x_train.shape[0], 28, 28,1).astype('float32')\n",
        "x_valid = x_valid.reshape(x_valid.shape[0], 28, 28,1).astype('float32')\n",
        "x_test = x_test.reshape(x_test.shape[0], 28, 28,1).astype('float32')\n",
        "num_classes = 10\n",
        "\n",
        "def larger_model():\n",
        "  # create model\n",
        "  model = Sequential()\n",
        "  \n",
        "  model.add(Conv2D(64, 3, 3, input_shape=(28, 28,1), activation='relu'))\n",
        "  model.add(Conv2D(64, 3, 3, activation='relu'))\n",
        "  model.add(MaxPooling2D((2, 2), strides=(2,2)))\n",
        "  model.add(Dropout(0.25))\n",
        "  \n",
        "  model.add(Conv2D(128, 3, 3, activation='relu'))\n",
        "  model.add(Conv2D(128, 3, 3, activation='relu'))\n",
        "  model.add(MaxPooling2D((2, 2), strides=(2,2)))\n",
        "  model.add(Dropout(0.25))\n",
        "  \n",
        "  model.add(Flatten())\n",
        "  model.add(Dense(2000, activation='relu'))\n",
        "  model.add(Dropout(0.25))\n",
        "  model.add(Dense(2000, activation='relu'))\n",
        "  model.add(Dropout(0.25))\n",
        "  model.add(Dense(num_classes, activation='softmax'))\n",
        "  # Compile model\n",
        "  model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])\n",
        "  return model"
      ],
      "execution_count": 0,
      "outputs": []
    },
    {
      "metadata": {
        "id": "KBybK-d74Ywf",
        "colab_type": "code",
        "outputId": "a7856cca-d87b-45e2-c53d-4e8aa4613f70",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 309
        }
      },
      "cell_type": "code",
      "source": [
        "model = larger_model()\n",
        "# Fit the model\n",
        "y_binary = to_categorical(y_train)\n",
        "y_valid_bin = to_categorical(y_valid)\n",
        "model.fit(x_train, y_binary, epochs=5, batch_size=100)\n",
        "\n",
        "# Final evaluation of the model\n",
        "scores = model.evaluate(x_valid, y_valid_bin, verbose=0)\n",
        "print(\"Deep CNN Accuracy: %.2f%%\" % (100-scores[1]*100))"
      ],
      "execution_count": 0,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "/usr/local/lib/python3.6/dist-packages/ipykernel_launcher.py:16: UserWarning: Update your `Conv2D` call to the Keras 2 API: `Conv2D(64, (3, 3), input_shape=(28, 28, 1..., activation=\"relu\")`\n",
            "  app.launch_new_instance()\n",
            "/usr/local/lib/python3.6/dist-packages/ipykernel_launcher.py:17: UserWarning: Update your `Conv2D` call to the Keras 2 API: `Conv2D(64, (3, 3), activation=\"relu\")`\n",
            "/usr/local/lib/python3.6/dist-packages/ipykernel_launcher.py:21: UserWarning: Update your `Conv2D` call to the Keras 2 API: `Conv2D(128, (3, 3), activation=\"relu\")`\n",
            "/usr/local/lib/python3.6/dist-packages/ipykernel_launcher.py:22: UserWarning: Update your `Conv2D` call to the Keras 2 API: `Conv2D(128, (3, 3), activation=\"relu\")`\n"
          ],
          "name": "stderr"
        },
        {
          "output_type": "stream",
          "text": [
            "Epoch 1/5\n",
            "50000/50000 [==============================] - 426s 9ms/step - loss: 0.5151 - acc: 0.8555\n",
            "Epoch 2/5\n",
            "26800/50000 [===============>..............] - ETA: 3:18 - loss: 0.3093 - acc: 0.9235"
          ],
          "name": "stdout"
        },
        {
          "output_type": "stream",
          "text": [
            "50000/50000 [==============================] - 426s 9ms/step - loss: 0.3059 - acc: 0.9251\n",
            "Epoch 3/5\n",
            "43300/50000 [========================>.....] - ETA: 56s - loss: 0.2684 - acc: 0.9351"
          ],
          "name": "stdout"
        },
        {
          "output_type": "stream",
          "text": [
            "50000/50000 [==============================] - 422s 8ms/step - loss: 0.2674 - acc: 0.9354\n",
            "Epoch 4/5\n",
            "50000/50000 [==============================] - 422s 8ms/step - loss: 0.2415 - acc: 0.9411\n",
            "Epoch 5/5\n",
            "  500/50000 [..............................] - ETA: 7:01 - loss: 0.2014 - acc: 0.9400"
          ],
          "name": "stdout"
        },
        {
          "output_type": "stream",
          "text": [
            "50000/50000 [==============================] - 427s 9ms/step - loss: 0.2219 - acc: 0.9458\n",
            "Deep CNN Accuracy: 3.78%\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "metadata": {
        "id": "rUKvXdWJ5r3E",
        "colab_type": "code",
        "colab": {}
      },
      "cell_type": "code",
      "source": [
        "#Predict labels on test set\n",
        "eval_results = model.predict(x_test, batch_size=None, verbose=0, steps=None)"
      ],
      "execution_count": 0,
      "outputs": []
    },
    {
      "metadata": {
        "id": "9F2U1zMDGJrR",
        "colab_type": "code",
        "colab": {}
      },
      "cell_type": "code",
      "source": [
        "cnn_pred = []\n",
        "\n",
        "for pred in eval_results:\n",
        "  cnn_pred.append(np.argmax(pred))\n",
        "cnn_pred = np.array(cnn_pred, dtype = np.int32)"
      ],
      "execution_count": 0,
      "outputs": []
    },
    {
      "metadata": {
        "id": "2IAkfXw7GV5-",
        "colab_type": "code",
        "colab": {}
      },
      "cell_type": "code",
      "source": [
        "######################### SAVING PREDICTIONS TO FILE ############################################\n",
        "index = np.arange(len(X_test))\n",
        "\n",
        "#Formatting CNN data for submission\n",
        "cnn_submission = []\n",
        "cnn_submission.append('Id,Label')\n",
        "for i in range(len(cnn_pred)):\n",
        "    string = str(index[i]) + ',' + str(cnn_pred[i])\n",
        "    cnn_submission.append(string)\n",
        "cnn_submission = np.array(cnn_submission)\n",
        "\n",
        "#Save in csv file for Convoluted Neural Nets\n",
        "np.savetxt('DEEPCNN.csv', cnn_submission, fmt=\"%s\")\n",
        "\n",
        "\n",
        "files.download('DEEPCNN.csv')"
      ],
      "execution_count": 0,
      "outputs": []
    }
  ]
}