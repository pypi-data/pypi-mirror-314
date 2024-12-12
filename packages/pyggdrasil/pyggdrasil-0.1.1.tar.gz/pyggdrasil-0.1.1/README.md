 This is a tiny library to print nested dictionaries as trees in the format of
 file trees.

 # Install

    pip install pyggdrasil


# Use

```
>>> from pyggdrasil import render_tree
>>>
>>> data = {
>>>     1: {
>>>         "a": ["A", "B", "C"],
>>>         "b": ["D", "E"]
>>>     },
>>>     2: {
>>>         "x": ["V", "W", "Q"],
>>>         "y": ["Y", "Z"],
>>>         "z": ["X", "Y"],
>>>     }
>>> }
>>> print(render_tree(data))

├─ 1
│  ├─ a
│  │  ├─ A
│  │  ├─ B
│  │  └─ C
│  └─ b
│     ├─ D
│     └─ E
└─ 2
   ├─ x
   │  ├─ V
   │  ├─ W
   │  └─ Q
   ├─ y
   │  ├─ Y
   │  └─ Z
   └─ z
      ├─ X
      └─ Y
```
