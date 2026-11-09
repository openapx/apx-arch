# apx-arch
openapx Arch app and REST API



## Configuration

### APP_HOME environmental variable
The `APP_HOME` or `APPHOME` environmental variable points to the directory where the app and API configurations are stored. This 
directory should not be the app and API installation directory or one of its subdirectories.

The `APP_HOME` directory and its content should be readable by the account that runs the app and API services.

The environmental variables `APP_HOME` and `APPHOME` are case insensitive. Only one can and should be defined.
<br/>

### Configuration property files
The app and API configuration property files are stored in the `$APP_HOME/config` directory with file extension 
`.properties`. The configuration property files are read and interpreted in natural sort order. 

Only the `config` directory in lower case is currently supported. 
<br/>

### Configuration properties
A configuration property is defined through one or more configuration property files. If a particular property is defined in more than one property file, an error will occurr.

A property is a key/value pair delimited by a single equal sign `=`. Only the first occurrence of an equal sign is interpreted as the delimiter and any subsequent equal signs are assumed to be part of the property value.

A property key or name 
* consists of the characters A-Z, digits 0-9 and a period `.`
* cannot start or end with a period
* longer than 2 characters

A property key or name does not currently have a limit on the maximum number of characters.

The property value starts at the character after the delimiter until the end of the current line. Multiline property values are not supported.

Leading and trailing whitespace is ignored for both the property key and value.

Lines starting with first non-whitespace character equal to a hash `#` are interpreted as comments. Inline comments, such as `MYKEY = MY VALUE   # some comment` is currently not supported with the string `# some comment` assumed to be part of the property value.

Lines consisting entirely of whitespace are ignored
<br/>

