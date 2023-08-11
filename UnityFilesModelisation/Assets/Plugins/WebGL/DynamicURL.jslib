mergeInto(LibraryManager.library, {
    GetURLFromPage: function () {
        var search = window.location.origin;
	var bufferSize = lengthBytesUTF8(search) + 1
	var buffer = _malloc(bufferSize);
	stringToUTF8(search, buffer, bufferSize);
	return buffer;
    },
    GetIDFromPage: function () {
        var search = window.location.href;
        
        var regex = /\/([^\/]*)$/;
        var match = search.match(regex);
        var result = "";

        if (match && match.length >= 2) {
            result = match[1];
        }
	console.log(result);
        var bufferSize = lengthBytesUTF8(result) + 1
	var buffer = _malloc(bufferSize);
	stringToUTF8(result, buffer, bufferSize);
	console.log(buffer);
	return buffer;
    }
});
