import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import tensorflow as tf

###Inicialization
x = tf.constant(4, shape=(1, 1), dtype=tf.float32)
x = tf.constant([[3,2],[1,3]], shape = (2,2), dtype = tf.int32)
x = tf.ones(3,dtype =tf.int64)
x = tf.random.normal((3,3), mean =0, stddev =0.5)
x = tf.random.uniform((3,3,2), minval =0, maxval=5)
x = tf.range(12)
y= tf.range(0,-10,-1)
#z = tf.add(x,y)
#z=tf.subtract(x,y)
#z=tf.multiply(x,y)
#z=tf.divide(x,y)
#z=tf.tensordot(x, y, axes=1)##Producto escalar
#z=tf.matmul(x,y) #@ also se usa
indices = tf.constant([0,1])
x_ind = tf.gather(x,indices)
x = tf.reshape(x,(3,4))
x = tf.transpose(x, perm = [1,0]) ##en 2D so funciona esta perm
print(x.dtype)
#print(tf.cast(x, dtype=tf.float64))
###Print code, you have to initialize a session, the tensor object needs to be evaluated
###Probably the yt guy mades with conda but sudando
with tf.compat.v1.Session() as sess:
    init = tf.compat.v1.global_variables_initializer()
    sess.run(init)
    print(x.eval())
    print


