function convertToSingleLine(text) {
    var unescapedText = text.replace(/\\([bfnrtv'"\\/]|u[0-9a-fA-F]{4}|x[0-9a-fA-F]{2}|[0-7]{1,3})/g, function(match, capture) {
      switch (capture) {
        case 'b':
          return '\\b';
        case 'f':
          return '\\f';
        case 'n':
          return '\\n';
        case 'r':
          return '\\r';
        case 't':
          return '\\t';
        case 'v':
          return '\\v';
        case '\'':
          return '\'';
        case '\"':
          return '\"';
        case '\\':
          return '\\';
        case '\/':
          return '\/';
        default:
          if (capture.startsWith('u')) {
            var unicode = String.fromCharCode(parseInt(capture.substring(1), 16));
            return unicode;
          } else if (capture.startsWith('x')) {
            var hex = String.fromCharCode(parseInt(capture.substring(1), 16));
            return hex;
          } else {
            var octal = String.fromCharCode(parseInt(capture, 8));
            return octal;
          }
      }
    });
  
    // Remove line breaks and extra whitespace
    unescapedText = unescapedText.replace(/\n/g, ' \\n').replace(/\r/g, ' \\r').replace(/\s+/g, ' ');
  
    return unescapedText;
  }
  var source = `hello
  my name is`
  var unsource = convertToSingleLine(source)
  