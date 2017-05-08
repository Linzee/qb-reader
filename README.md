# QB reader
Small Python library for reading and writing (Qubicle Binary (.qb))[http://minddesk.com/learn/article.php?id=22] files.

### Reading
```
import Qb

with open('example.qb', 'rb') as file:
	qb = Qb()
	qb.load(file)

	layer = qb.matrixList[0]

	layer.pos // Position of voxel matrix: (0, 0, 0)
	layer.data.shape() // Size: (10, 8, 10)

	layer[0][2][1] // Voxel color at position x=0 y=2 z=1: 0xffffffff
```

### Writing
```
import Qb

with open('example.qb', 'wb') as file:
	qb = Qb()
	layer = QbMatrix("main", data, (0, 0, 0)) // Matrix name, data as 3-dimensional array, position of matrix
	qb.matrixList.append(layer)
	qb.save(file)
```