from random import randint
import numpy
from tkinter import *
from tkinter import filedialog, Text, Tk
import os
import tkinter as tk
from PIL import Image, ImageTk


def upshift(a, index, n):
    col = []
    for j in range(len(a)):
        col.append(a[j][index])
    shiftCol = numpy.roll(col, -n)
    for i in range(len(a)):
        for j in range(len(a[0])):
            if j == index:
                a[i][j] = shiftCol[i]


def downshift(a, index, n):
    col = []
    for j in range(len(a)):
        col.append(a[j][index])
    shiftCol = numpy.roll(col, n)
    for i in range(len(a)):
        for j in range(len(a[0])):
            if j == index:
                a[i][j] = shiftCol[i]


def rotate180(n):
    bits = "{0:b}".format(n)
    return int(bits[::-1], 2)


def encryption(im, pix):
    # Obtaining the RGB matrices
    r = []
    g = []
    b = []
    for i in range(im.size[0]):
        r.append([])
        g.append([])
        b.append([])
        for j in range(im.size[1]):
            rgbPerPixel = pix[i, j]
            r[i].append(rgbPerPixel[0])
            g[i].append(rgbPerPixel[1])
            b[i].append(rgbPerPixel[2])

    # M x N image matrix
    m = im.size[0]  # rows
    n = im.size[1]  # columns

    # Vectors Kr and Kc
    alpha = 8
    Kr = [randint(0, pow(2, alpha) - 1) for i in range(m)]
    Kc = [randint(0, pow(2, alpha) - 1) for i in range(n)]

    # Sub-key generation
    def getKeyMatrix(key, message, keyMatrix):
        k = 0
        for i in range(len(message)):
            for j in range(len(message)):
                keyMatrix[i][j] = ord(key[k]) % 65
                k += 1

    def encrypt(messageVector, message, cipherMatrix, keyMatrix):
        for i in range(len(message)):
            for j in range(1):
                cipherMatrix[i][j] = 0
                for x in range(len(message)):
                    cipherMatrix[i][j] += (keyMatrix[i][x] *
                                           messageVector[x][j])
                cipherMatrix[i][j] = cipherMatrix[i][j] % 26

    def HillCipher(message, key):
        keyMatrix = [[0] * (len(message)) for i in range(len(message))]
        cipherMatrix = [[0] for i in range(len(message))]
        getKeyMatrix(key, message, keyMatrix)
        messageVector = [[0] for i in range(len(message))]
        for i in range(len(message)):
            messageVector[i][0] = ord(message[i]) % 65
        encrypt(messageVector, message, cipherMatrix, keyMatrix)
        CipherText = []
        for i in range(len(message)):
            CipherText.append(chr(cipherMatrix[i][0] + 65))
        temp = []
        for i in range(len(CipherText)):
            temp.append(str(ord(CipherText[i]) - 65))
        for i in range(len(temp)):
            temp.append(temp[i][::-1])
        arr = list(map(int, temp))
        return arr

    message = input("Enter the private key (3 lettered):").upper()
    key1 = HillCipher(message, "GYBNQKURP")
    # key1=[15,14,7,51,71,70]
    for i in range(3):
        if key1[i] % 2 == 0:
            key1[i] = key1[i] + 1
        if 0 <= key1[i] <= 9:
            key1[i + 3] = key1[i] * 10

    # maximum number of iterations
    ITER_MAX = 3

    print('Vector Kr : ', Kr)
    print('Vector Kc : ', Kc)

    # key for encryption written into the file keys.txt
    f = open('keys.txt', 'w+')
    f.write('Vector Kr :\n')
    for a in Kr:
        f.write(str(a) + '\n')
    f.write('Vector Kc :\n')
    for a in Kc:
        f.write(str(a) + '\n')
    f.write('ITER_MAX :\n')
    f.write(str(ITER_MAX) + '\n')

    for iterations in range(ITER_MAX):
        # affine transformation
        for i in range(m):
            for j in range(n):
                r[i][j] = (key1[0] * r[i][j] + key1[3]) % 256
                g[i][j] = (key1[1] * g[i][j] + key1[4]) % 256
                b[i][j] = (key1[2] * b[i][j] + key1[5]) % 256
        # For each row
        for i in range(m):
            # right circular shift
            r[i] = numpy.roll(r[i], key1[3])
            g[i] = numpy.roll(g[i], key1[4])
            b[i] = numpy.roll(b[i], key1[5])
        # For each column
        for i in range(n):
            # up circular shift
            upshift(r, i, key1[0])
            upshift(g, i, key1[1])
            upshift(b, i, key1[2])

        # For each row
        for i in range(m):
            for j in range(n):
                if i % 2 == 1:
                    r[i][j] = r[i][j] ^ Kc[j]
                    g[i][j] = g[i][j] ^ Kc[j]
                    b[i][j] = b[i][j] ^ Kc[j]
                else:
                    r[i][j] = r[i][j] ^ rotate180(Kc[j])
                    g[i][j] = g[i][j] ^ rotate180(Kc[j])
                    b[i][j] = b[i][j] ^ rotate180(Kc[j])

        # For each column
        for j in range(n):
            for i in range(m):
                if j % 2 == 0:
                    r[i][j] = r[i][j] ^ Kr[i]
                    g[i][j] = g[i][j] ^ Kr[i]
                    b[i][j] = b[i][j] ^ Kr[i]
                else:
                    r[i][j] = r[i][j] ^ rotate180(Kr[i])
                    g[i][j] = g[i][j] ^ rotate180(Kr[i])
                    b[i][j] = b[i][j] ^ rotate180(Kr[i])
        for i in range(m):
            for j in range(n):
                pix[i, j] = (r[i][j], g[i][j], b[i][j])

if __name__ == '__main__':

    def saveimg(img):
        img.save('C:\\Users\\DELL\\Desktop\\cyber_algo\\encry_img_monkey.png')
        print("Success")
        exit(0)
    im = Image.open('C:\\Users\\DELL\\Desktop\\cyber_algo\\monkey.jpg')

    '''w,h = im.size
    with open("Width.txt", "w") as outfile:
        json.dump(w, outfile)
    with open("Height.txt", "w") as outfile:
        json.dump(h, outfile)

    def add_margin(img, top, right, bottom, left, color):
        width, height = img.size
        new_width = width + right + left
        new_height = height + top + bottom
        result = Image.new(img.mode, (new_width, new_height), color)
        result.paste(img, (left, top))
        return result

    if w>h:
        x = w-h
        im = add_margin(im,0,0,x,0,(255,255,255))
    elif h>w:
        x = h-w
        im = add_margin(im,0,x,0,0,(255,255,255))
    else:
        im = add_margin(im,0,0,0,0,(255,255,255))'''
    
    pix = im.load()#converting image to pixels as python object
    encryption(im, pix)
    saveimg(im)
    exit()
