# pypyc
Pypyc website wrapper.

# Usage

## Login
```py
from pypyc import Pypyc

pyc = Pypyc()
pyc.login("pyccode", "password")
```

## Getting Messages
Messages can be obtained with `pyc.getMessages(pageNumber)`.  
Messages are returned as a list of `Message` objects  
```py
messages_list = pyc.getMessages(1)
print(messages_list[0].title)
```

## Getting Circulars
Circulars can be obtained with `pyc.getCirculars()`.  
Circulars are returned as a list of `Circular` objects  
```py
circulars_list = pyc.getCirculars()
print(circulars_list[0].title)
```

# Classes

## Message
### Properties
`title` _str_  
Title of the message  
  
`url` _str_  
Link to the message  
  
`icon` _str | None_  
Returns attachment icon in markdown format if there are attachments in the message  
  
`author` _str_  
Author of the message  
  
`date` _str_  
Message creation date  
  
`messageId` _str_  
The message's id  
  
`authorId` _str_  
The author's id  
  
`attachmentId` _str_  
The attachment's id. Returns `"0"` there are no attachments in the message  

`hasAttachments` _bool_
Returns `True` if message contains attachments

### Methods
`getText()` _str_  
Returns message content in text  


## Message
### Properties
`title` _str_  
Title of the circular  
  
`date` _str_  
Creation date of the circular  
  
`id` _str_  
Circular's unique Id  
  
`url` _str_  
Link to the circular  

### Methods
`getBinaryContent()` _bytes_  
Returns Binary Content of the circular's PDF 