import numpy as np
import cv2
import matplotlib.pylab as plt

BLACK = 0
WHITE = 255
BLK_SIZE = 4


def pick_unique(elements):
  ret = np.random.choice(elements)
  elements.remove(ret)
  return ret


def generate_B_Blk(B_pixel, indices, B_blk, desired_pixel, A_white_indices=[]):
  if desired_pixel == BLACK:
    if B_pixel == BLACK: # B: 1 pixel is white
      B_blk[pick_unique(indices)] = WHITE
    else: # B: 2 pixels are white
      B_blk[pick_unique(indices)] = WHITE
      B_blk[pick_unique(indices)] = WHITE
  else:
      B_blk[pick_unique(A_white_indices)] = WHITE
      if B_pixel == WHITE: # B: 2 pixels are white
        B_blk[pick_unique(indices)] = WHITE


def generate_encoded_blks(A_pixel, B_pixel, desired_pixel):
  A_blk = np.asarray([BLACK for i in range(BLK_SIZE)])
  B_blk = np.asarray([BLACK for i in range(BLK_SIZE)])
  indices = [i for i in range(BLK_SIZE)]
  if desired_pixel == BLACK: # C: all pixels are black
    if A_pixel == BLACK: # A: 1 pixel is white
      A_blk[pick_unique(indices)] = WHITE
      generate_B_Blk(B_pixel, indices, B_blk, desired_pixel)
    else: # A: 2 pixels are white
        A_blk[pick_unique(indices)] = WHITE
        A_blk[pick_unique(indices)] = WHITE
        generate_B_Blk(B_pixel, indices, B_blk, desired_pixel)
  else: # C: 1 pixel is white
    if A_pixel == BLACK: # A: 1 pixel is white
      A_white_pixel = pick_unique(indices)
      A_blk[A_white_pixel] = WHITE
      generate_B_Blk(B_pixel, indices, B_blk, desired_pixel, [A_white_pixel])
    else: # A: 2 pixels are white
        A_white_pixel_1 = pick_unique(indices)
        A_white_pixel_2 = pick_unique(indices)
        A_blk[A_white_pixel_1] = WHITE
        A_blk[A_white_pixel_2] = WHITE
        generate_B_Blk(B_pixel, indices, B_blk, desired_pixel, [A_white_pixel_1, A_white_pixel_2])
  C_blk = np.asarray([WHITE*(pixel == 2*WHITE) for pixel in A_blk + B_blk])
  return A_blk, B_blk, C_blk


def encode_images(A, B, C):
  H, W = A.shape[0], A.shape[1]
  enc_A = np.zeros((H*2, W*2))
  enc_B = np.zeros((H*2, W*2))
  enc_C = np.zeros((H*2, W*2))
  for row in range(H):
    for col in range(W):
      A_blk, B_blk, C_blk = generate_encoded_blks(A[row,col], B[row,col], C[row,col])
      enc_A[row*2:row*2+2, col*2:col*2+2] = A_blk.reshape((BLK_SIZE//2, BLK_SIZE//2))
      enc_B[row*2:row*2+2, col*2:col*2+2] = B_blk.reshape((BLK_SIZE//2, BLK_SIZE//2))
      enc_C[row*2:row*2+2, col*2:col*2+2] = C_blk.reshape((BLK_SIZE//2, BLK_SIZE//2))
  return enc_A, enc_B, enc_C


def convert_img_black_n_white(path, shape):
  originalImage = cv2.imread(path)[:shape[0], :shape[1]]
  grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
  (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
  return blackAndWhiteImage


shape = (600, 820)
A = convert_img_black_n_white('piano.jpg', shape)
B = convert_img_black_n_white('butterfly.png', shape)
C = convert_img_black_n_white('ship.png', shape)

enc_A, enc_B, enc_C = encode_images(A, B, C)

plt.figure(figsize=(12,8))
plt.subplot('131')
plt.title('enc_A')
plt.imshow(enc_A, cmap='gray')
plt.subplot('132')
plt.title('enc_B')
plt.imshow(enc_B, cmap='gray')
plt.subplot('133')
plt.title('enc_C')
plt.imshow(enc_C, cmap='gray')

cv2.imwrite('A.bmp', enc_A)
cv2.imwrite('B.bmp', enc_B)
cv2.imwrite('C.bmp', enc_C)