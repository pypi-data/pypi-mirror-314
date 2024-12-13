from .formats import AbstractDataFileFormat, dataFileFormatsDictionary, availableExtensions, dataFileFormats

def registerDatafileFormat(datafileFormat: AbstractDataFileFormat):
    global dataFileFormatsDictionary, availableExtensions

    if not isinstance(datafileFormat, AbstractDataFileFormat):
        raise ValueError(f"Expected an instance of AbstractDataFileFormat, got {type(datafileFormat)}")
    
    if datafileFormat in dataFileFormats:
        raise ValueError(f"DataFileFormat {datafileFormat} is already registered")

    if not isinstance(datafileFormat.extension, str):
        raise ValueError(f"Extension must be a string, got {type(datafileFormat.extension)}")
    
    if not datafileFormat.extension:
        raise ValueError("Extension must not be empty")
    
    if datafileFormat.extension in dataFileFormatsDictionary:
        raise ValueError(f"Extension {datafileFormat.extension} is already registered in dictionnary")

    if datafileFormat.extension in availableExtensions:
        raise ValueError(f"Extension {datafileFormat.extension} is already registered in available extensions")
    
    # Add the datafile format to the list
    dataFileFormats.append(datafileFormat)
    
    # Add the datafile format to the dictionary
    dataFileFormatsDictionary[datafileFormat.extension] = datafileFormat

    # Add the extension to the list of available extensions
    availableExtensions.add(datafileFormat.extension)
